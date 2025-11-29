import asyncio
import os
from browser import BrowserAgent
from extraction import extract_data, classify_document
from verification import verify_case
from data_model import FullCaseData
from utils import generate_stock_id, save_dataset
import concurrent.futures
from dotenv import load_dotenv
import zipfile
import shutil

# Load environment variables
load_dotenv()

# Configuration
URL = "https://admin.staging.clutchenv.ca/private-purchases/59213148-6383-40fe-80f3-cc699c52abdb/tasks"
USERNAME = "benjamin.koppeser+zamp@clutch.ca"
PASSWORD = "MUSASHI-detailed-regiment-bothers-1!"
OUTPUT_DIR = "downloads"
VIDEO_DIR = "videos"

async def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    agent = BrowserAgent()
    await agent.start(record_video_dir=VIDEO_DIR)
    
    try:
        # 1. Login & Navigate
        await agent.login(URL, USERNAME, PASSWORD)
        
        # 2. Capture DL Screenshot
        dl_path = await agent.capture_dl_screenshot(OUTPUT_DIR)
        
        # 3. Download Documents (ZIP)
        zip_path = await agent.download_documents(OUTPUT_DIR)
        
        doc_paths = {}
        if dl_path:
            doc_paths["DL"] = dl_path

        # 4. Unzip and Classify
        if zip_path and os.path.exists(zip_path):
            print(f"Unzipping {zip_path}...")
            extract_dir = os.path.join(OUTPUT_DIR, "extracted")
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
            os.makedirs(extract_dir)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print("Classifying extracted files...")
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    if file.startswith(".") or file.endswith(".DS_Store"): continue
                    
                    file_path = os.path.join(root, file)
                    
                    # Robust classification logic from test_extraction.py
                    if "BOS" in file:
                        doc_type = "BOS"
                    elif "BANK" in file:
                        doc_type = "BANK"
                    elif "OWNERSHIP" in file:
                        doc_type = "OWNERSHIP"
                    elif "LIEN" in file:
                        doc_type = "LIEN"
                    else:
                        doc_type = classify_document(file_path)
                    
                    print(f"Classified {file} as {doc_type}")
                    
                    if doc_type in ["BOS", "BANK", "OWNERSHIP", "LIEN"]:
                        doc_paths[doc_type] = file_path
                        # Rename for clarity (optional)
                        new_name = f"{doc_type}_{file}"
                        new_path = os.path.join(root, new_name)
                        os.rename(file_path, new_path)
                        doc_paths[doc_type] = new_path
        else:
            print("No ZIP file downloaded or found.")

        # Ensure DL screenshot from parent dir is included if not found in ZIP
        if "DL" not in doc_paths and dl_path and os.path.exists(dl_path):
             print(f"Using captured DL screenshot: {dl_path}")
             doc_paths["DL"] = dl_path

        # 5. Extraction (Parallel)
        print("Starting extraction...")
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
                    print(f"Extracted {doc_type}")
                except Exception as e:
                    print(f"Extraction failed for {doc_type}: {e}")
            
            # Print extracted data for review
            for doc_type, data in extracted_data.items():
                if data:
                    print(f"--- {doc_type} Data ---")
                    print(data.model_dump_json(indent=2))
                    print("---------------------")

        # 5. Verification
        print("Starting verification...")
        stock_id = generate_stock_id()
        
        # Construct FullCaseData
        case_data = FullCaseData(
            stock_id=stock_id,
            bos=extracted_data.get("BOS"),
            dl=extracted_data.get("DL"),
            banking=extracted_data.get("BANK"),
            ownership=extracted_data.get("OWNERSHIP"),
            lien=extracted_data.get("LIEN")
        )
        
        # Run verification logic
        verified_case = verify_case(case_data)
        
        # Generate Note Message
        results_summary = []
        for res in verified_case.verification_results:
            # Create a readable summary line
            status = res.validation_status or "Unknown"
            reason = res.validation_reasoning or "No reasoning provided"
            # We don't have document_type explicitly, but we can infer or just list them
            results_summary.append(f"Status: {status}\nReasoning: {reason}\n")
            
        note_message = f"Verification Results ({stock_id}):\n" + "\n".join(results_summary)
        print(f"Note to add:\n{note_message}")
        
        # 6. Add Notes to Portal
        print("Adding verification notes to portal...")
        
        # Mapping from Verification Type to UI Task Name
        task_mapping = {
            "DL-BOS": "Drivers License Verification",
            "BOS-BANK": "Void Cheque or Direct Deposit Form",
            "BOS-OWNERSHIP": "Proof of Ownership",
            "BOS-LIEN": "Lien Check"
        }

        for res in verified_case.verification_results:
            ver_type = res.verification_type
            task_name = task_mapping.get(ver_type)
            
            if task_name:
                status = res.validation_status or "Unknown"
                reason = res.validation_reasoning or "No reasoning provided"
                note_content = f"Status: {status}\nReasoning: {reason}"
                
                await agent.add_note_to_task(task_name, note_content)
            else:
                print(f"Skipping note for unknown verification type: {ver_type}")
        
        # 7. Save Dataset
        json_path, csv_path = save_dataset([verified_case], output_dir="datasets")
        print(f"Dataset saved to {json_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await agent.close()

if __name__ == "__main__":
    asyncio.run(main())
