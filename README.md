# Clutch Document Verification Automation

This project automates the end-to-end process of verifying vehicle purchase documents for Clutch. It logs into the admin portal, downloads relevant documents (Bill of Sale, Driver's License, Banking, Ownership, Lien), extracts data using Gemini 2.5 AI, performs cross-document validation, and posts verification notes back to the portal.

## Features

*   **Automated Browser Navigation**: Logs into the Clutch admin portal and navigates to the specific task page.
*   **Document Retrieval**: Captures screenshots of the Driver's License and downloads all other documents as a ZIP file.
*   **Intelligent Extraction**: Uses Google's Gemini 2.5 Flash model to extract structured data from PDF and image files.
*   **Cross-Document Verification**: Validates data consistency across documents:
    *   **DL vs. BOS**: Name matching, ID expiration, valid ID type.
    *   **BOS vs. BANK**: Name matching, account type (Chequing), account structure.
    *   **BOS vs. OWNERSHIP**: VIN matching, ownership duration (>60 days), vehicle make/model match.
    *   **BOS vs. LIEN**: VIN matching, lien status/amount reconciliation.
*   **Automated Reporting**: Posts detailed "PASS/FAIL" notes with reasoning directly to the corresponding line items in the admin portal.

## Prerequisites

*   Python 3.9+
*   A Google Cloud Project with the **Gemini API** enabled.
*   Valid credentials for the Clutch admin portal.

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers**:
    ```bash
    playwright install chromium
    ```

## Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## Usage

To run the full end-to-end workflow:

```bash
python3 main.py
```

### What happens when you run it:

1.  **Login**: The script launches a browser (visible mode), logs into the portal, and navigates to the target task.
2.  **Capture**: It opens the Driver's License preview and takes a screenshot.
3.  **Download**: It downloads the "STC Task Documents" ZIP file.
4.  **Extract**: It unzips the files and uses Gemini to extract data from each document (BOS, DL, Bank, Ownership, Lien).
5.  **Verify**: It runs the validation logic defined in `verification.py`.
6.  **Report**: It navigates back to the portal and adds a note to each relevant task line (e.g., "Drivers License Verification", "Proof of Ownership") with the validation status and reasoning.
7.  **Save**: A JSON record of the verification is saved to the `datasets/` directory.

## Project Structure

*   `main.py`: The main orchestrator script.
*   `browser.py`: Handles all Playwright browser interactions (login, download, posting notes).
*   `extraction.py`: Manages communication with the Gemini API for document data extraction.
*   `verification.py`: Contains the logic and rules for cross-document validation.
*   `data_model.py`: Pydantic models defining the structure of extracted data and verification results.
*   `utils.py`: Helper functions for ID generation and file saving.
*   `test_extraction.py`: A utility script to test extraction/verification on local files without running the browser automation.
