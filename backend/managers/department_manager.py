"""
Department Manager - Rajby Textile Industries
Handles all textile manufacturing departments and list storage.
"""
from typing import List, Optional
from models.department import Department


class DepartmentManager:
    """Manages collection of Department objects stored in an in-memory list."""

    def __init__(self):
        self.departments: List[Department] = []
        self._next_id: int = 101

    def generate_id(self) -> str:
        """Generate auto-incremented department ID e.g. DEP-101."""
        new_id = f"DEP-{self._next_id}"
        self._next_id += 1
        return new_id

    def add_department(self, name: str, description: str = "") -> Department:
        """Add new textile department, checking for uniqueness."""
        name_clean = name.strip()
        if not name_clean:
            raise ValueError("Department name is required.")

        for dept in self.departments:
            if dept.name.lower() == name_clean.lower():
                raise ValueError(f"Department '{name_clean}' already exists.")

        dept_id = self.generate_id()
        department = Department(dept_id=dept_id, name=name_clean, description=description)
        self.departments.append(department)
        return department

    def get_all(self, employee_manager=None) -> List[dict]:
        """Return all departments with live employee counts."""
        result = []
        for dept in self.departments:
            data = dept.to_dict()
            if employee_manager:
                data["employee_count"] = employee_manager.count_by_department(dept.name)
            else:
                data["employee_count"] = 0
            result.append(data)
        return result

    def get_by_id(self, dept_id: str) -> Optional[Department]:
        """Find a Department object by dept_id."""
        clean_id = dept_id.strip().upper()
        for dept in self.departments:
            if dept.dept_id == clean_id:
                return dept
        return None

    def get_by_name(self, name: str) -> Optional[Department]:
        """Find a Department object by name (case-insensitive)."""
        clean_name = name.strip().lower()
        for dept in self.departments:
            if dept.name.lower() == clean_name:
                return dept
        return None

    def update_department(self, dept_id: str, name: str, description: str = None) -> Department:
        """Update department name and description."""
        dept = self.get_by_id(dept_id)
        if not dept:
            raise ValueError(f"Department with ID '{dept_id}' not found.")

        name_clean = name.strip() if name else ""
        if name_clean and name_clean.lower() != dept.name.lower():
            for other in self.departments:
                if other.dept_id != dept.dept_id and other.name.lower() == name_clean.lower():
                    raise ValueError(f"Another department named '{name_clean}' already exists.")

        dept.update(name=name_clean, description=description)
        return dept

    def delete_department(self, dept_id: str, employee_manager) -> bool:
        """
        Delete department.
        Enforces rule: Cannot delete a department if employees are currently assigned to it!
        """
        dept = self.get_by_id(dept_id)
        if not dept:
            raise ValueError(f"Department with ID '{dept_id}' not found.")

        assigned_count = employee_manager.count_by_department(dept.name)
        if assigned_count > 0:
            raise ValueError(
                f"Cannot delete department '{dept.name}' because {assigned_count} employee(s) are assigned to it. "
                f"Please reassign or update staff records first."
            )

        self.departments.remove(dept)
        return True

    def count(self) -> int:
        """Total number of departments."""
        return len(self.departments)
