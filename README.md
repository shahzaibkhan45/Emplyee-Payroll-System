# Rajby Textile Industries - Employee Payroll Management System

A full-stack, enterprise-grade Employee HR & Payroll Management System customized for the **Pakistani Textile & Denim Manufacturing Industry**, inspired by **Rajby Textiles / Rajby Industries, Karachi, Pakistan**.

Built with **HTML5, CSS3, Vanilla JavaScript, Python, Object-Oriented Programming (OOP), and Flask**.

> **Note:** This is an independent, customized payroll system tailored for Pakistani textile mill workflows (EOBI, SESSI, shifts, overtime, Pakistani CNIC, and PKR currency), inspired by industrial operations in Karachi.

---

## 🏭 Company Branding & Localization

- **Company Name:** Rajby Textile Industries
- **Industry:** Textile & Denim Manufacturing
- **Location:** Plot A/12, S.I.T.E. Industrial Area, Karachi - 75700, Pakistan
- **Currency:** Pakistani Rupee (**PKR**, Symbol: **Rs.**)
- **Timezone:** Asia/Karachi (PKT)
- **Date Format:** `DD-MM-YYYY`
- **Phone Format:** `+92 (XX) XXX-XXXX` or `+92 3XX XXXXXXX`
- **Working Schedule:** Monday - Saturday (Sunday weekly plant holiday)
- **Theme:** Corporate Navy Blue, Classic Denim Blue, Crisp White & Slate

---

## 🧵 The 18 Textile Manufacturing Departments

1. **Human Resources (HR)** - Compliance, talent acquisition, worker welfare & attendance
2. **Administration** - Mill facility management, plant vehicles, and civil infrastructure
3. **Production** - Core garment and denim assembly line management
4. **Cutting Department** - Computerized fabric spreading, CAD patterning, and laser cutting
5. **Stitching Department** - Progressive bundle sewing, flat-lock & denim chain stitching
6. **Washing & Laundry** - Industrial enzyme wash, stone wash, laser whiskering & eco-rinse
7. **Dyeing Department** - Indigo rope dyeing, slasher sizing, and reactive color chemistry
8. **Weaving Department** - High-speed airjet and projectile denim looms
9. **Finishing Department** - Garment pressing, sanforizing, labeling, and carton packing
10. **Quality Control (QC)** - Inline AQL 2.5 inspection, tensile tests, and metal detection
11. **Merchandising** - International denim buyer liaison, sampling, and order execution
12. **Industrial Engineering (IE)** - SMV time-motion studies, line balancing & ergonomics
13. **Maintenance** - Electromechanical, steam boiler, compressor, and generator upkeep
14. **Warehouse & Stores** - Raw cotton yarn, denim roll inventory, chemicals & trims
15. **Supply Chain** - Yarn procurement, customs clearing, and export container freight
16. **Finance & Accounts** - Cost accounting, payroll disbursements, and FBR/SRB tax filings
17. **Information Technology (IT)** - Mill ERP, biometric attendance punch devices & network
18. **Security** - Plant gate vigilance, CCTV monitoring, and factory perimeter security

---

## 👷 Pakistani Employee Profiles & CNIC Validation

- **Employee ID:** Auto-generated e.g. `RTI-1001`, `RTI-1002`, ...
- **Full Pakistani Identity:** Full Name, Father's / Husband's Name, Pakistani CNIC (`XXXXX-XXXXXXX-X`), Phone Number (`+92`), Official/Personal Email, Gender, DOB, Address, City (Karachi default), Emergency Contact.
- **Factory Shift System:**
  - **Morning Shift:** 06:00 AM - 02:00 PM (8 hrs)
  - **Evening Shift:** 02:00 PM - 10:00 PM (8 hrs)
  - **Night Shift:** 10:00 PM - 06:00 AM (8 hrs)
  - **General Office Shift:** 09:00 AM - 06:00 PM (9 hrs)
- **Employment Types:** Permanent, Contract, Daily Wage, Probation
- **Status:** Active, Inactive, On Leave, Terminated
- **Banking in Pakistan:** Meezan Bank, HBL, UBL, MCB, Bank Alfalah, Standard Chartered, NBP, etc., with Title and IBAN.
- **Strict Validations:** Unique CNIC (13 digits), unique Employee ID, unique Email, non-negative basic salary.

---

## ⏱️ Factory Attendance & Overtime Engine

- Biometric check-in and check-out tracking.
- Statuses: `Present`, `Absent`, `Half Day`, `Leave`, `Late Arrival`.
- Overtime Hours logging (e.g. 1.5 hrs, 2.0 hrs).
- **Duplicate Prevention:** Prohibits duplicate entries for the same employee on the same date.
- **Department-wise Attendance Audit:** Live headcount, present, absent, leaves, and overtime hours per textile department.

---

## 💰 Payroll & Pakistani Statutory Deductions

All calculations are executed in **Pakistani Rupees (PKR / Rs.)**:

### Earnings
- **Basic Salary**
- **House Rent Allowance (HRA)** (30% standard)
- **Medical Allowance** (10% standard)
- **Transport Allowance** (Rs. 5,000 - 8,000 industrial standard)
- **Other Industrial Allowances**
- **Plant Overtime Payment** ($\text{Overtime Hours} \times \text{Overtime Hourly Rate}$)
- **Attendance / Performance Bonus**

### Deductions
- **EOBI Contribution:** Employees' Old-Age Benefits Institution (Statutory Rs. 370 employee share)
- **SESSI Contribution:** Sindh Employees Social Security Institution
- **Income Tax Deduction:** Pakistani FBR Tax Slab estimation
- **Unpaid Leave Deduction:** Auto-computed based on monthly attendance records
- **Advance Salary Deduction**
- **Company Loan Deduction**
- **Other Deductions**

### Mathematical Formula
$$\text{Gross Salary} = \text{Basic Salary} + \text{Total Allowances} + \text{Overtime Payment} + \text{Bonus}$$
$$\text{Net Salary} = \text{Gross Salary} - \text{Total Deductions}$$

---

## 📄 Official Salary Slip (Payslip)

- Official Rajby Textile Industries letterhead with S.I.T.E. Karachi address.
- Employee ID, CNIC, Shift, Bank & Account Details.
- Itemized earnings (Basic, HRA, Medical, Transport, Overtime, Bonus) in PKR.
- Itemized deductions (EOBI, SESSI, Tax, Advance, Leave) in PKR.
- Highlighted Net Salary in PKR (Rs.).
- Dual signatures (Employee Signature & Head of HR/Accounts Signatory).
- Print to paper or export as clean PDF (`Ctrl+P`).

---

## 🛠️ Add Employee Modal Scrolling Bug Fix

- Correct modal viewport height limit (`max-height: calc(100vh - 40px)`).
- Anchored, fixed modal header and modal footer (`flex: 0 0 auto`).
- Form body is independently scrollable (`flex: 1 1 auto; overflow-y: auto; overflow-x: hidden; min-height: 0;`).
- Background page scroll is locked when modal is open (`overflow: hidden`).
- Tested across desktop, tablet, and mobile displays.

---

## 🚀 How to Run the Application

### 1. Requirements
- Python 3.10+
- Flask & Flask-CORS:
  ```bash
  pip install flask flask-cors
  ```

### 2. Start Server

**Option A (Recommended on Windows):**
Double-click `start.bat` in the project root.

**Option B (From Terminal / PowerShell):**
```powershell
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" run.py
```
*(Or `python run.py` if Python is added to your system PATH)*

### 3. Open in Browser
Visit:
```
http://127.0.0.1:5000/
```

### 4. Run Automated Test Suite
```powershell
& "C:\Users\DELL\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" backend/verify_endpoints.py
```
