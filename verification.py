import google.generativeai as genai
import os
import json
from data_model import FullCaseData, VerificationResult

def verify_case(case_data: FullCaseData) -> FullCaseData:
    """
    Performs cross-document validation using Gemini 2.5 and specific validation prompts.
    """
    model_name = "gemini-2.5-flash"
    model = genai.GenerativeModel(model_name=model_name)
    
    # 1. DL-BOS Validation
    if case_data.bos and case_data.dl:
        print("Running DL-BOS Validation...")
        
        # Prepare input context
        input_context = {
            "bos_data": case_data.bos.model_dump(),
            "id_data_primary": case_data.dl.model_dump(),
            "proof_of_residence_provided": False, # Default for now
            "stock_id": case_data.stock_id
        }
        
        prompt = f"""
        You are a precise identity verification validator.
        
        ## Objective
        Validate Driver's License/ID data against the Bill of Sale (BOS) using strict matching rules.
        
        ## Input Data
        {json.dumps(input_context, indent=2, default=str)}
        
        ## Validation Rules
        1. Exact Name Matching: First and Last names must match EXACTLY (case-insensitive). No abbreviations.
        2. ID Expiration: ID must not be expired > 30 days relative to BOS Effective Date.
        3. Alternative ID: If primary ID expired/suspended, check alternative (not provided here).
        4. Suspended License: Fail unless proof of residence provided.
        
        ## Output Format
        Return JSON matching this structure:
        {{
          "stock_id": "...",
          "validation_status": "PASS|FAIL",
          "validation_timestamp": "...",
          "checks_performed": {{ "name_match": true, "expiration_valid": true, ... }},
          "validation_details": {{
            "bos_customer_name": "...",
            "id_customer_name": "...",
            "name_match_result": "...",
            "expiration_status": "...",
            "days_expired": 0
          }},
          "failure_details": {{ "failure_category": "...", "specific_issue": "..." }},
          "next_steps": {{ "can_proceed_to_completion": true }},
          "comment_for_task": "...",
          "validation_reasoning": "..."
        }}
        """
        
        try:
            result = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(response_mime_type="application/json")
            )
            validation_data = json.loads(result.text)
            
            # Map to VerificationResult
            res = VerificationResult(
                stock_id=case_data.stock_id,
                verification_type="DL-BOS",
                validation_status=validation_data.get("validation_status", "FAIL"),
                validation_timestamp=validation_data.get("validation_timestamp"),
                # We can store the full details if we expand the model, but for now map to existing fields
                checks_performed=validation_data.get("checks_performed"),
                validation_details=validation_data.get("validation_details"),
                failure_details=validation_data.get("failure_details"),
                next_steps=validation_data.get("next_steps"),
                comment_for_task=validation_data.get("comment_for_task"),
                task_status_recommendation=validation_data.get("task_status_recommendation"),
                validation_reasoning=validation_data.get("validation_reasoning")
            )
            case_data.verification_results.append(res)
            
        except Exception as e:
            print(f"DL-BOS Validation failed: {e}")
            case_data.verification_results.append(VerificationResult(
                stock_id=case_data.stock_id,
                validation_status="FAIL",
                validation_reasoning=f"Validation error: {e}"
            ))
    # 2. BOS-BANK Validation
    if case_data.bos and case_data.banking:
        print("Running BOS-BANK Validation...")
        input_context = {
            "bos_data": case_data.bos.model_dump(),
            "banking_data": case_data.banking.model_dump(),
            "stock_id": case_data.stock_id
        }
        prompt = f"""
        You are a precise banking verification validator.
        
        ## Objective
        Validate Banking document data against the Bill of Sale (BOS).
        
        ## Input Data
        {json.dumps(input_context, indent=2, default=str)}
        
        ## Validation Rules
        1. Name Match: Bank Account Holder Name must match BOS Customer Name (Exact match).
        2. Account Type: Must be "Chequing". Reject "Savings".
        3. Account Number Structure: Validate Institution (3 digits), Transit (5 digits), Account (7-12 digits).
        
        ## Output Format (JSON)
        {{
          "validation_status": "PASS|FAIL",
          "validation_details": {{
             "bos_name": "...",
             "bank_name": "...",
             "name_match": true,
             "account_type_valid": true
          }},
          "failure_details": {{ "specific_issue": "..." }},
          "validation_reasoning": "..."
        }}
        """
        _run_validation(model, prompt, case_data, "BOS-BANK")

    # 3. BOS-OWNERSHIP Validation
    if case_data.bos and case_data.ownership:
        print("Running BOS-OWNERSHIP Validation...")
        input_context = {
            "bos_data": case_data.bos.model_dump(),
            "ownership_data": case_data.ownership.model_dump(),
            "stock_id": case_data.stock_id
        }
        prompt = f"""
        You are a vehicle ownership validator.
        
        ## Objective
        Validate Ownership/Registration data against the Bill of Sale (BOS).
        
        ## Input Data
        {json.dumps(input_context, indent=2, default=str)}
        
        ## Validation Rules
        1. VIN Match: BOS VIN (or last 6) must match Ownership VIN exactly.
        2. Ownership Duration: Registration Date must be <= (BOS Date - 60 days). 
           - If owned < 60 days, FAIL (requires supporting docs).
        3. Vehicle Details: Make/Model/Year must match.
        
        ## Output Format (JSON)
        {{
          "validation_status": "PASS|FAIL",
          "validation_details": {{
             "vin_match": true,
             "days_owned": 100,
             "duration_valid": true
          }},
          "failure_details": {{ "specific_issue": "..." }},
          "validation_reasoning": "..."
        }}
        """
        _run_validation(model, prompt, case_data, "BOS-OWNERSHIP")

    # 4. BOS-LIEN Validation
    if case_data.bos and case_data.lien:
        print("Running BOS-LIEN Validation...")
        input_context = {
            "bos_data": case_data.bos.model_dump(),
            "lien_data": case_data.lien.model_dump(),
            "stock_id": case_data.stock_id
        }
        prompt = f"""
        You are a lien validator.
        
        ## Objective
        Validate Lien document data against the Bill of Sale (BOS).
        
        ## Input Data
        {json.dumps(input_context, indent=2, default=str)}
        
        ## Validation Rules
        1. VIN Match: BOS VIN must match Lien VIN.
        2. Lien Amount Reconciliation: 
           - BOS 'Applicable Loan Balance' should match Lien 'Outstanding Amount' (or 'Lien Amount').
           - Tolerance: +/- $100.
        3. Status: If 'Discharged', amount should be 0.
        
        ## Output Format (JSON)
        {{
          "validation_status": "PASS|FAIL",
          "validation_details": {{
             "vin_match": true,
             "amount_difference": 0.0,
             "amount_match": true
          }},
          "failure_details": {{ "specific_issue": "..." }},
          "validation_reasoning": "..."
        }}
        """
        _run_validation(model, prompt, case_data, "BOS-LIEN")

    return case_data

def _run_validation(model, prompt, case_data, doc_type):
    try:
        result = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        validation_data = json.loads(result.text)
        
        res = VerificationResult(
            stock_id=case_data.stock_id,
            verification_type=doc_type,
            validation_status=validation_data.get("validation_status", "FAIL"),
            validation_details=validation_data.get("validation_details"),
            failure_details=validation_data.get("failure_details"),
            validation_reasoning=validation_data.get("validation_reasoning")
        )
        case_data.verification_results.append(res)
    except Exception as e:
        print(f"{doc_type} Validation failed: {e}")
        case_data.verification_results.append(VerificationResult(
            stock_id=case_data.stock_id,
            verification_type=doc_type,
            validation_status="FAIL",
            validation_reasoning=f"Validation error: {e}"
        ))
