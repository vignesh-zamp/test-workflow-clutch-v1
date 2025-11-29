import google.generativeai as genai
import os
import json
from data_model import BillOfSale, DriversLicense, BankingDocument, VehicleOwnership, LienDocument
import typing_extensions as typing
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
# Assumes GEMINI_API_KEY is set in environment variables
if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def classify_document(file_path: str) -> str:
    """
    Classifies a document into one of the known types: BOS, BANK, OWNERSHIP, LIEN, or UNKNOWN.
    """
    model_name = "gemini-2.5-flash"
    model = genai.GenerativeModel(model_name=model_name)
    
    sample_file = genai.upload_file(path=file_path, display_name=os.path.basename(file_path))
    
    prompt = """
    Analyze this document and classify it into exactly one of these categories based on these specific rules:
    - BOS (Bill of Sale): Look for the word "Clutch".
    - LIEN (Lien Check): Look for the word "Lien".
    - OWNERSHIP (Vehicle Ownership/Registration): Look for the phrase "Permit - Vehicle".
    - BANK (Void Cheque/Direct Deposit): Look for the phrase "Transit number".
    - UNKNOWN: If it doesn't fit any of the above.
    
    Return ONLY the category code (e.g., "BOS").
    """
    
    try:
        result = model.generate_content([sample_file, prompt])
        return result.text.strip()
    except Exception as e:
        print(f"Classification failed for {file_path}: {e}")
        return "UNKNOWN"


def extract_data(file_path: str, doc_type: str):
    """
    Extracts structured data from a document image using Gemini 2.5.
    """
    model_name = "gemini-2.5-flash" # Or gemini-1.5-pro-latest, using a capable model
    
    # Upload file
    sample_file = genai.upload_file(path=file_path, display_name=os.path.basename(file_path))
    
    # Select the appropriate Pydantic model
    # Select the appropriate Pydantic model and detailed prompt
    # Select the appropriate Pydantic model and detailed prompt
    if doc_type == "BOS":
        response_schema = BillOfSale
        prompt = """
        You are a precise Bill of Sale document extraction agent.
        
        ## Objective
        Read the provided Bill of Sale (BOS) document and extract the following vehicle transaction details. If a value is missing or not found, return "NA".
        
        ## Fields to Extract
        1. Customer_Full_Name: Extract complete buyer name. Remove "OBO", "C/O", business entities.
        2. Customer_First_Name: First name from cleaned full name.
        3. Customer_Last_Name: Last name from cleaned full name.
        4. BOS_Effective_Date: Date of sale (MM/DD/YYYY).
        5. Vehicle_Year: 4-digit year.
        6. Vehicle_Make: Manufacturer/Brand.
        7. Vehicle_Model: Model name.
        8. VIN_Full: 17-char VIN.
        9. VIN_Last_6: Last 6 digits of VIN.
        10. Stock_ID: Stock/Inventory number.
        11. Net_Vehicle_Value: Final net amount (numeric).
        
        ## Multiple Owner Parsing
        If multiple owners (e.g., "AND", "&"), split and populate Customer_Names_Parsed.
        
        ## Output Format
        Return JSON matching this structure:
        {
          "Stock_ID": "...",
          "Customer_Full_Name": "...",
          "Customer_First_Name": "...",
          "Customer_Last_Name": "...",
          "BOS_Effective_Date": "...",
          "Vehicle_Year": "...",
          "Vehicle_Make": "...",
          "Vehicle_Model": "...",
          "VIN_Full": "...",
          "VIN_Last_6": "...",
          "Net_Vehicle_Value": 0.0,
          "Customer_Names_Parsed": [{"Full_Name": "...", ...}],
          "Owner_Count": 1,
          "Multiple_Owners": false,
          "Confidence_Score": 0.95,
          "Extraction_Notes": "..."
        }
        """
    elif doc_type == "DL":
        response_schema = DriversLicense
        prompt = """
        You are a precise identity document extraction agent.
        
        ## Objective
        Read the provided ID document and extract identity details. If missing, return "NA".
        
        ## Fields to Extract
        1. ID_Full_Name: FIRST MIDDLE LAST.
        2. ID_First_Name: First name.
        3. ID_Middle_Name: Middle name/initial (NA if none).
        4. ID_Last_Name: Last name.
        5. ID_Date_of_Birth: MM/DD/YYYY.
        6. ID_Issue_Date: MM/DD/YYYY.
        7. ID_Expiry_Date: MM/DD/YYYY.
        8. ID_Number: License/ID number.
        9. ID_Type: DriverLicense, Passport, PRCard, CitizenshipCard, MilitaryID, OntarioPhotoID, or NA.
        10. ID_Status: valid, expired, suspended, unknown.
        11. Temporary_ID_Provided: "Y" or "N".
        12. Temporary_ID_Type: Type if temporary.
        13. Temporary_ID_Expiry_Date: MM/DD/YYYY.
        
        ## Output Format
        Return JSON matching this structure:
        {
          "Stock_ID": "...",
          "Owner_Number": "...",
          "ID_Full_Name": "...",
          "ID_First_Name": "...",
          "ID_Middle_Name": "...",
          "ID_Last_Name": "...",
          "ID_Date_of_Birth": "...",
          "ID_Issue_Date": "...",
          "ID_Expiry_Date": "...",
          "ID_Number": "...",
          "ID_Type": "...",
          "ID_Status": "...",
          "Temporary_ID_Provided": "...",
          "Temporary_ID_Type": "...",
          "Temporary_ID_Expiry_Date": "...",
          "Confidence_Score": 0.95,
          "Extraction_Notes": "..."
        }
        """
    elif doc_type == "BANK":
        response_schema = BankingDocument
        prompt = """
        You are a banking document extraction agent.
        
        ## Objective
        Extract banking details from Void Cheque, Direct Deposit form, or Bank Statement.
        
        ## Fields to Extract
        1. Account_Holder_Name: Name on the account.
        2. Bank_Institution_Number: 3 digits.
        3. Bank_Transit_Number: 5 digits.
        4. Bank_Account_Number: 7-12 digits.
        5. Bank_Account_Type: "Chequing" or "Savings".
        6. Bank_Name: Name of the bank.
        
        ## Output Format
        Return JSON matching this structure:
        {
          "Stock_ID": "...",
          "Account_Holder_Name": "...",
          "Bank_Institution_Number": "...",
          "Bank_Transit_Number": "...",
          "Bank_Account_Number": "...",
          "Bank_Account_Type": "...",
          "Bank_Name": "...",
          "Confidence_Score": 0.95,
          "Extraction_Notes": "..."
        }
        """
    elif doc_type == "OWNERSHIP":
        response_schema = VehicleOwnership
        prompt = """
        You are a vehicle ownership document extraction agent.
        
        ## Objective
        Extract details from Vehicle Ownership / Registration / Permit.
        
        ## Fields to Extract
        1. Owner_Name: Full name of owner.
        2. VIN: Vehicle Identification Number.
        3. VIN_Last_6: Last 6 digits.
        4. Year: Vehicle year.
        5. Make: Vehicle make.
        6. Model: Vehicle model.
        7. Registration_Date: Date issued (MM/DD/YYYY).
        8. Province: Province code (e.g., ON).
        
        ## Output Format
        Return JSON matching this structure:
        {
          "Stock_ID": "...",
          "Owner_Name": "...",
          "VIN": "...",
          "VIN_Last_6": "...",
          "Year": "...",
          "Make": "...",
          "Model": "...",
          "Registration_Date": "...",
          "Province": "...",
          "Confidence_Score": 0.95,
          "Extraction_Notes": "..."
        }
        """
    elif doc_type == "LIEN":
        response_schema = LienDocument
        prompt = """
        You are a lien search document extraction agent.
        
        ## Objective
        Extract details from Lien Search or PPSA Search.
        
        ## Fields to Extract
        1. Lien_Status: "Active", "Discharged", "None".
        2. Debtor_Name: Name of debtor.
        3. VIN: Vehicle VIN.
        4. Year: Vehicle year.
        5. Make: Vehicle make.
        6. Model: Vehicle model.
        7. Lender_Name: Secured party name.
        8. Lien_Amount: Original amount (numeric).
        9. Outstanding_Amount: Current amount (numeric).
        10. Per_Diem: Daily interest (numeric).
        11. Valid_Until_Date: Expiry date (MM/DD/YYYY).
        
        ## Output Format
        Return JSON matching this structure:
        {
          "Stock_ID": "...",
          "Lien_Status": "...",
          "Debtor_Name": "...",
          "VIN": "...",
          "Year": "...",
          "Make": "...",
          "Model": "...",
          "Lender_Name": "...",
          "Lien_Amount": 0.0,
          "Outstanding_Amount": 0.0,
          "Per_Diem": 0.0,
          "Valid_Until_Date": "...",
          "Confidence_Score": 0.95,
          "Extraction_Notes": "..."
        }
        """
    else:
        raise ValueError(f"Unknown document type: {doc_type}")

    # Configure generation to return JSON, but don't enforce schema via SDK to avoid "Unknown field" errors
    # We rely on the prompt to guide the structure and Pydantic to validate the result.
    generation_config = genai.GenerationConfig(
        response_mime_type="application/json"
    )
    
    model = genai.GenerativeModel(model_name=model_name)
    
    try:
        result = model.generate_content(
            [sample_file, prompt],
            generation_config=generation_config
        )
        
        # Parse result manually
        data = json.loads(result.text)
        
        # Instantiate Pydantic model
        # This will validate the data against our model
        return response_schema(**data)
        
    except json.JSONDecodeError:
        print(f"Failed to decode JSON for {doc_type}. Raw text: {result.text}")
        return None
    except Exception as e:
        print(f"Error parsing Gemini response for {doc_type}: {e}")
        # print(f"Raw response: {result.text}")
        return None
