"""
Rajby Textile Industries - Employee Payroll Management Server
REST API Endpoints & Static File Routing
Strict OOP Separation: All business logic resides in Manager classes with in-memory Python lists.
"""
import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data import (
    department_manager,
    employee_manager,
    attendance_manager,
    payroll_manager
)

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)


# ==========================================
# Frontend Page Routing
# ==========================================

@app.route("/")
def index():
    """Serve Executive Dashboard."""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    """Serve HTML pages and static assets (CSS, JS, images)."""
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    html_file = f"{path}.html"
    if os.path.exists(os.path.join(FRONTEND_DIR, html_file)):
        return send_from_directory(FRONTEND_DIR, html_file)
    return send_from_directory(FRONTEND_DIR, "index.html")


# ==========================================
# API: Metadata (Shifts & Designations)
# ==========================================

@app.route("/api/config", methods=["GET"])
def get_config():
    """Return company branding and textile operational configurations."""
    return jsonify({
        "status": "success",
        "company": {
            "name": "Rajby Textile Industries",
            "tagline": "Denim & Apparel Manufacturing",
            "industry": "Textile & Denim Manufacturing",
            "city": "Karachi",
            "country": "Pakistan",
            "address": "Plot A/12, S.I.T.E. Area, Karachi - 75700, Pakistan",
            "currency": "PKR",
            "currency_symbol": "Rs.",
            "phone": "+92 (21) 3256-7890",
            "email": "hr@rajby.local",
            "working_days": "Monday - Saturday",
            "weekly_holiday": "Sunday"
        },
        "shifts": [
            {"id": "shift-1", "name": "Morning Shift", "timing": "06:00 AM - 02:00 PM", "hours": 8},
            {"id": "shift-2", "name": "Evening Shift", "timing": "02:00 PM - 10:00 PM", "hours": 8},
            {"id": "shift-3", "name": "Night Shift", "timing": "10:00 PM - 06:00 AM", "hours": 8},
            {"id": "shift-4", "name": "General Office Shift", "timing": "09:00 AM - 06:00 PM", "hours": 9}
        ],
        "designations": [
            "Production Manager",
            "HR Manager",
            "HR Officer",
            "Supervisor",
            "Line Incharge",
            "Machine Operator",
            "Stitching Operator",
            "Cutting Operator",
            "Washing Operator",
            "Quality Inspector",
            "Packing Staff",
            "Helper",
            "Electrician",
            "Maintenance Technician",
            "Store Keeper",
            "Security Guard",
            "Accountant",
            "Senior Merchandiser",
            "Dyeing Master",
            "Industrial Engineer (IE)"
        ],
        "banks": [
            "Meezan Bank Ltd",
            "Habib Bank Limited (HBL)",
            "United Bank Limited (UBL)",
            "MCB Bank Ltd",
            "Bank Alfalah",
            "Standard Chartered Bank",
            "National Bank of Pakistan (NBP)",
            "Habib Metropolitan Bank",
            "Faysal Bank Ltd",
            "Askari Bank Ltd"
        ]
    }), 200


# ==========================================
# API: Dashboard
# ==========================================

@app.route("/api/dashboard", methods=["GET"])
def get_dashboard_data():
    """Retrieve real-time textile operational metrics for executive dashboard in PKR."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    att_summary = attendance_manager.get_today_summary(employee_manager, today_str)
    pay_summary = payroll_manager.get_summary_statistics()

    dept_distribution = []
    for dept in department_manager.departments:
        dept_distribution.append({
            "name": dept.name,
            "count": employee_manager.count_by_department(dept.name)
        })

    return jsonify({
        "status": "success",
        "company": "Rajby Textile Industries, Karachi",
        "currency": "PKR",
        "currency_symbol": "Rs.",
        "stats": {
            "total_employees": employee_manager.count_total(),
            "active_employees": employee_manager.count_active(),
            "inactive_employees": employee_manager.count_inactive(),
            "on_leave_employees": employee_manager.count_on_leave(),
            "total_departments": department_manager.count(),
            "total_monthly_payroll": pay_summary["current_month_total"],
            "pending_payroll": pay_summary["pending_payroll_total"],
            "paid_payroll": pay_summary["paid_payroll_total"],
            "present_employees": att_summary["present"],
            "absent_employees": att_summary["absent"],
            "leave_employees": att_summary["leave"],
            "half_day_employees": att_summary["half_day"],
            "late_arrival_employees": att_summary.get("late_arrival", 0),
            "unmarked_attendance": att_summary["unmarked"],
            "total_overtime_hours": att_summary.get("total_overtime_hours", 0.0)
        },
        "recent_employees": employee_manager.get_recent_employees(5),
        "department_distribution": dept_distribution,
        "payroll_summary": pay_summary,
        "today_attendance": att_summary
    }), 200


# ==========================================
# API: Department Management
# ==========================================

@app.route("/api/departments", methods=["GET"])
def list_departments():
    """List all 18 textile manufacturing departments with employee counts."""
    departments = department_manager.get_all(employee_manager)
    return jsonify({"status": "success", "count": len(departments), "data": departments}), 200


@app.route("/api/departments", methods=["POST"])
def create_department():
    """Add a new department."""
    payload = request.get_json(silent=True) or {}
    name = payload.get("name", "").strip()
    description = payload.get("description", "").strip()

    try:
        new_dept = department_manager.add_department(name=name, description=description)
        return jsonify({
            "status": "success",
            "message": f"Department '{new_dept.name}' created successfully.",
            "data": new_dept.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/departments/<dept_id>", methods=["GET"])
def get_department(dept_id):
    """Get single department details."""
    dept = department_manager.get_by_id(dept_id)
    if not dept:
        return jsonify({"status": "error", "message": f"Department '{dept_id}' not found."}), 404
    data = dept.to_dict()
    data["employee_count"] = employee_manager.count_by_department(dept.name)
    return jsonify({"status": "success", "data": data}), 200


@app.route("/api/departments/<dept_id>", methods=["PUT"])
def update_department(dept_id):
    """Update department name or description."""
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    description = payload.get("description")

    try:
        updated = department_manager.update_department(dept_id, name=name, description=description)
        return jsonify({
            "status": "success",
            "message": f"Department '{updated.name}' updated successfully.",
            "data": updated.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/departments/<dept_id>", methods=["DELETE"])
def delete_department(dept_id):
    """Delete department (restricted if employees are assigned)."""
    try:
        department_manager.delete_department(dept_id, employee_manager)
        return jsonify({
            "status": "success",
            "message": f"Department '{dept_id}' deleted successfully."
        }), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ==========================================
# API: Employee Management
# ==========================================

@app.route("/api/employees", methods=["GET"])
def list_employees():
    """List employees with optional filters (search, department, status, employee_type, shift)."""
    search = request.args.get("search")
    dept = request.args.get("department")
    status = request.args.get("status")
    emp_type = request.args.get("employee_type")
    shift = request.args.get("shift")

    employees = employee_manager.get_all(
        search=search,
        department=dept,
        status=status,
        employee_type=emp_type,
        shift=shift
    )
    return jsonify({"status": "success", "count": len(employees), "data": employees}), 200


@app.route("/api/employees", methods=["POST"])
def create_employee():
    """Add a new textile employee with Pakistani CNIC, shift, and bank details."""
    payload = request.get_json(silent=True) or {}
    try:
        new_emp = employee_manager.add_employee(payload, department_manager)
        return jsonify({
            "status": "success",
            "message": f"Employee '{new_emp.full_name}' ({new_emp.employee_id}) added successfully.",
            "data": new_emp.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/employees/<emp_id>", methods=["GET"])
def get_employee(emp_id):
    """Get single employee profile."""
    emp = employee_manager.get_by_id(emp_id)
    if not emp:
        return jsonify({"status": "error", "message": f"Employee '{emp_id}' not found."}), 404
    return jsonify({"status": "success", "data": emp.to_dict()}), 200


@app.route("/api/employees/<emp_id>", methods=["PUT"])
def update_employee(emp_id):
    """Update employee details."""
    payload = request.get_json(silent=True) or {}
    try:
        updated = employee_manager.update_employee(emp_id, payload, department_manager)
        return jsonify({
            "status": "success",
            "message": f"Employee '{updated.full_name}' updated successfully.",
            "data": updated.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/employees/<emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    """Delete employee record."""
    try:
        employee_manager.delete_employee(emp_id)
        return jsonify({"status": "success", "message": f"Employee '{emp_id}' deleted successfully."}), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ==========================================
# API: Attendance Management
# ==========================================

@app.route("/api/attendance", methods=["POST"])
def mark_attendance():
    """Mark daily attendance with check-in/out, shift, and overtime."""
    payload = request.get_json(silent=True) or {}
    emp_id = payload.get("employee_id")
    date = payload.get("date")
    status = payload.get("status", "Present")
    check_in = payload.get("check_in", "08:00 AM")
    check_out = payload.get("check_out", "05:00 PM")
    overtime_hours = float(payload.get("overtime_hours") or 0.0)
    shift = payload.get("shift")
    remarks = payload.get("remarks", "")

    try:
        record = attendance_manager.mark_attendance(
            employee_id=emp_id,
            date=date,
            status=status,
            check_in=check_in,
            check_out=check_out,
            overtime_hours=overtime_hours,
            shift=shift,
            remarks=remarks,
            employee_manager=employee_manager
        )
        return jsonify({
            "status": "success",
            "message": f"Attendance marked for {record.employee_id} on {record.date} ({record.status}).",
            "data": record.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/attendance", methods=["GET"])
def list_attendance():
    """List attendance with filters (date, month, department, employee_id, status)."""
    date = request.args.get("date")
    month = request.args.get("month")
    dept = request.args.get("department")
    emp_id = request.args.get("employee_id")
    status = request.args.get("status")

    records = attendance_manager.get_attendance_list(
        date=date,
        month=month,
        department=dept,
        employee_id=emp_id,
        status=status,
        employee_manager=employee_manager
    )
    return jsonify({
        "status": "success",
        "count": len(records),
        "data": records
    }), 200


@app.route("/api/attendance/department-report", methods=["GET"])
def department_attendance_report():
    """Department-wise attendance summary for a given date."""
    target_date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    report = attendance_manager.get_department_attendance_report(
        date=target_date,
        employee_manager=employee_manager,
        department_manager=department_manager
    )
    return jsonify({
        "status": "success",
        "date": target_date,
        "data": report
    }), 200


@app.route("/api/attendance/<att_id>", methods=["PUT"])
def update_attendance(att_id):
    """Update attendance status, check-in/out, or overtime."""
    payload = request.get_json(silent=True) or {}
    try:
        updated = attendance_manager.update_attendance(
            attendance_id=att_id,
            status=payload.get("status"),
            check_in=payload.get("check_in"),
            check_out=payload.get("check_out"),
            overtime_hours=payload.get("overtime_hours"),
            shift=payload.get("shift"),
            remarks=payload.get("remarks")
        )
        return jsonify({
            "status": "success",
            "message": f"Attendance record '{att_id}' updated.",
            "data": updated.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/attendance/<att_id>", methods=["DELETE"])
def delete_attendance(att_id):
    """Delete an attendance entry."""
    try:
        attendance_manager.delete_attendance(att_id)
        return jsonify({"status": "success", "message": f"Attendance record '{att_id}' deleted."}), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ==========================================
# API: Payroll Management
# ==========================================

@app.route("/api/payroll/calculate-preview", methods=["GET"])
def preview_payroll():
    """Auto-fetches employee salary and computes suggested components in PKR."""
    emp_id = request.args.get("employee_id")
    month = request.args.get("month", datetime.now().strftime("%Y-%m"))

    if not emp_id:
        return jsonify({"status": "error", "message": "Employee ID is required."}), 400

    emp = employee_manager.get_by_id(emp_id)
    if not emp:
        return jsonify({"status": "error", "message": f"Employee '{emp_id}' not found."}), 404

    existing = payroll_manager.get_by_employee_and_month(emp_id, month)
    is_generated = existing is not None

    calc = payroll_manager.calculate_suggested_components(emp, month, attendance_manager)
    calc["already_generated"] = is_generated
    if is_generated:
        calc["existing_payroll_id"] = existing.payroll_id
        calc["existing_status"] = existing.payment_status

    return jsonify({"status": "success", "data": calc}), 200


@app.route("/api/payroll", methods=["GET"])
def list_payrolls():
    """List monthly payroll records in PKR."""
    month = request.args.get("month")
    dept = request.args.get("department")
    emp_id = request.args.get("employee_id")
    status = request.args.get("status")

    payrolls = payroll_manager.get_all(month=month, department=dept, employee_id=emp_id, status=status)
    return jsonify({
        "status": "success",
        "currency": "PKR",
        "currency_symbol": "Rs.",
        "count": len(payrolls),
        "total_payout": sum(p["net_salary"] for p in payrolls),
        "data": payrolls
    }), 200


@app.route("/api/payroll", methods=["POST"])
def generate_payroll():
    """Generate monthly payroll in PKR. Prevents duplicate for same employee and month."""
    payload = request.get_json(silent=True) or {}
    emp_id = payload.get("employee_id")
    month = payload.get("month")

    try:
        new_payroll = payroll_manager.generate_payroll(
            employee_id=emp_id,
            month=month,
            data=payload,
            employee_manager=employee_manager,
            attendance_manager=attendance_manager
        )
        return jsonify({
            "status": "success",
            "message": f"Payroll generated for {new_payroll.employee_name} ({month}). Net Salary: Rs. {new_payroll.net_salary:,.2f}",
            "data": new_payroll.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/payroll/<payroll_id>", methods=["GET"])
def get_payroll(payroll_id):
    """Get single payroll record (for salary slip view/print/PDF)."""
    p = payroll_manager.get_by_id(payroll_id)
    if not p:
        return jsonify({"status": "error", "message": f"Payroll '{payroll_id}' not found."}), 404

    # Enrich with employee's banking & shift info
    data = p.to_dict()
    emp = employee_manager.get_by_id(p.employee_id)
    if emp:
        data["bank_name"] = emp.bank_name
        data["account_title"] = emp.account_title
        data["account_number_iban"] = emp.account_number_iban
        data["shift"] = emp.shift
        data["employee_type"] = emp.employee_type

    return jsonify({"status": "success", "data": data}), 200


@app.route("/api/payroll/<payroll_id>/status", methods=["PUT"])
def update_payroll_status(payroll_id):
    """Update payroll status: Pending -> Approved -> Paid."""
    payload = request.get_json(silent=True) or {}
    new_status = payload.get("status", "Paid")
    try:
        updated = payroll_manager.update_payroll_status(payroll_id, new_status)
        return jsonify({
            "status": "success",
            "message": f"Payroll '{payroll_id}' status updated to '{updated.payment_status}'.",
            "data": updated.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/payroll/<payroll_id>", methods=["DELETE"])
def delete_payroll(payroll_id):
    """Delete a payroll record."""
    try:
        payroll_manager.delete_payroll(payroll_id)
        return jsonify({"status": "success", "message": f"Payroll '{payroll_id}' deleted."}), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ==========================================
# Main Server Runner
# ==========================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f" * Rajby Textile Industries HR & Payroll System running on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=True)
