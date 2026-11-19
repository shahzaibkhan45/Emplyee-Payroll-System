"""
Comprehensive Verification Script - Rajby Textile Industries
Tests all Flask endpoints, frontend HTML delivery, and Pakistani textile payroll logic.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

client = app.test_client()

def test_all():
    print("==================================================================")
    print(" Testing Rajby Textile Industries HR & Payroll System")
    print("==================================================================")

    print("\n1. Testing Frontend HTML Pages...")
    for path in ["/", "/employees", "/departments", "/attendance", "/payroll", "/salary-slip"]:
        res = client.get(path)
        assert res.status_code == 200, f"Failed GET {path}: {res.status_code}"
        print(f"  [OK] GET {path} -> 200")

    print("\n2. Testing Metadata Config API...")
    res = client.get("/api/config")
    assert res.status_code == 200
    cfg = res.get_json()
    assert cfg["company"]["currency"] == "PKR"
    assert len(cfg["shifts"]) == 4
    print(f"  [OK] GET /api/config -> Company: {cfg['company']['name']}, Currency: {cfg['company']['currency_symbol']}")

    print("\n3. Testing Dashboard API (PKR)...")
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    d = res.get_json()
    assert d["currency"] == "PKR"
    assert d["stats"]["total_departments"] == 18
    print(f"  [OK] GET /api/dashboard -> Total Employees: {d['stats']['total_employees']}, Textile Depts: {d['stats']['total_departments']}")

    print("\n4. Testing Pakistani Employee Management & CNIC Validation...")
    # Add new employee
    payload = {
        "full_name": "Kashif Siddiqui",
        "father_name": "Munir Siddiqui",
        "cnic": "42101-9988776-5",
        "phone": "+92 300 4455667",
        "email": "kashif.s@rajby.local",
        "gender": "Male",
        "dob": "1991-04-12",
        "address": "Korangi Industrial Area, Karachi",
        "city": "Karachi",
        "department": "Cutting Department",
        "designation": "Cutting Operator",
        "employee_type": "Permanent",
        "joining_date": "2024-01-15",
        "status": "Active",
        "shift": "Morning Shift",
        "basic_salary": 52000.0,
        "bank_name": "Meezan Bank Ltd",
        "account_title": "Kashif Siddiqui",
        "account_number_iban": "PK36MEZN0011223344556601"
    }
    res = client.post("/api/employees", json=payload)
    assert res.status_code == 201, f"Failed create employee: {res.data}"
    created = res.get_json()["data"]
    emp_id = created["employee_id"]
    print(f"  [OK] POST /api/employees -> Created {created['full_name']} ({emp_id}) with CNIC {created['cnic']}")

    # Test duplicate CNIC rejection
    res = client.post("/api/employees", json=payload)
    assert res.status_code == 400
    print(f"  [OK] Duplicate CNIC successfully prevented (HTTP 400)")

    # Test GET single employee
    res = client.get(f"/api/employees/{emp_id}")
    assert res.status_code == 200

    # Test Attendance Marking with Overtime
    print("\n5. Testing Attendance & Overtime Tracking...")
    res = client.post("/api/attendance", json={
        "employee_id": emp_id,
        "date": "2026-12-10",
        "status": "Present",
        "check_in": "05:50 AM",
        "check_out": "04:15 PM",
        "overtime_hours": 2.0,
        "shift": "Morning Shift",
        "remarks": "Onboarding overtime"
    })
    assert res.status_code == 201
    print(f"  [OK] POST /api/attendance -> Marked Present with 2.0 hrs Overtime")

    # Duplicate attendance date rejection
    res = client.post("/api/attendance", json={
        "employee_id": emp_id,
        "date": "2026-12-10",
        "status": "Absent"
    })
    assert res.status_code == 400
    print(f"  [OK] Duplicate attendance date prevented (HTTP 400)")

    # Test Department Report
    res = client.get("/api/attendance/department-report")
    assert res.status_code == 200
    print(f"  [OK] GET /api/attendance/department-report -> {len(res.get_json()['data'])} department reports")

    # Test Payroll Calculation Preview in PKR
    print("\n6. Testing Payroll Preview & Generation (PKR)...")
    res = client.get(f"/api/payroll/calculate-preview?employee_id={emp_id}&month=2026-12")
    assert res.status_code == 200
    preview = res.get_json()["data"]
    assert preview["basic_salary"] == 52000.0
    print(f"  [OK] GET /api/payroll/calculate-preview -> Basic: Rs. {preview['basic_salary']:,.2f}")

    # Generate Payroll in PKR
    pay_data = {
        "employee_id": emp_id,
        "month": "2026-12",
        "basic_salary": 52000.0,
        "house_allowance": 15600.0,
        "medical_allowance": 5200.0,
        "transport_allowance": 5000.0,
        "other_allowances": 0.0,
        "overtime_hours": 10.0,
        "overtime_rate": 500.0,
        "overtime_payment": 5000.0,
        "bonus": 2000.0,
        "unpaid_leave_deduction": 0.0,
        "advance_salary": 0.0,
        "loan_deduction": 0.0,
        "tax_deduction": 800.0,
        "eobi_contribution": 370.0,
        "sessi_contribution": 0.0,
        "other_deductions": 0.0,
        "payment_status": "Paid",
        "payment_date": "28-12-2026"
    }
    # Gross = 52000 + 15600 + 5200 + 5000 + 5000 + 2000 = 84800
    # Total Deductions = 800 + 370 = 1170
    # Net = 84800 - 1170 = 83630
    res = client.post("/api/payroll", json=pay_data)
    assert res.status_code == 201
    created_pay = res.get_json()["data"]
    pay_id = created_pay["payroll_id"]
    assert created_pay["net_salary"] == 83630.0
    print(f"  [OK] POST /api/payroll -> Generated {pay_id} (Net: Rs. {created_pay['net_salary']:,.2f})")

    # Duplicate monthly payroll rejection
    res = client.post("/api/payroll", json=pay_data)
    assert res.status_code == 400
    print(f"  [OK] Duplicate monthly payroll prevented (HTTP 400)")

    # Fetch Salary Slip
    res = client.get(f"/api/payroll/{pay_id}")
    assert res.status_code == 200
    slip = res.get_json()["data"]
    assert slip["cnic"] == "42101-9988776-5"
    print(f"  [OK] GET /api/payroll/{pay_id} -> Payslip fetched for {slip['employee_name']}")

    # Cleanup
    client.delete(f"/api/payroll/{pay_id}")
    client.delete(f"/api/employees/{emp_id}")
    print("  [OK] Test cleanup complete.")

    print("\nALL RAJBY TEXTILE VERIFICATION CHECKS COMPLETED WITH 100% SUCCESS! 🚀")

if __name__ == "__main__":
    test_all()
