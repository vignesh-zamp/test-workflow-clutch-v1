from pydantic import BaseModel
from typing import Optional, List, Any

# --- Extraction Models ---

class CustomerNameParsed(BaseModel):
    Full_Name: Optional[str] = None
    First_Name: Optional[str] = None
    Last_Name: Optional[str] = None
    Owner_Number: Optional[int] = None

class BillOfSale(BaseModel):
    Stock_ID: Optional[str] = None
    Customer_Full_Name: Optional[str] = None
    Customer_First_Name: Optional[str] = None
    Customer_Last_Name: Optional[str] = None
    BOS_Effective_Date: Optional[str] = None
    Vehicle_Year: Optional[str] = None # Prompt says "2020" (digits), could be int or str
    Vehicle_Make: Optional[str] = None
    Vehicle_Model: Optional[str] = None
    VIN_Full: Optional[str] = None
    VIN_Last_6: Optional[str] = None
    Net_Vehicle_Value: Optional[float] = None
    Customer_Names_Parsed: Optional[List[CustomerNameParsed]] = None
    Owner_Count: Optional[int] = None
    Multiple_Owners: Optional[bool] = None
    Confidence_Score: Optional[float] = None
    Extraction_Notes: Optional[str] = None

class DriversLicense(BaseModel):
    Stock_ID: Optional[str] = None
    Owner_Number: Optional[str] = None
    ID_Full_Name: Optional[str] = None
    ID_First_Name: Optional[str] = None
    ID_Middle_Name: Optional[str] = None
    ID_Last_Name: Optional[str] = None
    ID_Date_of_Birth: Optional[str] = None
    ID_Issue_Date: Optional[str] = None
    ID_Expiry_Date: Optional[str] = None
    ID_Number: Optional[str] = None
    ID_Type: Optional[str] = None
    ID_Status: Optional[str] = None
    Temporary_ID_Provided: Optional[str] = None # "Y" or "N"
    Temporary_ID_Type: Optional[str] = None
    Temporary_ID_Expiry_Date: Optional[str] = None
    Confidence_Score: Optional[float] = None
    Extraction_Notes: Optional[str] = None

class BankingDocument(BaseModel):
    Stock_ID: Optional[str] = None
    Account_Holder_Name: Optional[str] = None
    Bank_Institution_Number: Optional[str] = None
    Bank_Transit_Number: Optional[str] = None
    Bank_Account_Number: Optional[str] = None
    Bank_Account_Type: Optional[str] = None
    Bank_Name: Optional[str] = None
    Confidence_Score: Optional[float] = None
    Extraction_Notes: Optional[str] = None

class VehicleOwnership(BaseModel):
    Stock_ID: Optional[str] = None
    Owner_Name: Optional[str] = None
    VIN: Optional[str] = None
    VIN_Last_6: Optional[str] = None
    Year: Optional[str] = None
    Make: Optional[str] = None
    Model: Optional[str] = None
    Registration_Date: Optional[str] = None
    Province: Optional[str] = None
    Confidence_Score: Optional[float] = None
    Extraction_Notes: Optional[str] = None

class LienDocument(BaseModel):
    Stock_ID: Optional[str] = None
    Lien_Status: Optional[str] = None
    Debtor_Name: Optional[str] = None
    VIN: Optional[str] = None
    Year: Optional[str] = None
    Make: Optional[str] = None
    Model: Optional[str] = None
    Lender_Name: Optional[str] = None
    Lien_Amount: Optional[float] = None
    Outstanding_Amount: Optional[float] = None
    Per_Diem: Optional[float] = None
    Valid_Until_Date: Optional[str] = None
    Confidence_Score: Optional[float] = None
    Extraction_Notes: Optional[str] = None

# --- Verification Models ---

class ValidationChecks(BaseModel):
    name_match: Optional[bool] = None
    expiration_valid: Optional[bool] = None
    alternative_id_validated: Optional[bool] = None
    co_owner_check: Optional[bool] = None

class NameComponents(BaseModel):
    first_name_match: Optional[bool] = None
    last_name_match: Optional[bool] = None
    mismatch_component: Optional[str] = None
    expected_value: Optional[str] = None
    actual_value: Optional[str] = None

class ValidationDetails(BaseModel):
    bos_customer_name: Optional[str] = None
    id_customer_name: Optional[str] = None
    name_match_result: Optional[str] = None
    name_components: Optional[NameComponents] = None
    id_expiry_date: Optional[str] = None
    bos_effective_date: Optional[str] = None
    expiration_status: Optional[str] = None
    days_expired: Optional[int] = None
    grace_period_applied: Optional[bool] = None
    alternative_id_used: Optional[bool] = None
    alternative_id_type: Optional[str] = None
    proof_of_residence_accepted: Optional[bool] = None

class FailureDetails(BaseModel):
    failure_category: Optional[str] = None
    specific_issue: Optional[str] = None
    affected_owner: Optional[int] = None

class NextSteps(BaseModel):
    requires_alternative_id: Optional[bool] = None
    requires_proof_of_residence: Optional[bool] = None
    requires_co_owner_id: Optional[bool] = None
    can_proceed_to_completion: Optional[bool] = None

class VerificationResult(BaseModel):
    stock_id: Optional[str] = None
    verification_type: Optional[str] = None # e.g. "DL-BOS", "BOS-BANK"
    validation_status: Optional[str] = None # PASS|FAIL
    validation_timestamp: Optional[str] = None
    checks_performed: Optional[ValidationChecks] = None
    validation_details: Optional[Any] = None # Flexible dict for different validation types
    failure_details: Optional[FailureDetails] = None
    next_steps: Optional[NextSteps] = None
    comment_for_task: Optional[str] = None
    task_status_recommendation: Optional[str] = None
    validation_reasoning: Optional[str] = None

class FullCaseData(BaseModel):
    stock_id: str
    bos: Optional[BillOfSale] = None
    dl: Optional[DriversLicense] = None
    banking: Optional[BankingDocument] = None
    ownership: Optional[VehicleOwnership] = None
    lien: Optional[LienDocument] = None
    verification_results: List[VerificationResult] = []
