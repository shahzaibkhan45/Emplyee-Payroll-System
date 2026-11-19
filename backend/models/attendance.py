"""
Attendance Model - Rajby Textile Industries
Represents daily factory floor and office attendance, biometric check-in/out, and overtime.
"""
from datetime import datetime


class Attendance:
    """Represents a daily attendance entry for a textile factory employee."""

    VALID_STATUSES = [
        "Present",
        "Absent",
        "Half Day",
        "Leave",
        "Late Arrival",
        "Early Departure"
    ]

    def __init__(
        self,
        attendance_id: str,
        employee_id: str,
        date: str,
        status: str = "Present",
        check_in: str = "08:00 AM",
        check_out: str = "05:00 PM",
        overtime_hours: float = 0.0,
        shift: str = "General Office Shift",
        remarks: str = ""
    ):
        self.attendance_id = attendance_id.strip().upper()
        self.employee_id = employee_id.strip().upper()
        self.date = date.strip()
        
        normalized_status = status.strip().title()
        if normalized_status in ["Halfday", "Half-Day"]:
            normalized_status = "Half Day"
        elif normalized_status in ["Late", "Latearrival"]:
            normalized_status = "Late Arrival"
        elif normalized_status in ["Early", "Earlydeparture"]:
            normalized_status = "Early Departure"

        if normalized_status not in self.VALID_STATUSES:
            normalized_status = "Present"

        self.status = normalized_status
        self.check_in = check_in.strip() if check_in else "-"
        self.check_out = check_out.strip() if check_out else "-"
        self.overtime_hours = max(0.0, float(overtime_hours or 0.0))
        self.shift = shift.strip() if shift else "General Office Shift"
        self.remarks = remarks.strip() if remarks else ""

    def update(
        self,
        status: str = None,
        check_in: str = None,
        check_out: str = None,
        overtime_hours: float = None,
        shift: str = None,
        remarks: str = None
    ):
        """Update attendance details."""
        if status is not None and status.strip():
            normalized = status.strip().title()
            if normalized in ["Halfday", "Half-Day"]:
                normalized = "Half Day"
            elif normalized in ["Late", "Latearrival"]:
                normalized = "Late Arrival"
            elif normalized in ["Early", "Earlydeparture"]:
                normalized = "Early Departure"
            if normalized in self.VALID_STATUSES:
                self.status = normalized

        if check_in is not None:
            self.check_in = check_in.strip()
        if check_out is not None:
            self.check_out = check_out.strip()
        if overtime_hours is not None:
            self.overtime_hours = max(0.0, float(overtime_hours))
        if shift is not None:
            self.shift = shift.strip()
        if remarks is not None:
            self.remarks = remarks.strip()

    def to_dict(self) -> dict:
        """Serialize attendance object to dictionary."""
        return {
            "attendance_id": self.attendance_id,
            "employee_id": self.employee_id,
            "date": self.date,
            "status": self.status,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "overtime_hours": round(self.overtime_hours, 1),
            "shift": self.shift,
            "remarks": self.remarks
        }

    def __repr__(self):
        return f"<Attendance {self.attendance_id}: {self.employee_id} on {self.date} [{self.status}] (OT: {self.overtime_hours}h)>"
