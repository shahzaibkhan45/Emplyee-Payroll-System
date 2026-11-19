"""
Data Storage & In-Memory Initializer - Rajby Textile Industries, Karachi
Initializes Manager instances and seeds realistic Pakistani textile manufacturing data.
All records are stored as Python objects in memory lists with no database.
"""
from datetime import datetime, timedelta
from managers.department_manager import DepartmentManager
from managers.employee_manager import EmployeeManager
from managers.attendance_manager import AttendanceManager
from managers.payroll_manager import PayrollManager

# Global Manager Instances
department_manager = DepartmentManager()
employee_manager = EmployeeManager()
attendance_manager = AttendanceManager()
payroll_manager = PayrollManager()


def seed_data():
    """Seed comprehensive Pakistani textile manufacturing data into in-memory lists."""
    
    # 1. Seed All 18 Textile Manufacturing Departments
    textile_departments = [
        ("Human Resources (HR)", "Talent management, compliance, labor welfare, and payroll coordination."),
        ("Administration", "Plant administrative operations, transportation, and facility management."),
        ("Production", "Core garment and denim manufacturing, assembly lines, and output monitoring."),
        ("Cutting Department", "Automated fabric spreading, CAD patterning, and laser cutting."),
        ("Stitching Department", "Denim sewing, flat-lock assembly, and progressive bundle systems."),
        ("Washing & Laundry", "Garment enzyme washing, stone washing, laser whiskering, and eco-dry."),
        ("Dyeing Department", "Indigo rope dyeing, slasher dyeing, and reactive color processing."),
        ("Weaving Department", "High-speed airjet and projectile denim looms and fabric preparation."),
        ("Finishing Department", "Pressing, sanforizing, labeling, tag attachment, and final carton packing."),
        ("Quality Control (QC)", "AQL 2.5 inline quality audit, needle detection, and tensile testing."),
        ("Merchandising", "International denim buyer coordination, sampling, and order execution."),
        ("Industrial Engineering (IE)", "SMV time studies, line balancing, workstation ergonomics, and productivity."),
        ("Maintenance", "Preventive electromechanical maintenance, boiler operations, and compressor upkeep."),
        ("Warehouse & Stores", "Yarn, fabric roll inventory, trims, chemical storage, and SAP binning."),
        ("Supply Chain", "Raw material procurement, export logistics, and container shipments."),
        ("Finance & Accounts", "Cost accounting, tax compliance, bank payroll transfers, and statutory audits."),
        ("Information Technology (IT)", "ERP maintenance, biometric attendance devices, and mill network infrastructure."),
        ("Security", "CCTV gate monitoring, factory perimeter vigilance, and emergency evacuation drills.")
    ]

    for name, desc in textile_departments:
        department_manager.add_department(name=name, description=desc)

    # 2. Seed Realistic Pakistani Textile Mill Workforce (Karachi)
    pakistani_workforce = [
        {
            "full_name": "Muhammad Tariq",
            "father_name": "Muhammad Bashir",
            "cnic": "42101-1892345-1",
            "phone": "+92 300 2145890",
            "email": "m.tariq@rajby.local",
            "gender": "Male",
            "dob": "15-06-1983",
            "address": "House B-42, Block 4, Gulshan-e-Iqbal, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 321 9876543",
            "department": "Production",
            "designation": "Production Manager",
            "employee_type": "Permanent",
            "joining_date": "10-01-2018",
            "status": "Active",
            "shift": "General Office Shift",
            "basic_salary": 165000.0,
            "bank_name": "Meezan Bank Ltd",
            "account_title": "Muhammad Tariq",
            "account_number_iban": "PK36MEZN0001020304050601"
        },
        {
            "full_name": "Abdul Rehman",
            "father_name": "Haji Ghulam Qadir",
            "cnic": "42201-4567890-3",
            "phone": "+92 312 3456789",
            "email": "abdul.rehman@rajby.local",
            "gender": "Male",
            "dob": "22-09-1988",
            "address": "Sector 5-E, New Karachi, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 333 4567891",
            "department": "Stitching Department",
            "designation": "Line Incharge",
            "employee_type": "Permanent",
            "joining_date": "15-04-2020",
            "status": "Active",
            "shift": "Morning Shift",
            "basic_salary": 78000.0,
            "bank_name": "Habib Bank Limited (HBL)",
            "account_title": "Abdul Rehman",
            "account_number_iban": "PK54HABB0012345678901201"
        },
        {
            "full_name": "Shahzad Ahmed",
            "father_name": "Ahmed Din",
            "cnic": "42401-7890123-5",
            "phone": "+92 345 6789012",
            "email": "shahzad.ahmed@rajby.local",
            "gender": "Male",
            "dob": "12-03-1994",
            "address": "Plot 88, Sector 11-L, Orangi Town, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 301 2345678",
            "department": "Cutting Department",
            "designation": "Cutting Operator",
            "employee_type": "Permanent",
            "joining_date": "01-08-2021",
            "status": "Active",
            "shift": "Morning Shift",
            "basic_salary": 48000.0,
            "bank_name": "United Bank Limited (UBL)",
            "account_title": "Shahzad Ahmed",
            "account_number_iban": "PK22UNIL0098765432101201"
        },
        {
            "full_name": "Fatima Noor",
            "father_name": "Syed Noor-ul-Hassan",
            "cnic": "42301-3456781-4",
            "phone": "+92 334 1122334",
            "email": "fatima.noor@rajby.local",
            "gender": "Female",
            "dob": "18-11-1995",
            "address": "Apartment 304, Al-Ghafoor Heights, North Nazimabad, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 300 9988776",
            "department": "Human Resources (HR)",
            "designation": "HR Officer",
            "employee_type": "Permanent",
            "joining_date": "01-02-2022",
            "status": "Active",
            "shift": "General Office Shift",
            "basic_salary": 65000.0,
            "bank_name": "Bank Alfalah",
            "account_title": "Fatima Noor",
            "account_number_iban": "PK89ALFH0055443322110001"
        },
        {
            "full_name": "Bilal Khan",
            "father_name": "Akbar Khan",
            "cnic": "42101-9012345-7",
            "phone": "+92 321 8877665",
            "email": "bilal.khan@rajby.local",
            "gender": "Male",
            "dob": "05-04-1986",
            "address": "House 12, Area 36-B, Landhi Industrial Area, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 313 7788990",
            "department": "Dyeing Department",
            "designation": "Dyeing Master",
            "employee_type": "Permanent",
            "joining_date": "15-06-2019",
            "status": "Active",
            "shift": "Morning Shift",
            "basic_salary": 95000.0,
            "bank_name": "Meezan Bank Ltd",
            "account_title": "Bilal Khan",
            "account_number_iban": "PK36MEZN0011223344556602"
        },
        {
            "full_name": "Muhammad Naveed",
            "father_name": "Muhammad Sharif",
            "cnic": "42501-5678901-9",
            "phone": "+92 306 5544332",
            "email": "m.naveed@rajby.local",
            "gender": "Male",
            "dob": "10-10-1996",
            "address": "Street 9, Bilal Colony, Korangi, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 344 6655443",
            "department": "Washing & Laundry",
            "designation": "Washing Operator",
            "employee_type": "Permanent",
            "joining_date": "10-11-2021",
            "status": "Active",
            "shift": "Evening Shift",
            "basic_salary": 44000.0,
            "bank_name": "MCB Bank Ltd",
            "account_title": "Muhammad Naveed",
            "account_number_iban": "PK78MUCB0077889900112201"
        },
        {
            "full_name": "Ayesha Siddiqui",
            "father_name": "Tariq Siddiqui",
            "cnic": "42201-6789012-6",
            "phone": "+92 302 9900112",
            "email": "ayesha.s@rajby.local",
            "gender": "Female",
            "dob": "25-08-1992",
            "address": "B-15, PECHS Block 2, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 331 4455667",
            "department": "Merchandising",
            "designation": "Senior Merchandiser",
            "employee_type": "Permanent",
            "joining_date": "01-09-2020",
            "status": "Active",
            "shift": "General Office Shift",
            "basic_salary": 115000.0,
            "bank_name": "Standard Chartered Bank",
            "account_title": "Ayesha Siddiqui",
            "account_number_iban": "PK90SCBL0000112233445501"
        },
        {
            "full_name": "Syed Farhan Ali",
            "father_name": "Syed Asghar Ali",
            "cnic": "42101-2345678-3",
            "phone": "+92 315 7766554",
            "email": "farhan.ali@rajby.local",
            "gender": "Male",
            "dob": "14-02-1993",
            "address": "Flat D-12, Erum Garden, Gulshan-e-Maymar, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 308 3322110",
            "department": "Quality Control (QC)",
            "designation": "Quality Inspector",
            "employee_type": "Permanent",
            "joining_date": "15-03-2022",
            "status": "Active",
            "shift": "Morning Shift",
            "basic_salary": 54000.0,
            "bank_name": "Habib Bank Limited (HBL)",
            "account_title": "Syed Farhan Ali",
            "account_number_iban": "PK54HABB0099887766554402"
        },
        {
            "full_name": "Imran Baig",
            "father_name": "Mirza Anwar Baig",
            "cnic": "42301-8901234-5",
            "phone": "+92 333 8899001",
            "email": "imran.baig@rajby.local",
            "gender": "Male",
            "dob": "30-07-1989",
            "address": "Quarter 15, Federal B Area, Block 14, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 322 1122445",
            "department": "Maintenance",
            "designation": "Maintenance Technician",
            "employee_type": "Permanent",
            "joining_date": "05-01-2021",
            "status": "Active",
            "shift": "Night Shift",
            "basic_salary": 58000.0,
            "bank_name": "Meezan Bank Ltd",
            "account_title": "Imran Baig",
            "account_number_iban": "PK36MEZN0066778899001103"
        },
        {
            "full_name": "Zeeshan Qureshi",
            "father_name": "Abdul Latif Qureshi",
            "cnic": "42401-6789123-1",
            "phone": "+92 346 2233445",
            "email": "zeeshan.q@rajby.local",
            "gender": "Male",
            "dob": "08-12-1997",
            "address": "House 45, Sector 4, Baldia Town, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 311 9988776",
            "department": "Warehouse & Stores",
            "designation": "Store Keeper",
            "employee_type": "Permanent",
            "joining_date": "20-05-2023",
            "status": "Active",
            "shift": "Morning Shift",
            "basic_salary": 45000.0,
            "bank_name": "Bank Alfalah",
            "account_title": "Zeeshan Qureshi",
            "account_number_iban": "PK89ALFH0011335577990002"
        },
        {
            "full_name": "Asif Mehmood",
            "father_name": "Mehmood Ul Hassan",
            "cnic": "42201-1234567-9",
            "phone": "+92 300 8234567",
            "email": "asif.m@rajby.local",
            "gender": "Male",
            "dob": "04-05-1987",
            "address": "Flat 201, Al-Noor Plaza, Bahadurabad, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 321 7766554",
            "department": "Finance & Accounts",
            "designation": "Senior Accountant",
            "employee_type": "Permanent",
            "joining_date": "10-10-2019",
            "status": "Active",
            "shift": "General Office Shift",
            "basic_salary": 92000.0,
            "bank_name": "Habib Metropolitan Bank",
            "account_title": "Asif Mehmood",
            "account_number_iban": "PK45HMBB0012341234123401"
        },
        {
            "full_name": "Ghulam Mustafa",
            "father_name": "Allah Ditta",
            "cnic": "42501-7890123-7",
            "phone": "+92 332 5566778",
            "email": "ghulam.m@rajby.local",
            "gender": "Male",
            "dob": "19-01-1985",
            "address": "House 114, Model Colony, Malir, Karachi",
            "city": "Karachi",
            "emergency_contact": "+92 305 4433221",
            "department": "Security",
            "designation": "Security Guard",
            "employee_type": "Contract",
            "joining_date": "01-01-2023",
            "status": "Active",
            "shift": "Morning Shift",
            "basic_salary": 38000.0,
            "bank_name": "National Bank of Pakistan (NBP)",
            "account_title": "Ghulam Mustafa",
            "account_number_iban": "PK12NBPA0009876543210001"
        }
    ]

    for emp_data in pakistani_workforce:
        employee_manager.add_employee(emp_data, department_manager)

    # 3. Seed Realistic Multi-day Attendance with Biometric Check-in/out & Overtime
    today = datetime.now()
    all_emps = employee_manager.employees

    # For the last 5 days (excluding Sundays)
    for day_offset in range(5, -1, -1):
        target_dt = today - timedelta(days=day_offset)
        if target_dt.weekday() == 6:  # Sunday weekly off
            continue
        date_str = target_dt.strftime("%Y-%m-%d")

        for idx, emp in enumerate(all_emps):
            # Realistic status distribution
            ot = 0.0
            check_in = "07:55 AM"
            check_out = "05:00 PM"

            if emp.shift == "Morning Shift":
                check_in = "05:50 AM"
                check_out = "02:15 PM"
            elif emp.shift == "Evening Shift":
                check_in = "01:50 PM"
                check_out = "10:10 PM"
            elif emp.shift == "Night Shift":
                check_in = "09:50 PM"
                check_out = "06:10 AM"

            if idx == 2 and day_offset == 1:
                status = "Leave"
                check_in = "-"
                check_out = "-"
                remarks = "Approved medical leave"
            elif idx == 4 and day_offset == 2:
                status = "Half Day"
                check_out = "01:00 PM"
                remarks = "Urgent family matter"
            elif idx == 8 and day_offset == 0:
                status = "Late Arrival"
                check_in = "08:45 AM"
                remarks = "Karachi traffic delay"
            elif idx == 5 and day_offset == 3:
                status = "Absent"
                check_in = "-"
                check_out = "-"
                remarks = "Uninformed absence"
            else:
                status = "Present"
                # Production, Cutting & Stitching operators frequently do 2 hrs overtime
                if emp.department in ["Cutting Department", "Stitching Department", "Production", "Washing & Laundry"]:
                    ot = 2.0 if day_offset % 2 == 0 else 1.5
                    check_out = "07:05 PM" if emp.shift == "General Office Shift" else "04:15 PM"
                remarks = "Biometric punch verified"

            try:
                attendance_manager.mark_attendance(
                    employee_id=emp.employee_id,
                    date=date_str,
                    status=status,
                    check_in=check_in,
                    check_out=check_out,
                    overtime_hours=ot,
                    shift=emp.shift,
                    remarks=remarks,
                    employee_manager=employee_manager
                )
            except ValueError:
                pass

    # 4. Seed Monthly Payroll Records in PKR for October 2026 and November 2026
    current_month = today.strftime("%Y-%m")
    prev_month_dt = today.replace(day=1) - timedelta(days=1)
    previous_month = prev_month_dt.strftime("%Y-%m")

    # October 2026 Payroll for all staff
    for emp in all_emps:
        try:
            suggested = payroll_manager.calculate_suggested_components(
                emp, previous_month, attendance_manager
            )
            suggested["payment_status"] = "Paid"
            suggested["payment_date"] = f"28-10-2026"
            suggested["bonus"] = 15000.0 if "Manager" in emp.designation else (5000.0 if "Officer" in emp.designation else 2500.0)
            payroll_manager.generate_payroll(
                emp.employee_id, previous_month, suggested, employee_manager, attendance_manager
            )
        except ValueError:
            pass

    # November 2026 Payroll for subset (with Approved and Paid statuses)
    for idx, emp in enumerate(all_emps[:6]):
        try:
            suggested = payroll_manager.calculate_suggested_components(
                emp, current_month, attendance_manager
            )
            suggested["payment_status"] = "Paid" if idx < 4 else "Approved"
            suggested["payment_date"] = today.strftime("%d-%m-%Y")
            suggested["bonus"] = 5000.0
            payroll_manager.generate_payroll(
                emp.employee_id, current_month, suggested, employee_manager, attendance_manager
            )
        except ValueError:
            pass


# Execute seed
seed_data()
