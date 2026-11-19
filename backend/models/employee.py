"""
Employee Model - Rajby Textile Industries
Represents a textile mill employee with Pakistani identity, demographic, job, and banking details.
"""
from datetime import datetime


class Employee:
    """Represents an employee entity in the textile factory."""

    VALID_EMPLOYEE_TYPES = ["Permanent", "Contract", "Daily Wage", "Probation"]
    VALID_STATUSES = ["Active", "Inactive", "On Leave", "Terminated"]
    VALID_SHIFTS = [
        "Morning Shift",        # 06:00 - 14:00
        "Evening Shift",        # 14:00 - 22:00
        "Night Shift",          # 22:00 - 06:00
        "General Office Shift"  # 09:00 - 18:00
    ]

    def __init__(
        self,
        employee_id: str,
        full_name: str,
        father_name: str,
        cnic: str,
        phone: str,
        email: str,
        gender: str,
        dob: str,
        address: str,
        city: str = "Karachi",
        emergency_contact: str = "",
        department: str = "",
        designation: str = "",
        employee_type: str = "Permanent",
        joining_date: str = "",
        status: str = "Active",
        shift: str = "General Office Shift",
        basic_salary: float = 0.0,
        bank_name: str = "Meezan Bank Ltd",
        account_title: str = "",
        account_number_iban: str = "",
        profile_picture: str = ""
    ):
        self.employee_id = employee_id.strip().upper()
        self.full_name = full_name.strip()
        self.father_name = father_name.strip() if father_name else ""
        self.cnic = cnic.strip()  # Format: XXXXX-XXXXXXX-X
        self.phone = phone.strip()
        self.email = email.strip().lower() if email else ""
        self.gender = gender.strip()
        self.dob = dob.strip() if dob else ""
        self.address = address.strip() if address else ""
        self.city = city.strip() if city else "Karachi"
        self.emergency_contact = emergency_contact.strip() if emergency_contact else ""
        self.department = department.strip()
        self.designation = designation.strip()

        # Employee Type
        emp_type_clean = employee_type.strip().title()
        if emp_type_clean in ["Dailywage", "Daily-Wage"]:
            emp_type_clean = "Daily Wage"
        self.employee_type = emp_type_clean if emp_type_clean in self.VALID_EMPLOYEE_TYPES else "Permanent"

        self.joining_date = joining_date.strip() if joining_date else datetime.now().strftime("%d-%m-%Y")

        # Employment Status
        status_clean = status.strip().title()
        if status_clean in ["Onleave", "On-Leave"]:
            status_clean = "On Leave"
        self.status = status_clean if status_clean in self.VALID_STATUSES else "Active"

        # Shift
        self.shift = shift.strip() if shift and shift.strip() in self.VALID_SHIFTS else "General Office Shift"

        # Compensation in PKR
        self.basic_salary = max(0.0, float(basic_salary))

        # Banking
        self.bank_name = bank_name.strip() if bank_name else "Meezan Bank Ltd"
        self.account_title = account_title.strip() if account_title else self.full_name
        self.account_number_iban = account_number_iban.strip() if account_number_iban else ""
        self.profile_picture = profile_picture.strip() if profile_picture else ""

    def update(self, **kwargs):
        """Update employee details with validation."""
        for key, value in kwargs.items():
            if value is None:
                continue
            if key == "full_name" and str(value).strip():
                self.full_name = str(value).strip()
            elif key == "father_name":
                self.father_name = str(value).strip()
            elif key == "cnic" and str(value).strip():
                self.cnic = str(value).strip()
            elif key == "phone" and str(value).strip():
                self.phone = str(value).strip()
            elif key == "email":
                self.email = str(value).strip().lower()
            elif key == "gender" and str(value).strip():
                self.gender = str(value).strip()
            elif key == "dob":
                self.dob = str(value).strip()
            elif key == "address":
                self.address = str(value).strip()
            elif key == "city":
                self.city = str(value).strip()
            elif key == "emergency_contact":
                self.emergency_contact = str(value).strip()
            elif key == "department" and str(value).strip():
                self.department = str(value).strip()
            elif key == "designation" and str(value).strip():
                self.designation = str(value).strip()
            elif key == "employee_type":
                cleaned = str(value).strip().title()
                if cleaned in ["Dailywage", "Daily-Wage"]:
                    cleaned = "Daily Wage"
                if cleaned in self.VALID_EMPLOYEE_TYPES:
                    self.employee_type = cleaned
            elif key == "joining_date" and str(value).strip():
                self.joining_date = str(value).strip()
            elif key == "status":
                cleaned = str(value).strip().title()
                if cleaned in ["Onleave", "On-Leave"]:
                    cleaned = "On Leave"
                if cleaned in self.VALID_STATUSES:
                    self.status = cleaned
            elif key == "shift":
                if str(value).strip() in self.VALID_SHIFTS:
                    self.shift = str(value).strip()
            elif key == "basic_salary":
                self.basic_salary = max(0.0, float(value))
            elif key == "bank_name":
                self.bank_name = str(value).strip()
            elif key == "account_title":
                self.account_title = str(value).strip()
            elif key == "account_number_iban":
                self.account_number_iban = str(value).strip()
            elif key == "profile_picture":
                self.profile_picture = str(value).strip()

    @property
    def is_active(self) -> bool:
        """Check if employee is active."""
        return self.status == "Active"

    def to_dict(self) -> dict:
        """Serialize employee object to a dictionary."""
        return {
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "father_name": self.father_name,
            "cnic": self.cnic,
            "phone": self.phone,
            "email": self.email,
            "gender": self.gender,
            "dob": self.dob,
            "address": self.address,
            "city": self.city,
            "emergency_contact": self.emergency_contact,
            "department": self.department,
            "designation": self.designation,
            "employee_type": self.employee_type,
            "joining_date": self.joining_date,
            "status": self.status,
            "shift": self.shift,
            "basic_salary": round(self.basic_salary, 2),
            "bank_name": self.bank_name,
            "account_title": self.account_title,
            "account_number_iban": self.account_number_iban,
            "profile_picture": self.profile_picture
        }

    def __repr__(self):
        return f"<Employee {self.employee_id}: {self.full_name} ({self.department}) - {self.cnic}>"
