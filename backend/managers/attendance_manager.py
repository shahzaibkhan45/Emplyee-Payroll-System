"""
Attendance Manager - Rajby Textile Industries
Handles daily factory floor attendance, shifts, check-in/out, overtime, and department reports.
"""
from datetime import datetime
from typing import List, Optional, Dict
from models.attendance import Attendance


class AttendanceManager:
    """Manages collection of textile factory Attendance objects stored in an in-memory list."""

    def __init__(self):
        self.attendance_records: List[Attendance] = []
        self._next_id: int = 5001

    def generate_id(self) -> str:
        """Generate auto-incremented attendance ID e.g. ATT-5001."""
        new_id = f"ATT-{self._next_id}"
        self._next_id += 1
        return new_id

    def get_by_id(self, attendance_id: str) -> Optional[Attendance]:
        """Find attendance record by ID."""
        clean_id = attendance_id.strip().upper()
        for record in self.attendance_records:
            if record.attendance_id == clean_id:
                return record
        return None

    def find_entry(self, employee_id: str, date: str) -> Optional[Attendance]:
        """Find an existing attendance entry for an employee on a specific date."""
        emp_clean = employee_id.strip().upper()
        date_clean = date.strip()
        for record in self.attendance_records:
            if record.employee_id == emp_clean and record.date == date_clean:
                return record
        return None

    def mark_attendance(
        self,
        employee_id: str,
        date: str,
        status: str = "Present",
        check_in: str = "08:00 AM",
        check_out: str = "05:00 PM",
        overtime_hours: float = 0.0,
        shift: str = "General Office Shift",
        remarks: str = "",
        employee_manager=None
    ) -> Attendance:
        """
        Mark attendance for an employee on a date.
        Enforces rule: PREVENT DUPLICATE attendance entries for the same employee on the same date.
        """
        emp_clean = employee_id.strip().upper()
        date_clean = date.strip()

        if not emp_clean:
            raise ValueError("Employee ID is required.")
        if not date_clean:
            raise ValueError("Attendance date is required.")

        emp = None
        if employee_manager:
            emp = employee_manager.get_by_id(emp_clean)
            if not emp:
                raise ValueError(f"Employee with ID '{emp_clean}' does not exist.")

        # Check duplicate
        existing = self.find_entry(emp_clean, date_clean)
        if existing:
            emp_name = emp.full_name if emp else emp_clean
            raise ValueError(
                f"Attendance is already marked for {emp_name} ({emp_clean}) on {date_clean} "
                f"(Status: {existing.status}, In: {existing.check_in}, Out: {existing.check_out}). "
                f"Please edit the existing record instead."
            )

        att_id = self.generate_id()
        record = Attendance(
            attendance_id=att_id,
            employee_id=emp_clean,
            date=date_clean,
            status=status,
            check_in=check_in,
            check_out=check_out,
            overtime_hours=overtime_hours,
            shift=shift or (emp.shift if emp else "General Office Shift"),
            remarks=remarks
        )
        self.attendance_records.append(record)
        return record

    def update_attendance(
        self,
        attendance_id: str,
        status: str = None,
        check_in: str = None,
        check_out: str = None,
        overtime_hours: float = None,
        shift: str = None,
        remarks: str = None
    ) -> Attendance:
        """Update an existing attendance record."""
        record = self.get_by_id(attendance_id)
        if not record:
            raise ValueError(f"Attendance record '{attendance_id}' not found.")
        record.update(
            status=status,
            check_in=check_in,
            check_out=check_out,
            overtime_hours=overtime_hours,
            shift=shift,
            remarks=remarks
        )
        return record

    def delete_attendance(self, attendance_id: str) -> bool:
        """Delete an attendance record."""
        record = self.get_by_id(attendance_id)
        if not record:
            raise ValueError(f"Attendance record '{attendance_id}' not found.")
        self.attendance_records.remove(record)
        return True

    def get_attendance_list(
        self,
        date: str = None,
        month: str = None,
        department: str = None,
        employee_id: str = None,
        status: str = None,
        employee_manager=None
    ) -> List[dict]:
        """
        Filter attendance records by employee, department, date, month, or status.
        Enriches records with employee name, department, designation, and CNIC.
        """
        matched = self.attendance_records

        if date and date.strip() and date.lower() != "all":
            d_clean = date.strip()
            matched = [r for r in matched if r.date == d_clean]

        if month and month.strip() and month.lower() != "all":
            m_clean = month.strip()
            matched = [r for r in matched if r.date.startswith(m_clean) or (len(r.date) >= 7 and r.date.endswith(m_clean))]

        if employee_id and employee_id.strip() and employee_id.lower() != "all":
            emp_clean = employee_id.strip().upper()
            matched = [r for r in matched if r.employee_id == emp_clean]

        if status and status.strip() and status.lower() != "all":
            st_clean = status.strip().lower()
            matched = [r for r in matched if r.status.lower() == st_clean]

        results = []
        for r in matched:
            data = r.to_dict()
            emp = employee_manager.get_by_id(r.employee_id) if employee_manager else None
            if emp:
                data["employee_name"] = emp.full_name
                data["department"] = emp.department
                data["designation"] = emp.designation
                data["cnic"] = emp.cnic
            else:
                data["employee_name"] = "Unknown"
                data["department"] = "N/A"
                data["designation"] = "N/A"
                data["cnic"] = "N/A"

            # Filter by department if requested
            if department and department.strip() and department.lower() != "all":
                if data["department"].lower() != department.strip().lower():
                    continue

            results.append(data)

        results.sort(key=lambda x: (x["date"], x["employee_id"]), reverse=True)
        return results

    def get_department_attendance_report(self, date: str, employee_manager, department_manager) -> List[dict]:
        """Generate department-wise attendance statistics for a given date."""
        target_date = date.strip()
        daily_records = [r for r in self.attendance_records if r.date == target_date]

        report = []
        for dept in department_manager.departments:
            dept_emps = [e for e in employee_manager.employees if e.department.lower() == dept.name.lower() and e.status == "Active"]
            dept_emp_ids = {e.employee_id for e in dept_emps}

            records_in_dept = [r for r in daily_records if r.employee_id in dept_emp_ids]

            present = sum(1 for r in records_in_dept if r.status in ["Present", "Late Arrival"])
            absent = sum(1 for r in records_in_dept if r.status == "Absent")
            half_day = sum(1 for r in records_in_dept if r.status == "Half Day")
            on_leave = sum(1 for r in records_in_dept if r.status == "Leave")
            ot_hours = sum(r.overtime_hours for r in records_in_dept)

            total_staff = len(dept_emps)
            marked = len(records_in_dept)
            unmarked = max(0, total_staff - marked)

            report.append({
                "department_name": dept.name,
                "total_staff": total_staff,
                "present": present,
                "absent": absent,
                "half_day": half_day,
                "leave": on_leave,
                "unmarked": unmarked,
                "overtime_hours": round(ot_hours, 1)
            })

        return report

    def get_employee_monthly_stats(self, employee_id: str, month: str) -> Dict[str, float]:
        """
        Calculate total present days, absent days, half-days, leaves, and overtime hours
        for an employee in a specific month.
        """
        emp_clean = employee_id.strip().upper()
        month_clean = month.strip()

        records = [
            r for r in self.attendance_records
            if r.employee_id == emp_clean and (r.date.startswith(month_clean) or r.date.endswith(month_clean))
        ]

        stats = {
            "present_days": 0,
            "absent_days": 0,
            "half_day_days": 0,
            "leave_days": 0,
            "late_arrivals": 0,
            "total_overtime_hours": 0.0,
            "total_marked": len(records)
        }

        for r in records:
            st = r.status.lower()
            if st == "present":
                stats["present_days"] += 1
            elif st == "absent":
                stats["absent_days"] += 1
            elif "half" in st:
                stats["half_day_days"] += 1
            elif st == "leave":
                stats["leave_days"] += 1
            elif "late" in st:
                stats["late_arrivals"] += 1
                stats["present_days"] += 1

            stats["total_overtime_hours"] += r.overtime_hours

        stats["total_overtime_hours"] = round(stats["total_overtime_hours"], 1)
        return stats

    def get_today_summary(self, employee_manager, date: str = None) -> dict:
        """Summary counts (Present, Absent, Leave, Half Day, Late Arrival, Unmarked) for a target date."""
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        daily_records = [r for r in self.attendance_records if r.date == target_date]

        present = sum(1 for r in daily_records if r.status in ["Present", "Late Arrival"])
        absent = sum(1 for r in daily_records if r.status == "Absent")
        leave = sum(1 for r in daily_records if r.status == "Leave")
        half_day = sum(1 for r in daily_records if "half" in r.status.lower())
        late = sum(1 for r in daily_records if "late" in r.status.lower())
        overtime_hours = sum(r.overtime_hours for r in daily_records)

        total_active = employee_manager.count_active() if employee_manager else len(daily_records)
        unmarked = max(0, total_active - len(daily_records))

        return {
            "date": target_date,
            "total_active": total_active,
            "present": present,
            "absent": absent,
            "leave": leave,
            "half_day": half_day,
            "late_arrival": late,
            "unmarked": unmarked,
            "total_overtime_hours": round(overtime_hours, 1)
        }
