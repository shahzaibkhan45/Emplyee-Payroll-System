"""
Payroll Model - Rajby Textile Industries
Represents Pakistani textile employee monthly payroll with statutory deductions (EOBI, SESSI, Tax).
"""
from datetime import datetime


class Payroll:
    """Represents a monthly salary calculation in Pakistani Rupees (PKR)."""

    VALID_PAYROLL_STATUSES = ["Pending", "Approved", "Paid"]

    def __init__(
        self,
        payroll_id: str,
        employee_id: str,
        employee_name: str,
        cnic: str,
        department: str,
        designation: str,
        month: str,  # "YYYY-MM" e.g., "2026-11"
        basic_salary: float,
        house_allowance: float = 0.0,
        medical_allowance: float = 0.0,
        transport_allowance: float = 0.0,
        other_allowances: float = 0.0,
        overtime_hours: float = 0.0,
        overtime_rate: float = 0.0,
        overtime_payment: float = 0.0,
        bonus: float = 0.0,
        unpaid_leave_deduction: float = 0.0,
        advance_salary: float = 0.0,
        loan_deduction: float = 0.0,
        tax_deduction: float = 0.0,
        eobi_contribution: float = 0.0,
        sessi_contribution: float = 0.0,
        other_deductions: float = 0.0,
        payment_status: str = "Paid",
        payment_date: str = None
    ):
        self.payroll_id = payroll_id.strip().upper()
        self.employee_id = employee_id.strip().upper()
        self.employee_name = employee_name.strip()
        self.cnic = cnic.strip() if cnic else ""
        self.department = department.strip()
        self.designation = designation.strip()
        self.month = month.strip()

        # Earnings (PKR)
        self.basic_salary = max(0.0, float(basic_salary))
        self.house_allowance = max(0.0, float(house_allowance))
        self.medical_allowance = max(0.0, float(medical_allowance))
        self.transport_allowance = max(0.0, float(transport_allowance))
        self.other_allowances = max(0.0, float(other_allowances))

        self.overtime_hours = max(0.0, float(overtime_hours))
        self.overtime_rate = max(0.0, float(overtime_rate))
        # If overtime payment isn't passed directly, compute from hours * rate
        computed_ot = self.overtime_hours * self.overtime_rate if overtime_rate > 0 else 0.0
        self.overtime_payment = max(0.0, float(overtime_payment if overtime_payment > 0 else computed_ot))
        self.bonus = max(0.0, float(bonus))

        # Deductions (PKR)
        self.unpaid_leave_deduction = max(0.0, float(unpaid_leave_deduction))
        self.advance_salary = max(0.0, float(advance_salary))
        self.loan_deduction = max(0.0, float(loan_deduction))
        self.tax_deduction = max(0.0, float(tax_deduction))
        self.eobi_contribution = max(0.0, float(eobi_contribution))
        self.sessi_contribution = max(0.0, float(sessi_contribution))
        self.other_deductions = max(0.0, float(other_deductions))

        # Status
        status_clean = payment_status.strip().title() if payment_status else "Paid"
        self.payment_status = status_clean if status_clean in self.VALID_PAYROLL_STATUSES else "Paid"
        self.payment_date = payment_date or datetime.now().strftime("%d-%m-%Y")

    @property
    def total_allowances(self) -> float:
        """Total Allowances = House + Medical + Transport + Other."""
        return round(
            self.house_allowance + self.medical_allowance + self.transport_allowance + self.other_allowances,
            2
        )

    @property
    def gross_salary(self) -> float:
        """Gross Salary = Basic Salary + Total Allowances + Overtime Payment + Bonus."""
        return round(
            self.basic_salary + self.total_allowances + self.overtime_payment + self.bonus,
            2
        )

    @property
    def total_deductions(self) -> float:
        """Total Deductions = Unpaid Leave + Advance + Loan + Tax + EOBI + SESSI + Other."""
        return round(
            self.unpaid_leave_deduction +
            self.advance_salary +
            self.loan_deduction +
            self.tax_deduction +
            self.eobi_contribution +
            self.sessi_contribution +
            self.other_deductions,
            2
        )

    @property
    def net_salary(self) -> float:
        """Net Salary = Gross Salary - Total Deductions."""
        net = self.gross_salary - self.total_deductions
        return round(max(0.0, net), 2)

    def to_dict(self) -> dict:
        """Serialize payroll object to dictionary."""
        return {
            "payroll_id": self.payroll_id,
            "employee_id": self.employee_id,
            "employee_name": self.employee_name,
            "cnic": self.cnic,
            "department": self.department,
            "designation": self.designation,
            "month": self.month,
            "basic_salary": round(self.basic_salary, 2),
            "house_allowance": round(self.house_allowance, 2),
            "medical_allowance": round(self.medical_allowance, 2),
            "transport_allowance": round(self.transport_allowance, 2),
            "other_allowances": round(self.other_allowances, 2),
            "overtime_hours": round(self.overtime_hours, 1),
            "overtime_rate": round(self.overtime_rate, 2),
            "overtime_payment": round(self.overtime_payment, 2),
            "bonus": round(self.bonus, 2),
            "total_allowances": self.total_allowances,
            "gross_salary": self.gross_salary,
            "unpaid_leave_deduction": round(self.unpaid_leave_deduction, 2),
            "advance_salary": round(self.advance_salary, 2),
            "loan_deduction": round(self.loan_deduction, 2),
            "tax_deduction": round(self.tax_deduction, 2),
            "eobi_contribution": round(self.eobi_contribution, 2),
            "sessi_contribution": round(self.sessi_contribution, 2),
            "other_deductions": round(self.other_deductions, 2),
            "total_deductions": self.total_deductions,
            "net_salary": self.net_salary,
            "payment_status": self.payment_status,
            "payment_date": self.payment_date
        }

    def __repr__(self):
        return f"<Payroll {self.payroll_id}: {self.employee_name} ({self.month}) - Rs. {self.net_salary:,.2f}>"
