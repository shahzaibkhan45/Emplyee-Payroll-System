"""
Unit & Integration Test Suite - Rajby Textile Industries
Tests Pakistani CNIC validation, textile department deletion checks, duplicate attendance & payroll rules.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.department import Department
from models.employee import Employee
from models.attendance import Attendance
from models.payroll import Payroll
from managers.department_manager import DepartmentManager
from managers.employee_manager import EmployeeManager
from managers.attendance_manager import AttendanceManager
from managers.payroll_manager import PayrollManager


class TestRajbyPayrollSystem(unittest.TestCase):

    def setUp(self):
        """Set up fresh manager instances."""
        self.dept_mgr = DepartmentManager()
        self.emp_mgr = EmployeeManager()
        self.att_mgr = AttendanceManager()
        self.pay_mgr = PayrollManager()

        self.dept1 = self.dept_mgr.add_department("Stitching Department", "Denim stitching line")
        self.emp1 = self.emp_mgr.add_employee({
            "full_name": "Tariq Mahmood",
            "father_name": "Mahmood Ahmed",
            "cnic": "42101-1122334-1",
            "phone": "+92 300 1234567",
            "email": "tariq@rajby.local",
            "gender": "Male",
            "dob": "10-05-1990",
            "address": "Korangi, Karachi",
            "city": "Karachi",
            "department": "Stitching Department",
            "designation": "Stitching Operator",
            "employee_type": "Permanent",
            "joining_date": "01-01-2022",
            "status": "Active",
            "shift": "Morning Shift",
            "basic_salary": 50000.0,
            "bank_name": "Meezan Bank Ltd",
            "account_title": "Tariq Mahmood",
            "account_number_iban": "PK36MEZN0001020304050607"
        }, self.dept_mgr)

    def test_department_assignment_protection(self):
        """Cannot delete department if employees are assigned."""
        with self.assertRaises(ValueError):
            self.dept_mgr.delete_department(self.dept1.dept_id, self.emp_mgr)

        empty_dept = self.dept_mgr.add_department("Empty Dept", "No one assigned")
        self.assertTrue(self.dept_mgr.delete_department(empty_dept.dept_id, self.emp_mgr))

    def test_pakistani_cnic_validation(self):
        """Validates CNIC format (XXXXX-XXXXXXX-X) and prevents duplicates."""
        # Invalid format
        with self.assertRaises(ValueError):
            self.emp_mgr.add_employee({
                "full_name": "Invalid CNIC",
                "cnic": "12345",  # Invalid
                "phone": "+92 300 0000000",
                "department": "Stitching Department",
                "designation": "Helper",
                "basic_salary": 35000.0
            }, self.dept_mgr)

        # Duplicate CNIC
        with self.assertRaises(ValueError):
            self.emp_mgr.add_employee({
                "full_name": "Duplicate Person",
                "cnic": "42101-1122334-1",  # Same as Tariq Mahmood
                "phone": "+92 300 9999999",
                "department": "Stitching Department",
                "designation": "Helper",
                "basic_salary": 35000.0
            }, self.dept_mgr)

    def test_attendance_and_overtime(self):
        """Tests attendance marking, duplicate prevention on same date, and overtime."""
        rec = self.att_mgr.mark_attendance(
            employee_id=self.emp1.employee_id,
            date="2026-11-19",
            status="Present",
            check_in="05:55 AM",
            check_out="04:15 PM",
            overtime_hours=2.0,
            shift="Morning Shift",
            remarks="On time with OT",
            employee_manager=self.emp_mgr
        )
        self.assertEqual(rec.overtime_hours, 2.0)

        # Duplicate date rejected
        with self.assertRaises(ValueError):
            self.att_mgr.mark_attendance(
                employee_id=self.emp1.employee_id,
                date="2026-11-19",
                status="Absent",
                employee_manager=self.emp_mgr
            )

    def test_pkr_payroll_math_and_deductions(self):
        """Tests payroll math in PKR including EOBI, SESSI, and overtime."""
        # basic: 50,000, house: 15,000, med: 5,000, transport: 5,000 (Allowances: 25,000)
        # overtime: 2,500, bonus: 5,000 => Gross: 50,000 + 25,000 + 2,500 + 5,000 = 82,500
        # deductions: eobi 370, tax 1000, advance 2000 => Total Ded: 3,370
        # Net: 82,500 - 3,370 = 79,130
        data = {
            "basic_salary": 50000.0,
            "house_allowance": 15000.0,
            "medical_allowance": 5000.0,
            "transport_allowance": 5000.0,
            "other_allowances": 0.0,
            "overtime_hours": 5.0,
            "overtime_rate": 500.0,
            "overtime_payment": 2500.0,
            "bonus": 5000.0,
            "eobi_contribution": 370.0,
            "tax_deduction": 1000.0,
            "advance_salary": 2000.0
        }
        pay = self.pay_mgr.generate_payroll(
            self.emp1.employee_id, "2026-11", data, self.emp_mgr, self.att_mgr
        )
        self.assertEqual(pay.gross_salary, 82500.0)
        self.assertEqual(pay.total_deductions, 3370.0)
        self.assertEqual(pay.net_salary, 79130.0)

        # Duplicate month rejected
        with self.assertRaises(ValueError):
            self.pay_mgr.generate_payroll(
                self.emp1.employee_id, "2026-11", data, self.emp_mgr, self.att_mgr
            )


if __name__ == "__main__":
    unittest.main()
