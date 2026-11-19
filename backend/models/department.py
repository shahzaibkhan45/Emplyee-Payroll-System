"""
Department Model
Represents a textile manufacturing department at Rajby Textile Industries.
"""
from datetime import datetime


class Department:
    """Represents an organizational department within the textile mill."""

    def __init__(self, dept_id: str, name: str, description: str = "", created_at: str = None):
        self.dept_id = dept_id.strip().upper()
        self.name = name.strip()
        self.description = description.strip() if description else ""
        self.created_at = created_at or datetime.now().strftime("%d-%m-%Y")

    def update(self, name: str = None, description: str = None):
        """Update department details."""
        if name is not None and name.strip():
            self.name = name.strip()
        if description is not None:
            self.description = description.strip()

    def to_dict(self) -> dict:
        """Serialize department object to dictionary."""
        return {
            "dept_id": self.dept_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Department {self.dept_id}: {self.name}>"
