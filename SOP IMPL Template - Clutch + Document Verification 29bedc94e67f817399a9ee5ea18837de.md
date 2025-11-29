# SOP IMPL Template - Clutch + Document Verification Automation

AST: Apoorva Gupta, Vignesh Narayanan
FDE/SE: Sujal Jaiswal

AST team to populate the following template and hand-off to FDEs so they can effectively and quickly execute delivery. This information is already provided by AST teams to FDEs in Slack customer squad groups and daily syncs during delivery. 

The aim of this template and hand-off process is to ensure we 

1. Increase customer delivery speed without a lot of back & forth and coordination cost
2. Ensure delivery SLAs are not affected even if FDE, SE or ASM switch
3. Centralised documentation of business context and requirements of all processes as we scale to 1000s of processes

Reference images for information available for guidance. 

## SOP document attachment - AST

*(Please upload SOP document here)*

[Complete SOP Document](https://docs.google.com/document/d/1xI41znO-Cw8-6gUWd2JrBrsJoo43nmwn2ZtNjW23FDc/edit?usp=sharing)

[OCR Phase SOP Document](https://docs.google.com/document/d/1QS2DlENW13btqxY5D_0dk9Esxd7-vx_enelpv-EHO7Y/edit?usp=sharing)

## High-level Workflow Chart - AST

*(Please input SOP document to Claude and attach output xml file or flowchart diagram)*

[diagram-export-30-10-2025-15_04_37.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/diagram-export-30-10-2025-15_04_37.png)

## Prompt flow chart - AST (critical)

Each step in the below flow to be sequential. If to be executed parallely, mention 2a, 2b, 2c..

| **Step #** | **Prompt name** | **Called by** | **Objective** | **Input Variables : Type** | **Output Variables : Type** |
| --- | --- | --- | --- | --- | --- |
| 1 |  | Code/Prompt |  |  |  |
| 2 |  | Code/Prompt |  |  |  |

## External System Dependencies *(if applicable)* - AST

*(Please tick when done and whichever applicable)*

- [x]  Option 1: API credentials and documentation - add details below

We have received System Access to the Clutch Sandbox Environment for testing.  
Staging Access credentials are given below:

URL: [https://admin.staging.clutchenv.ca/](https://admin.staging.clutchenv.ca/)

Email: [benjamin.koppeser+guest@clutch.ca](mailto:benjamin.koppeser%2Bguest@clutch.ca)

PW: Zamp123!

- [ ]  If not, feasibility check with FDE on reverse engineering APIs - add comments below

- [ ]  If not, feasibility check with product / eng on workarounds / browser agent - add comments below

## Access to existing Pace organization - AST

- [x]  If organization exists, please add FDE to existing org on Pace dashboard
- [ ]  NA - new organization

## New Org and Process Name - AST

- Organisation name = Clutch
- Process name = Document Verification

## What data needs to be captured - AST (critical)

*(What exhaustive data - tables and columns need to be captured by Pace for the process to run effectively. This includes input source, intermediate processed and output data)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21) and [here](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21)

### Dataset Details:

| {Table name} | {column 1} | {column 2} | {column 3} | {column 4} | {column 5} | {column 6} | {column 7} | {column 8} | {column 9} |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Bill of Sale (BOS) | stock_id (String) | customer_first_name (String) | customer_last_name (String) | customer_full_name (String) | vehicle_year (Integer) | vehicle_make (String) | vehicle_model (String) | vehicle_vin (Alphanumeric) | vehicle_vin_last6 (Alphanumeric) | bos_effective_date (Date) | selling_price (Decimal) | additions_dropoff_tomorrow (Decimal) | additions_partnership_discount (Decimal) | applicable_loan_balance (Decimal) | deductions (Decimal) | adjustment_sbs (Decimal) | net_vehicle_value (Decimal) |  |
| 2. Driver’s License | id_first_name (String) | id_last_name (String) | id_full_name (String) | id_expiry_date (Date) | id_number (String) | id_issue_date (Date) | id_type (Enum: DriverLicense/Passport/PRCard/CitizenshipCard/MilitaryID/OntarioPhotoID) | temporary_id_provided (Y/N) | temporary_id_type (String) | temporary_id_expiry_date (Date) |  |  |  |  |  |  |  |  |
| 3. Banking Document | bank_account_holder_name (String) | bank_institution_number (Integer) | bank_transit_number (Integer) | bank_account_number (Integer) | bank_account_type (Enum: Chequing/Savings) | bank_name (String) |  |  |  |  |  |  |  |  |  |  |  |  |
| 4. Vehicle Ownership | ownership_first_name (String) | ownership_last_name (String) | ownership_full_name (String) | ownership_vin (Alphanumeric) | ownership_vin_last6 (Alphanumeric) | ownership_year (Integer/String) | ownership_make (String) | ownership_model (String) | ownership_registration_date (Date) | province (String) |  |  |  |  |  |  |  |  |
| 5. Lien Check Report | lien_status (Enum: Active/Discharged/None) | lien_vin (Alphanumeric) | lender_name (String) | lien_amount (Decimal) | lien_per_diem (Decimal) |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6. Lien Buyout Letter | lien_debtor_name (String) | lien_vin (Alphanumeric) | lien_vehicle_year (Integer) | lien_vehicle_make (String) | lien_vehicle_model (String) | lien_outstanding_amount (Decimal) | lien_valid_until_date (Date) | lender_name (String) |  |  |  |  |  |  |  |  |  |  |
| 7. Lease Release Letter | lease_lessee_name (String) | lease_vin (Alphanumeric) | lease_vehicle_year (Integer) | lease_vehicle_make (String) | lease_vehicle_model (String) | lease_discharge_status (String) | lease_discharge_date (Date) | lease_buyout_amount (Decimal) |  |  |  |  |  |  |  |  |  |  |
- Decide whether the table should be hidden or visible on dashboard
1. Bill of Sale (BOS)
    - Visible
2. Driver's License
    - Hidden
3. Banking Document
    - Hidden
4. Vehicle Ownership
    - Hidden
5. Lien Check Report
    - Hidden
6. Lien Buyout Letter
    - Hidden
7. Lease Release Letter
    - Hidden

- Which fields or columns above should be hidden on the dashboard (but needed for Pace)
    - `vehicle_vin_last6` — used for VIN match shorthand
    - `applicable_loan_balance` — needed for lien reconciliation
    - `adjustment_sbs` — used for net value computation logic
    - `deductions` — needed to compute `net_vehicle_value`
    - `additions_dropoff_tomorrow`
    - `additions_partnership_discount`
    - `selling_price`

- Which fields or columns above are mandatory to be captured and which are optional
    
    
    **Core Identity & Name**
    
    - `customer_full_name` / `id_full_name` / `bank_account_holder_name` / `ownership_full_name` / `lease_lessee_name` / `lien_debtor_name`
    
    **Vehicle Identification**
    
    ---
    
    - `vehicle_vin` / `ownership_vin` / `lien_vin` / `lease_vin`
    - `vehicle_vin_last6` / `ownership_vin_last6`
    - `vehicle_make` / `ownership_make` / `lien_vehicle_make` / `lease_vehicle_make`
    - `vehicle_model` / `ownership_model` / `lien_vehicle_model` / `lease_vehicle_model`
    - `vehicle_year` / `ownership_year` / `lien_vehicle_year` / `lease_vehicle_year`
    
    **Date-Based Validations**
    
    ---
    
    - `bos_effective_date`
    - `id_expiry_date`
    - `ownership_registration_date`
    - `lien_valid_until_date`
    - `lease_discharge_date`
    
    **Financial Validation**
    
    ---
    
    - `selling_price`
    - `applicable_loan_balance` / `lien_outstanding_amount`
    - `net_vehicle_value`
    - `lease_buyout_amount` (for lease validation)
    
    **Verification/Classification Fields**
    
    ---
    
    - `id_type` (to validate alternate ID rules)
    - `bank_account_type` (must be Chequing)
    - `lien_status` (Active/Discharged/None)
    - `lease_discharge_status` (must be Paid in Full/Equivalent)
    - `province` (for ownership rule logic)
    
    **In summary, Pace *must* extract at least these to process end-to-end:**
    
    ---
    
    - **Identity linkage:** `customer_full_name` / `id_full_name`
    - **Vehicle linkage:** `vehicle_vin`, `vehicle_make`, `vehicle_model`, `vehicle_year`
    - **Ownership linkage:** `ownership_vin`, `ownership_registration_date`, `province`
    - **Financial linkage:** `selling_price`, `applicable_loan_balance`, `net_vehicle_value`
    - **Temporal checks:** `bos_effective_date`, `id_expiry_date`, `lien_valid_until_date`
    - **Type checks:** `id_type`, `bank_account_type`, `lien_status`, `lease_discharge_status`

<aside>
🛑

Check-point: Once the FDE completes datasets and process creation, FDE should provide the input and expected output (golden-dataset) schema for AST team to create and run evals on Langfuse via Windmill Scripts ([Reference](https://www.notion.so/Building-AI-Agents-From-Process-to-Prompt-23bedc94e67f804ba452d4d0b06089fe?pvs=21) and [Reference Video](https://app.avoma.com/meetings/4fddee2f-0bfc-4722-9d87-1e3de0ac6ca7)) 

</aside>

## What gets shown on dashboard - AST (critical)

### Process Activity Run States

*(For the process, what are exhaustive states that runs will go through - for eg: Needs Attention, In-Progress, Done, Void)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21)

- [x]  In progress
- [x]  Needs Attention
- [x]  Completed
- [x]  Void

### Process Activity Run State Change logic: check-in

- [x]  Quick check-in: Ensure the logic of when an item moves from one state to the other is mece detailed out in SOP document for workflow logic to be comprehensive (For eg: when all is an item supposed to be in progress, when all is an item supposed to be Void, when all is an item supposed to be in Needs Attention bucket, when all is an item supposed to be in Done bucket)

### Process View Table

*(On the process page, what columns should the customer see. This will be a sub-set of the [Datasets](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21) captured above. This will be 1 table only. Add as many columns as required to show to the customer)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21)

| Process View Datasets | Status | {column 2} | {column 3} | … |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bill of Sale (BOS) | customer_full_name (String) | vehicle_year (Integer) | vehicle_make (String) | vehicle_model (String) | vehicle_vin (Alphanumeric) | bos_effective_date (Date) | selling_price (Decimal) | applicable_loan_balance (Decimal) | net_vehicle_value (Decimal) |  |
|  |  |  |  |  |  |  |  |  |  |  |

### Process View run headers

*(When you click on a single run, what should the title and value of each run be named)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21)

- Header Name = Stock ID
- Header Value = {{stock ID}}

### Process View Key Details

*(When you click on a single run, what dataset values do you want the customer to see specific to the run. You can have multiple tables added here)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21)

### **Key Details Table 1: Bill of Sale Summary**

- **Customer Name:** `{customer_full_name}`
- **Vehicle:** `{vehicle_year} {vehicle_make} {vehicle_model}`
- **BOS Effective Date:** `{bos_effective_date}`
- **Applicable Loan / Lien Amount:** `${applicable_loan_balance}`
- **Net Vehicle Value:** `${net_vehicle_value}`

### Process View Artefacts

*(When you click on a single run, what artefacts do you want the customer to see.* The same artefacts are referenced with logs*)*

Where this goes: Check [here](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21)

| Artefact of | Type (pdf, email, pdf-datasets, link etc.) | Artefact Display Name |
| --- | --- | --- |
| Bill of Sale (Primary) | pdf | Bill_of_Sale_<stockID>.pdf |
| Driver’s License (Owner) | image/pdf | Owner_ID_<stockID>.pdf |
| Driver’s License (Co-Owner) | image/pdf | Co_Owner_ID_<stockID>.pdf |
| Banking Document | pdf | Direct_Deposit_Form_<stockID>.pdf |
| Vehicle Ownership | pdf | Ownership_Document_<stockID>.pdf |
| Lien Buyout Letter / Report | pdf | Lien_Document_<stockID>.pdf |
| Lease Release / Buyout Letter | pdf | Lease_Document_<stockID>.pdf |

### Process View Log Groups Master <> Activity Run State

*(When you click on a single run, what log group or activity progress should be shown to the customer when a) the step begins b) when it is completed c) when it fails due to an error d) when it needs HITL, what log groups need to have See Reasoning steps by CoT agent, what artefacts need to be referenced for each log group. Typically each log group or activity is a job-to-be-done. If a particular activity requires Needs Attention (or HITL) by user, what actions should Pace ask the user to complete - MCQ / field entry etc. and whether communication should happen on Slack or dashboard only. Please detail exhaustive log group steps here and what activity state change they represent corresponding to the specific log status)*

Check [here](https://www.notion.so/SOP-IMPL-Template-Clutch-Document-Verification-Automation-29bedc94e67f817399a9ee5ea18837de?pvs=21)

| Sr # | Log Group Overview | Log Group Initiated State Messaging  | Log Group Success State Messaging | Log Group Failed State Messaging  | Log Group Needs Attention State Messaging (if relevant) | Activity Run State Change Mapping (does any log group state need changing activity run status) | See Reasoning or Thought Steps within group - Messaging during CoT agentic activities | Artefacts or CTAs Referenced | Needs Attention -  Action by user | HITL communication on dashboard / Slack / email? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Document Intake & Screenshot Capture | “Started fetching task and capturing screenshots for Bill of Sale, ID, Banking, and Ownership documents.” | “All required documents captured and tagged successfully.” | “Document fetch failed — missing or inaccessible files.” | “One or more document screenshots missing. Please upload manually.” | Moves Activity Run → In Progress | “Pace verifying available documents before initiating OCR.” | Screenshot batch artefacts (Batch_<stockID>.zip) | Upload missing document(s) / verify upload integrity | Dashboard |
| 2 | OCR Extraction & Dataset Population | “OCR extraction initiated on all captured documents.” | “OCR completed successfully — all key fields extracted.” | “OCR failed due to low image quality or unreadable text.” | “OCR extracted partial data. Please review highlighted fields.” | Remains In Progress | “Pace CoT reasoning extracting fields using layout + text patterns.” | Dataset sheets (BOS.csv, ID.csv, Bank.csv etc.) | Manually enter or correct unread OCR fields | Dashboard |
| 3 | Bill of Sale (BOS) Verification | “Validating Bill of Sale fields and computing net vehicle value.” | “Bill of Sale verification complete — all values consistent.” | “BOS verification failed — missing or invalid field values.” | “BOS mismatch detected in Vehicle Value or VIN. Please confirm values.” | Remains In Progress | “Pace CoT reasoning on calculation consistency (Selling + Adjustments = Net).” | Bill_of_Sale_<stockID>.pdf, Validation_Matrix.pdf | Confirm or edit BOS value fields | Dashboard |
| 4 | Identity Verification (Driver’s License) | “Starting ID verification — matching customer name and expiry validity.” | “Identity verified successfully — full name and expiry date valid.” | “ID verification failed — name or expiry invalid.” | “Name mismatch / expired ID detected. Please confirm or upload alternative ID.” | Moves Activity Run → Needs Attention | “Pace CoT comparing parsed OCR name tokens with BOS fields.” | Driver_ID_<stockID>.pdf | Upload alternate ID / confirm name override | Dashboard + Slack |
| 5 | Banking Information Verification | “Validating bank details for payment release.” | “Banking information verified — account format and name match valid.” | “Bank validation failed — account invalid or mismatched name.” | “Non-chequing account detected or format invalid. Please confirm.” | Remains In Progress | “Pace CoT reasoning across institution number + name mapping.” | Direct_Deposit_Form_<stockID>.pdf | Confirm banking info or re-upload correct form | Dashboard |
| 6 | Vehicle Ownership Verification | “Validating ownership document against Bill of Sale details.” | “Ownership verified — VIN, make, and year match confirmed.” | “Ownership validation failed — VIN mismatch or registration invalid.” | “Ownership date <60 days or VIN mismatch detected. Please confirm.” | Remains In Progress | “Pace CoT verifying last-6 VIN and effective date compliance.” | Ownership_Document_<stockID>.pdf | Confirm ownership date or upload updated registration | Dashboard |
| 7 | Lien Documentation Verification (If Applicable) | “Checking lien status and lender details.” | “Lien validated — discharge letter verified or balance matched.” | “Lien verification failed — invalid amount or missing discharge.” | “Lien record mismatch — please confirm lender or upload new letter.” | Moves Activity Run → Needs Attention | “Pace CoT matching lien amount and VIN across lender templates.” | Lien_Document_<stockID>.pdf, Carfax_Report.pdf | Upload discharge proof / verify amount | Dashboard + Slack |
| 8 | Lease Documentation Verification (If Applicable) | “Verifying lease release or buyout documentation.” | “Lease verification successful — discharge confirmed.” | “Lease verification failed — invalid discharge or mismatch.” | “Lease incomplete or missing signatures. Please confirm with lender.” | Remains In Progress | “Pace CoT reasoning over text patterns for ‘paid in full’ status.” | Lease_Document_<stockID>.pdf | Confirm discharge / upload signed letter | Dashboard |

Cross Document Validation Matrix

| **Validation Area** | **Primary Source (Golden Record)** | **Secondary Source(s)** | **Condition / Rule** | **Exception / Special Handling** |
| --- | --- | --- | --- | --- |
| **1. Customer Name Consistency (Main Owner)** | BOS → `customer_full_name` | Driver’s License → `id_full_name` | Exact match (case-insensitive, ignore punctuation) | Reject abbreviations (e.g., “A.” ≠ “ARMAN”). For alternate ID: ensure DoB and name consistency. |
| **2. Co-owner (if applicable)** | BOS (co-owner if listed) | Secondary License (optional dataset) | Exact match | Same rules as above. |
| **3. Banking Name Match** | BOS → `customer_full_name` | Banking → `bank_account_holder_name` | Exact match | Reject if mismatch or joint account name not matching BOS. |
| **4. VIN Match (Vehicle Identity)** | BOS → `vehicle_vin_last6` / `vehicle_vin` | Ownership → `ownership_vin_last6` / `ownership_vin`Lien Buyout → `lien_vin`Lease Release → `lease_vin` | Full or last-6 VIN must match exactly across all | Flag mismatch even if 1-digit difference. Accept truncated VIN only if prefix known missing from form. |
| **5. Vehicle Make/Model/Year Consistency** | BOS → `vehicle_make`, `vehicle_model`, `vehicle_year` | Ownership, Lien, Lease datasets | Exact text match (ignore casing) | If minor abbreviation difference (“VW” = “Volkswagen”), normalize via lookup map. |
| **6. ID Expiry Logic** | BOS → `bos_effective_date` | Driver’s License → `id_expiry_date` | ID expiry ≥ BOS date OR within 30-day grace window | Accept alternative ID if driver’s license expired ≤30 days. Flag if >30 days. |
| **7. Bank Account Validation** | N/A | Banking → `bank_institution_number`, `bank_transit_number`, `bank_account_number`, `bank_account_type` | Validate structure: 3-5-7/12 digit pattern; `bank_account_type` = Chequing | Reject Savings accounts or invalid digit lengths. |
| **8. Ownership Duration** | BOS → `bos_effective_date` | Ownership → `ownership_registration_date` | Registration ≤ (BOS − 60 days) | If <60 days, require supporting docs (insurance/BOS ≥ 60 days old). |
| **9. Lien Validation** | BOS → `vehicle_vin` | Lien Check → `lien_status`, `lien_vin`Lien Buyout → `lien_outstanding_amount`, `lien_valid_until_date` | VIN match, lien amount valid (numeric), letter date ≤ 7 days old | Flag missing lender logo or expired validity. Accept Carfax “Discharged” if amount = 0. |
| **10. Lien Amount Reconciliation** | BOS → `applicable_loan_balance` | Lien Buyout → `lien_outstanding_amount` | Values should be equal ± $100 tolerance | Accept small rounding variance; flag if larger. |
| **11. Lease Validation** | BOS → `vehicle_vin` | Lease → `lease_vin`, `lease_discharge_status` | VIN must match; discharge = “Paid in Full” or equivalent | Flag incomplete or missing discharge letter. |
| **12. Financial Consistency** | BOS → `selling_price`, `adjustment_sbs`, `applicable_loan_balance`, `net_vehicle_value` | Derived check | `net_vehicle_value = (selling_price + additions - deductions ± adjustments)` | Ensure OCRed amounts compute correctly; round to 2 decimals. |
| **13. Province Logic (Ownership)** | N/A | Ownership → `province` | Must match one of accepted provinces; validate format | Apply province-specific ownership validation (BC can be electronic, ON must be original). |
| **14. Document Presence** | BOS mandatory | All secondary docs | All required documents must exist based on stock type | If missing: flag “Incomplete Set.” |
| **15. Overall Task Status** | — | — | If all validations pass → Mark Complete; else → Needs Attention | Generate JSON exception log listing field-level failures. |

## Email trigger set-up hygiene - AST

*(If email is the primary trigger for the process, please coordinate with @Yashikha Jain to set-up emails for dev and prod environments separately)*

- [ ]  Done

---

## Change Log - FDE / AST

*(FDE / AST to list down all changes that’s happened to track scope creep)*

| Change Topic | Change Description | Time-stamp |
| --- | --- | --- |
|  |  |  |
|  |  |  |

---

## User, Org, Dataset, Process IDs - FDE

*(FDEs to enter all relevant ids for the org, datasets and process which need frequent referencing)*

| Type | Description | ID |
| --- | --- | --- |
|  |  |  |
|  |  |  |

---

## SOP IMPL Reference Images

- Data tables
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image.png)
    
- Data table columns
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%201.png)
    
- Process State Groups
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%202.png)
    
- Process View Table
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%203.png)
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%204.png)
    
- Process View run-wise Header Name and Value Details
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%205.png)
    
- Process View run Key Details
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%206.png)
    
- Process View Artefacts
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%207.png)
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%208.png)
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%209.png)
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%2010.png)
    
- Process View Logs - Logs Master
    
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%2011.png)
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%2012.png)
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%2013.png)
    
    ![image.png](SOP%20IMPL%20Template%20-%20Clutch%20+%20Document%20Verification/image%2014.png)