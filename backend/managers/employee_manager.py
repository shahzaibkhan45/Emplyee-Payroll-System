"""
Employee Manager - Rajby Textile Industries
Handles employee business logic, in-memory list storage, and Pakistani CNIC & ID validations.
"""
import re
from typing import List, Optional
from models.employee import Employee


class EmployeeManager:
    """Manages collection of textile mill Employee objects stored in an in-memory list."""

    def __init__(self):
        self.employees: List[Employee] = []
        self._next_id: int = 1001

    def generate_id(self) -> str:
        """Generate auto-incremented Rajby employee ID: RTI-1001."""
        new_id = f"RTI-{self._next_id}"
        self._next_id += 1
        return new_id

    def validate_cnic(self, cnic: str, exclude_id: str = None) -> bool:
        """
        Validate Pakistani CNIC format (XXXXX-XXXXXXX-X) and verify uniqueness.
        """
        cnic_clean = cnic.strip()
        pattern = r"^\d{5}-\d{7}-\d{1}$"
        if not re.match(pattern, cnic_clean):
            raise ValueError(f"Invalid CNIC format: '{cnic}'. CNIC must follow format: 42101-1234567-1 (13 digits with hyphens).")

        for emp in self.employees:
            if exclude_id and emp.employee_id == exclude_id.strip().upper():
                continue
            if emp.cnic == cnic_clean:
                raise ValueError(f"Employee with CNIC '{cnic_clean}' already exists in the system ({emp.full_name} - {emp.employee_id}).")
        return True

    def validate_email(self, email: str, exclude_id: str = None) -> bool:
        """Validate email format and verify uniqueness across employees."""
        if not email or not email.strip():
            return True
        email_clean = email.strip().lower()
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email_clean):
            raise ValueError(f"Invalid email address format: '{email}'.")

        for emp in self.employees:
            if exclude_id and emp.employee_id == exclude_id.strip().upper():
                continue
            if emp.email and emp.email == email_clean:
                raise ValueError(f"An employee with email '{email_clean}' already exists ({emp.full_name}).")
        return True

    def add_employee(self, data: dict, department_manager=None) -> Employee:
        """Create and append a new Employee object with full Pakistani textile validations."""
        required = ["full_name", "cnic", "phone", "department", "designation", "basic_salary"]
        for field in required:
            if field not in data or str(data[field]).strip() == "":
                raise ValueError(f"Field '{field.replace('_', ' ').title()}' is required.")

        full_name = str(data["full_name"]).strip()
        father_name = str(data.get("father_name", "")).strip()
        cnic = str(data["cnic"]).strip()
        self.validate_cnic(cnic)

        email = str(data.get("email", "")).strip().lower()
        self.validate_email(email)

        phone = str(data["phone"]).strip()
        gender = str(data.get("gender", "Male")).strip()
        dob = str(data.get("dob", "")).strip()
        address = str(data.get("address", "")).strip()
        city = str(data.get("city", "Karachi")).strip()
        emergency_contact = str(data.get("emergency_contact", "")).strip()
        department = str(data["department"]).strip()

        if department_manager:
            dept = department_manager.get_by_name(department)
            if not dept:
                raise ValueError(f"Department '{department}' does not exist.")

        designation = str(data["designation"]).strip()
        employee_type = str(data.get("employee_type", "Permanent")).strip()
        joining_date = str(data.get("joining_date", "")).strip()
        status = str(data.get("status", "Active")).strip()
        shift = str(data.get("shift", "General Office Shift")).strip()

        try:
            basic_salary = float(data["basic_salary"])
            if basic_salary < 0:
                raise ValueError("Basic salary cannot be negative.")
        except (ValueError, TypeError):
            raise ValueError("Basic salary must be a valid positive number in PKR.")

        bank_name = str(data.get("bank_name", "Meezan Bank Ltd")).strip()
        account_title = str(data.get("account_title", full_name)).strip()
        account_number_iban = str(data.get("account_number_iban", "")).strip()
        profile_picture = str(data.get("profile_picture", "")).strip()

        # Check for custom employee_id or auto-generate
        custom_id = str(data.get("employee_id", "")).strip().upper()
        if custom_id:
            if self.get_by_id(custom_id):
                raise ValueError(f"Employee ID '{custom_id}' is already assigned.")
            emp_id = custom_id
        else:
            emp_id = self.generate_id()

        employee = Employee(
            employee_id=emp_id,
            full_name=full_name,
            father_name=father_name,
            cnic=cnic,
            phone=phone,
            email=email,
            gender=gender,
            dob=dob,
            address=address,
            city=city,
            emergency_contact=emergency_contact,
            department=department,
            designation=designation,
            employee_type=employee_type,
            joining_date=joining_date,
            status=status,
            shift=shift,
            basic_salary=basic_salary,
            bank_name=bank_name,
            account_title=account_title,
            account_number_iban=account_number_iban,
            profile_picture=profile_picture
        )

        self.employees.append(employee)
        return employee

    def get_all(
        self,
        search: str = None,
        department: str = None,
        status: str = None,
        employee_type: str = None,
        shift: str = None
    ) -> List[dict]:
        """Retrieve employees with searching and filtering."""
        filtered = self.employees

        if department and department.strip() and department.lower() != "all":
            dept_filter = department.strip().lower()
            filtered = [e for e in filtered if e.department.lower() == dept_filter]

        if status and status.strip() and status.lower() != "all":
            st_filter = status.strip().lower()
            filtered = [e for e in filtered if e.status.lower() == st_filter]

        if employee_type and employee_type.strip() and employee_type.lower() != "all":
            type_filter = employee_type.strip().lower()
            filtered = [e for e in filtered if e.employee_type.lower() == type_filter]

        if shift and shift.strip() and shift.lower() != "all":
            shift_filter = shift.strip().lower()
            filtered = [e for e in filtered if e.shift.lower() == shift_filter]

        if search and search.strip():
            query = search.strip().lower()
            filtered = [
                e for e in filtered
                if query in e.employee_id.lower()
                or query in e.full_name.lower()
                or query in e.father_name.lower()
                or query in e.cnic.lower()
                or query in e.email.lower()
                or query in e.designation.lower()
                or query in e.department.lower()
                or query in e.phone.lower()
            ]

        return [e.to_dict() for e in filtered]

    def get_by_id(self, employee_id: str) -> Optional[Employee]:
        """Find an Employee object by ID."""
        clean_id = employee_id.strip().upper()
        for emp in self.employees:
            if emp.employee_id == clean_id:
                return emp
        return None

    def get_by_cnic(self, cnic: str) -> Optional[Employee]:
        """Find employee by CNIC."""
        clean_cnic = cnic.strip()
        for emp in self.employees:
            if emp.cnic == clean_cnic:
                return emp
        return None

    def update_employee(self, employee_id: str, data: dict, department_manager=None) -> Employee:
        """Update existing employee with Pakistani validation."""
        emp = self.get_by_id(employee_id)
        if not emp:
            raise ValueError(f"Employee with ID '{employee_id}' not found.")

        # CNIC validation
        if "cnic" in data and data["cnic"]:
            self.validate_cnic(str(data["cnic"]), exclude_id=emp.employee_id)

        # Email validation
        if "email" in data and data["email"]:
            self.validate_email(str(data["email"]), exclude_id=emp.employee_id)

        # Department validation
        if "department" in data and data["department"] and department_manager:
            if not department_manager.get_by_name(str(data["department"])):
                raise ValueError(f"Department '{data['department']}' does not exist.")

        # Basic salary validation
        if "basic_salary" in data and data["basic_salary"] is not None:
            try:
                basic_salary = float(data["basic_salary"])
                if basic_salary < 0:
                    raise ValueError("Basic salary cannot be negative.")
                data["basic_salary"] = basic_salary
            except (ValueError, TypeError):
                raise ValueError("Basic salary must be a valid number in PKR.")

        emp.update(**data)
        return emp

    def delete_employee(self, employee_id: str) -> bool:
        """Remove employee from in-memory list."""
        emp = self.get_by_id(employee_id)
        if not emp:
            raise ValueError(f"Employee with ID '{employee_id}' not found.")
        self.employees.remove(emp)
        return True

    def count_total(self) -> int:
        """Total number of employees."""
        return len(self.employees)

    def count_active(self) -> int:
        """Total number of active employees."""
        return sum(1 for e in self.employees if e.status == "Active")

    def count_inactive(self) -> int:
        """Total number of inactive or terminated employees."""
        return sum(1 for e in self.employees if e.status in ["Inactive", "Terminated"])

    def count_on_leave(self) -> int:
        """Total number of employees currently on leave."""
        return sum(1 for e in self.employees if e.status == "On Leave")

    def count_by_department(self, department_name: str) -> int:
        """Count employees currently assigned to a department."""
        dept_name = department_name.strip().lower()
        return sum(1 for e in self.employees if e.department.lower() == dept_name)

    def get_recent_employees(self, limit: int = 5) -> List[dict]:
        """Return the most recently added or joined employees."""
        sorted_emps = sorted(
            self.employees,
            key=lambda e: (e.joining_date, e.employee_id),
            reverse=True
        )
        return [e.to_dict() for e in sorted_emps[:limit]]
