"""
Payroll Manager - Rajby Textile Industries
Handles monthly textile payroll processing in PKR, statutory deductions (EOBI, SESSI), overtime, and validation.
"""
from datetime import datetime
from typing import List, Optional, Dict
from models.payroll import Payroll


class PayrollManager:
    """Manages collection of textile mill Payroll objects stored in an in-memory list."""

    def __init__(self):
        self.payrolls: List[Payroll] = []
        self._next_id: int = 8001

    def generate_id(self, month: str) -> str:
        """Generate formatted payroll ID: e.g. RTI-PAY-202611-8001."""
        clean_m = month.replace("-", "")
        new_id = f"RTI-PAY-{clean_m}-{self._next_id}"
        self._next_id += 1
        return new_id

    def get_by_id(self, payroll_id: str) -> Optional[Payroll]:
        """Find payroll record by ID."""
        clean_id = payroll_id.strip().upper()
        for p in self.payrolls:
            if p.payroll_id == clean_id:
                return p
        return None

    def get_by_employee_and_month(self, employee_id: str, month: str) -> Optional[Payroll]:
        """Find existing payroll entry for an employee for a specific month."""
        emp_clean = employee_id.strip().upper()
        month_clean = month.strip()
        for p in self.payrolls:
            if p.employee_id == emp_clean and p.month == month_clean:
                return p
        return None

    def calculate_suggested_components(
        self,
        employee,
        month: str,
        attendance_manager=None
    ) -> dict:
        """
        Auto-computes suggested Pakistani textile salary components for an employee:
        - House Rent Allowance: 30% of Basic Salary
        - Medical Allowance: 10% of Basic Salary
        - Transport Allowance: Rs. 5,000 standard industrial transport subsidy
        - Overtime calculation: Overtime Hours * (Basic Salary / 208 hours * 2 per Pak Labor Laws)
        - EOBI Contribution: Rs. 370 statutory employee contribution
        - SESSI Contribution: Rs. 0 (Employer covered under Sindh laws) or nominal
        - Unpaid Leave Deduction: Absent days * (Basic Salary / 30)
        - Income Tax: Configurable Pakistani tax slab estimation
        """
        basic = float(employee.basic_salary)

        # Standard Pakistani industrial allowances breakdown
        house_allowance = round(basic * 0.30, 2)
        medical_allowance = round(basic * 0.10, 2)
        transport_allowance = 5000.0 if basic < 100000 else 8000.0
        other_allowances = 0.0

        # Overtime & Absence from attendance records
        overtime_hours = 0.0
        overtime_rate = round((basic / 208.0) * 2.0, 2) if basic > 0 else 0.0
        overtime_payment = 0.0
        unpaid_leave_deduction = 0.0
        absent_days = 0
        half_days = 0

        if attendance_manager:
            stats = attendance_manager.get_employee_monthly_stats(employee.employee_id, month)
            absent_days = stats["absent_days"]
            half_days = stats["half_day_days"]
            overtime_hours = stats["total_overtime_hours"]
            overtime_payment = round(overtime_hours * overtime_rate, 2)

            daily_rate = basic / 30.0
            unpaid_leave_deduction = round((absent_days * daily_rate) + (half_days * daily_rate * 0.5), 2)

        # Statutory Pakistani EOBI & SESSI contributions
        eobi_contribution = 370.0  # Employees' Old-Age Benefits Institution share
        sessi_contribution = 0.0   # SESSI is typically employer paid, kept configurable

        # Pakistani Income Tax estimation on taxable monthly salary (annual > 600,000 PKR)
        gross_monthly = basic + house_allowance + medical_allowance + transport_allowance + overtime_payment
        annual_taxable = gross_monthly * 12.0
        tax_deduction = 0.0
        if annual_taxable > 600000:
            # 5% on amount exceeding 600k annually
            tax_deduction = round(((annual_taxable - 600000) * 0.05) / 12.0, 2)

        return {
            "employee_id": employee.employee_id,
            "employee_name": employee.full_name,
            "cnic": employee.cnic,
            "department": employee.department,
            "designation": employee.designation,
            "month": month,
            "basic_salary": basic,
            "house_allowance": house_allowance,
            "medical_allowance": medical_allowance,
            "transport_allowance": transport_allowance,
            "other_allowances": other_allowances,
            "overtime_hours": overtime_hours,
            "overtime_rate": overtime_rate,
            "overtime_payment": overtime_payment,
            "bonus": 0.0,
            "unpaid_leave_deduction": unpaid_leave_deduction,
            "advance_salary": 0.0,
            "loan_deduction": 0.0,
            "tax_deduction": tax_deduction,
            "eobi_contribution": eobi_contribution,
            "sessi_contribution": sessi_contribution,
            "other_deductions": 0.0,
            "absent_days": absent_days,
            "half_days": half_days
        }

    def generate_payroll(
        self,
        employee_id: str,
        month: str,
        data: dict,
        employee_manager,
        attendance_manager=None
    ) -> Payroll:
        """
        Generate and record monthly payroll for a textile employee in PKR.
        Enforces rule: PREVENT DUPLICATE payroll generation for the same employee and month.
        """
        emp_clean = employee_id.strip().upper()
        month_clean = month.strip()

        if not emp_clean:
            raise ValueError("Employee ID is required.")
        if not month_clean:
            raise ValueError("Payroll month (YYYY-MM) is required.")

        emp = employee_manager.get_by_id(emp_clean)
        if not emp:
            raise ValueError(f"Employee with ID '{emp_clean}' not found.")

        # Duplicate check
        existing = self.get_by_employee_and_month(emp_clean, month_clean)
        if existing:
            raise ValueError(
                f"Payroll for {emp.full_name} ({emp_clean}) for month {month_clean} has already been generated "
                f"(ID: {existing.payroll_id}, Net: Rs. {existing.net_salary:,.2f}, Status: {existing.payment_status})."
            )

        try:
            basic_salary = float(data.get("basic_salary", emp.basic_salary))
            house_allowance = float(data.get("house_allowance", 0.0))
            medical_allowance = float(data.get("medical_allowance", 0.0))
            transport_allowance = float(data.get("transport_allowance", 0.0))
            other_allowances = float(data.get("other_allowances", 0.0))

            overtime_hours = float(data.get("overtime_hours", 0.0))
            overtime_rate = float(data.get("overtime_rate", 0.0))
            overtime_payment = float(data.get("overtime_payment", 0.0))
            bonus = float(data.get("bonus", 0.0))

            unpaid_leave_deduction = float(data.get("unpaid_leave_deduction", 0.0))
            advance_salary = float(data.get("advance_salary", 0.0))
            loan_deduction = float(data.get("loan_deduction", 0.0))
            tax_deduction = float(data.get("tax_deduction", 0.0))
            eobi_contribution = float(data.get("eobi_contribution", 0.0))
            sessi_contribution = float(data.get("sessi_contribution", 0.0))
            other_deductions = float(data.get("other_deductions", 0.0))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid numeric input in payroll components: {str(e)}")

        payment_status = str(data.get("payment_status", "Paid")).strip()
        payment_date = str(data.get("payment_date", datetime.now().strftime("%d-%m-%Y"))).strip()

        payroll_id = self.generate_id(month_clean)
        payroll = Payroll(
            payroll_id=payroll_id,
            employee_id=emp_clean,
            employee_name=emp.full_name,
            cnic=emp.cnic,
            department=emp.department,
            designation=emp.designation,
            month=month_clean,
            basic_salary=basic_salary,
            house_allowance=house_allowance,
            medical_allowance=medical_allowance,
            transport_allowance=transport_allowance,
            other_allowances=other_allowances,
            overtime_hours=overtime_hours,
            overtime_rate=overtime_rate,
            overtime_payment=overtime_payment,
            bonus=bonus,
            unpaid_leave_deduction=unpaid_leave_deduction,
            advance_salary=advance_salary,
            loan_deduction=loan_deduction,
            tax_deduction=tax_deduction,
            eobi_contribution=eobi_contribution,
            sessi_contribution=sessi_contribution,
            other_deductions=other_deductions,
            payment_status=payment_status,
            payment_date=payment_date
        )

        self.payrolls.append(payroll)
        return payroll

    def update_payroll_status(self, payroll_id: str, new_status: str) -> Payroll:
        """Update payroll approval status (Pending, Approved, Paid)."""
        p = self.get_by_id(payroll_id)
        if not p:
            raise ValueError(f"Payroll record '{payroll_id}' not found.")
        cleaned = new_status.strip().title()
        if cleaned in Payroll.VALID_PAYROLL_STATUSES:
            p.payment_status = cleaned
        return p

    def get_all(
        self,
        month: str = None,
        department: str = None,
        employee_id: str = None,
        status: str = None
    ) -> List[dict]:
        """Retrieve payroll records with optional filters."""
        filtered = self.payrolls

        if month and month.strip() and month.lower() != "all":
            m_clean = month.strip()
            filtered = [p for p in filtered if p.month == m_clean]

        if department and department.strip() and department.lower() != "all":
            dept_clean = department.strip().lower()
            filtered = [p for p in filtered if p.department.lower() == dept_clean]

        if employee_id and employee_id.strip() and employee_id.lower() != "all":
            emp_clean = employee_id.strip().upper()
            filtered = [p for p in filtered if p.employee_id == emp_clean]

        if status and status.strip() and status.lower() != "all":
            st_clean = status.strip().lower()
            filtered = [p for p in filtered if p.payment_status.lower() == st_clean]

        sorted_records = sorted(filtered, key=lambda p: (p.month, p.payroll_id), reverse=True)
        return [p.to_dict() for p in sorted_records]

    def delete_payroll(self, payroll_id: str) -> bool:
        """Delete a payroll record."""
        p = self.get_by_id(payroll_id)
        if not p:
            raise ValueError(f"Payroll record '{payroll_id}' not found.")
        self.payrolls.remove(p)
        return True

    def get_summary_statistics(self) -> dict:
        """Compute aggregate PKR figures for dashboard and executive reports."""
        if not self.payrolls:
            return {
                "total_payroll_count": 0,
                "current_month_total": 0.0,
                "pending_payroll_total": 0.0,
                "paid_payroll_total": 0.0,
                "latest_month": datetime.now().strftime("%Y-%m"),
                "department_payouts": {},
                "recent_payrolls": []
            }

        latest_month = self.payrolls[-1].month

        # Month specific sums
        current_month_records = [p for p in self.payrolls if p.month == latest_month]
        current_month_total = sum(p.net_salary for p in current_month_records)

        pending_total = sum(p.net_salary for p in current_month_records if p.payment_status in ["Pending", "Approved"])
        paid_total = sum(p.net_salary for p in current_month_records if p.payment_status == "Paid")

        dept_payouts = {}
        for p in current_month_records:
            dept_payouts[p.department] = round(dept_payouts.get(p.department, 0.0) + p.net_salary, 2)

        recent = [p.to_dict() for p in sorted(self.payrolls, key=lambda x: x.payroll_id, reverse=True)[:5]]

        return {
            "total_payroll_count": len(self.payrolls),
            "current_month_total": round(current_month_total, 2),
            "pending_payroll_total": round(pending_total, 2),
            "paid_payroll_total": round(paid_total, 2),
            "latest_month": latest_month,
            "department_payouts": dept_payouts,
            "recent_payrolls": recent
        }
