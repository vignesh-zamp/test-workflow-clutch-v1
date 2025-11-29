import asyncio
import os
from extraction import extract_data, classify_document
from verification import verify_case
from data_model import FullCaseData
from utils import generate_stock_id
import concurrent.futures
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EXTRACT_DIR = "downloads/extracted"

def main():
    if not os.path.exists(EXTRACT_DIR):
        print(f"Directory {EXTRACT_DIR} does not exist.")
        return

    print(f"Scanning {EXTRACT_DIR}...")
    
    doc_paths = {}
    
    # 1. Identify files
    for root, dirs, files in os.walk(EXTRACT_DIR):
        for file in files:
            if file.startswith(".") or file.endswith(".DS_Store"): continue
            
            file_path = os.path.join(root, file)
            
            # Simple heuristic or re-classify
            # Since we renamed them in main.py, we might rely on filename
            if "BOS" in file:
                doc_type = "BOS"
            elif "BANK" in file:
                doc_type = "BANK"
            elif "OWNERSHIP" in file:
                doc_type = "OWNERSHIP"
            elif "LIEN" in file:
                doc_type = "LIEN"
            elif "DL" in file or "Screenshot" in file: # DL was a screenshot
                doc_type = "DL"
            else:
                print(f"Classifying {file}...")
                doc_type = classify_document(file_path)
            
            print(f"Found {doc_type}: {file}")
            doc_paths[doc_type] = file_path

    # Check for the main DL screenshot in the parent directory
    dl_path = "downloads/dl_screenshot.png"
    if os.path.exists(dl_path):
        print(f"Found DL: {dl_path}")
        doc_paths["DL"] = dl_path
    else:
        print(f"DL screenshot not found at {dl_path}")

    # 2. Extract Data
    print("\nStarting Extraction...")
    extracted_data = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for doc_type, path in doc_paths.items():
            futures[executor.submit(extract_data, path, doc_type)] = doc_type
        
        for future in concurrent.futures.as_completed(futures):
            doc_type = futures[future]
            try:
                data = future.result()
                extracted_data[doc_type] = data
                print(f"Successfully extracted {doc_type}")
                print(f"--- {doc_type} Data ---")
                print(data.model_dump_json(indent=2))
                print("---------------------")
            except Exception as e:
                print(f"Extraction failed for {doc_type}: {e}")

    # 3. Verify
    print("\nStarting Verification...")
    stock_id = generate_stock_id()
    
    case_data = FullCaseData(
        stock_id=stock_id,
        bos=extracted_data.get("BOS"),
        dl=extracted_data.get("DL"),
        banking=extracted_data.get("BANK"),
        ownership=extracted_data.get("OWNERSHIP"),
        lien=extracted_data.get("LIEN")
    )
    
    verified_case = verify_case(case_data)
    
    print("\nVerification Results:")
    for res in verified_case.verification_results:
        print(f"\n--- {res.validation_status} ---")
        print(f"Reasoning: {res.validation_reasoning}")
        if res.validation_details:
            print(f"Details: {res.validation_details}")
        if res.failure_details:
            print(f"Failure: {res.failure_details}")
            
if __name__ == "__main__":
    main()
