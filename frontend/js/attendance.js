/**
 * Attendance Management Controller - Rajby Textile Industries
 * Factory Floor Biometric Logging, Check-in/out, Shifts, Overtime & Department Audit
 */

let activeEmployeesList = [];
let departmentsList = [];
let currentViewMode = 'daily'; // 'daily', 'monthly', 'department'
let currentEditingAttId = null;

document.addEventListener('DOMContentLoaded', () => {
  const today = new Date().toISOString().split('T')[0];
  const currentMonth = today.substring(0, 7);

  const dailyDateInput = document.getElementById('attendanceDailyDate');
  if (dailyDateInput) dailyDateInput.value = today;

  const monthlyInput = document.getElementById('attendanceMonthFilter');
  if (monthlyInput) monthlyInput.value = currentMonth;

  const formDateInput = document.getElementById('attDate');
  if (formDateInput) formDateInput.value = today;

  loadInitialDropdowns();
  loadDailyAttendance();

  // Filter Listeners
  if (dailyDateInput) {
    dailyDateInput.addEventListener('change', () => {
      if (currentViewMode === 'daily') loadDailyAttendance();
      else if (currentViewMode === 'department') loadDepartmentReport();
    });
  }

  const deptFilter = document.getElementById('attendanceDeptFilter');
  if (deptFilter) {
    deptFilter.addEventListener('change', () => {
      if (currentViewMode === 'daily') loadDailyAttendance();
      else if (currentViewMode === 'monthly') loadMonthlyAttendance();
    });
  }

  const statusFilter = document.getElementById('attendanceStatusFilter');
  if (statusFilter) {
    statusFilter.addEventListener('change', () => {
      if (currentViewMode === 'daily') loadDailyAttendance();
      else if (currentViewMode === 'monthly') loadMonthlyAttendance();
    });
  }

  const monthFilter = document.getElementById('attendanceMonthFilter');
  const empFilter = document.getElementById('attendanceEmpFilter');
  if (monthFilter) monthFilter.addEventListener('change', () => {
    if (currentViewMode === 'monthly') loadMonthlyAttendance();
  });
  if (empFilter) empFilter.addEventListener('change', () => {
    if (currentViewMode === 'monthly') loadMonthlyAttendance();
  });

  // Form submit
  const form = document.getElementById('attendanceForm');
  if (form) form.addEventListener('submit', handleAttendanceFormSubmit);
});

/**
 * Load Employees & Departments for filter/modal selectors
 */
async function loadInitialDropdowns() {
  try {
    const [empRes, deptRes] = await Promise.all([
      fetchAPI('/api/employees?status=Active'),
      fetchAPI('/api/departments')
    ]);

    if (empRes.status === 'success') {
      activeEmployeesList = empRes.data;

      const empFilter = document.getElementById('attendanceEmpFilter');
      if (empFilter) {
        empFilter.innerHTML = '<option value="">All Employees</option>' +
          activeEmployeesList.map(e => `<option value="${e.employee_id}">${escapeHTML(e.full_name)} (${e.employee_id})</option>`).join('');
      }

      const modalEmp = document.getElementById('attEmployeeId');
      if (modalEmp) {
        modalEmp.innerHTML = '<option value="">Select Employee</option>' +
          activeEmployeesList.map(e => `<option value="${e.employee_id}" data-shift="${e.shift}">${escapeHTML(e.full_name)} (${e.employee_id}) - ${e.department}</option>`).join('');

        modalEmp.addEventListener('change', (e) => {
          const selectedOption = e.target.selectedOptions[0];
          if (selectedOption && selectedOption.dataset.shift) {
            const shiftSelect = document.getElementById('attShift');
            if (shiftSelect) shiftSelect.value = selectedOption.dataset.shift;
          }
        });
      }
    }

    if (deptRes.status === 'success') {
      departmentsList = deptRes.data;
      const deptFilter = document.getElementById('attendanceDeptFilter');
      if (deptFilter) {
        deptFilter.innerHTML = '<option value="">All Departments</option>' +
          departmentsList.map(d => `<option value="${escapeHTML(d.name)}">${escapeHTML(d.name)}</option>`).join('');
      }
    }
  } catch (error) {
    console.error('Error loading dropdowns:', error);
  }
}

/**
 * Switch tabs: Daily Log vs Monthly Log vs Department Audit
 */
function switchAttendanceView(mode) {
  currentViewMode = mode;
  const dailyControls = document.getElementById('dailyControls');
  const monthlyControls = document.getElementById('monthlyControls');
  const tableContainer = document.getElementById('attendanceTableContainer');
  const deptReportContainer = document.getElementById('deptReportContainer');

  const btnDaily = document.getElementById('tabDailyBtn');
  const btnMonthly = document.getElementById('tabMonthlyBtn');
  const btnDept = document.getElementById('tabDeptBtn');

  // Reset button states
  [btnDaily, btnMonthly, btnDept].forEach(b => {
    if (b) {
      b.classList.remove('active', 'btn-primary');
      b.classList.add('btn-secondary');
    }
  });

  if (mode === 'daily') {
    dailyControls.style.display = 'flex';
    monthlyControls.style.display = 'none';
    tableContainer.style.display = 'block';
    deptReportContainer.style.display = 'none';
    btnDaily.classList.add('active', 'btn-primary');
    btnDaily.classList.remove('btn-secondary');
    loadDailyAttendance();
  } else if (mode === 'monthly') {
    dailyControls.style.display = 'none';
    monthlyControls.style.display = 'flex';
    tableContainer.style.display = 'block';
    deptReportContainer.style.display = 'none';
    btnMonthly.classList.add('active', 'btn-primary');
    btnMonthly.classList.remove('btn-secondary');
    loadMonthlyAttendance();
  } else if (mode === 'department') {
    dailyControls.style.display = 'flex';
    monthlyControls.style.display = 'none';
    tableContainer.style.display = 'none';
    deptReportContainer.style.display = 'block';
    btnDept.classList.add('active', 'btn-primary');
    btnDept.classList.remove('btn-secondary');
    loadDepartmentReport();
  }
}

/**
 * Load Daily Attendance
 */
async function loadDailyAttendance() {
  const date = document.getElementById('attendanceDailyDate')?.value || new Date().toISOString().split('T')[0];
  const dept = document.getElementById('attendanceDeptFilter')?.value || '';
  const status = document.getElementById('attendanceStatusFilter')?.value || '';

  const params = new URLSearchParams({ date });
  if (dept) params.append('department', dept);
  if (status) params.append('status', status);

  try {
    const res = await fetchAPI(`/api/attendance?${params.toString()}`);
    if (res.status === 'success') {
      updateAttendanceMetricBadges(res.data);
      renderAttendanceTable(res.data);
    }
  } catch (error) {
    showToast('Failed to load daily attendance: ' + error.message, 'danger');
  }
}

/**
 * Load Monthly Attendance
 */
async function loadMonthlyAttendance() {
  const month = document.getElementById('attendanceMonthFilter')?.value || new Date().toISOString().substring(0, 7);
  const empId = document.getElementById('attendanceEmpFilter')?.value || '';
  const dept = document.getElementById('attendanceDeptFilter')?.value || '';
  const status = document.getElementById('attendanceStatusFilter')?.value || '';

  const params = new URLSearchParams({ month });
  if (empId) params.append('employee_id', empId);
  if (dept) params.append('department', dept);
  if (status) params.append('status', status);

  try {
    const res = await fetchAPI(`/api/attendance?${params.toString()}`);
    if (res.status === 'success') {
      updateAttendanceMetricBadges(res.data);
      renderAttendanceTable(res.data);
    }
  } catch (error) {
    showToast('Failed to load monthly attendance: ' + error.message, 'danger');
  }
}

/**
 * Load Department-wise Attendance Report
 */
async function loadDepartmentReport() {
  const date = document.getElementById('attendanceDailyDate')?.value || new Date().toISOString().split('T')[0];
  try {
    const res = await fetchAPI(`/api/attendance/department-report?date=${date}`);
    if (res.status === 'success') {
      renderDepartmentReportTable(res.data, date);
    }
  } catch (error) {
    showToast('Failed to load department audit: ' + error.message, 'danger');
  }
}

function updateAttendanceMetricBadges(records) {
  const present = records.filter(r => ['present', 'late arrival'].includes(r.status.toLowerCase())).length;
  const absent = records.filter(r => r.status.toLowerCase() === 'absent').length;
  const leave = records.filter(r => r.status.toLowerCase() === 'leave').length;
  const halfDay = records.filter(r => r.status.toLowerCase().includes('half')).length;
  const late = records.filter(r => r.status.toLowerCase().includes('late')).length;
  const otHours = records.reduce((sum, r) => sum + (parseFloat(r.overtime_hours) || 0), 0);

  setText('attMetricPresent', present);
  setText('attMetricAbsent', absent);
  setText('attMetricLeave', leave);
  setText('attMetricHalfDay', halfDay);
  setText('attMetricLate', late);
  setText('attMetricOT', otHours.toFixed(1) + ' hrs');
}

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

/**
 * Render Attendance Table
 */
function renderAttendanceTable(records) {
  const tbody = document.getElementById('attendanceTableBody');
  const countBadge = document.getElementById('attendanceCountBadge');
  if (countBadge) countBadge.textContent = `${records.length} Records`;

  if (!tbody) return;

  if (records.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="9" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          <h4 class="empty-title">No attendance records found</h4>
          <p class="empty-desc">Click "Mark Attendance" to log check-in/out or select another date.</p>
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = records.map(rec => {
    let badgeClass = 'badge-success';
    const st = rec.status.toLowerCase();
    if (st === 'absent') badgeClass = 'badge-danger';
    else if (st === 'leave') badgeClass = 'badge-warning';
    else if (st.includes('half')) badgeClass = 'badge-info';
    else if (st.includes('late')) badgeClass = 'badge-warning';

    return `
      <tr>
        <td>
          <span style="font-family: monospace; font-weight: 700; color: var(--denim);">
            ${escapeHTML(rec.attendance_id)}
          </span>
        </td>
        <td>
          <div style="font-weight: 700;">${escapeHTML(rec.employee_name || 'N/A')}</div>
          <div style="font-size: 11px; color: var(--text-muted); font-family: monospace;">
            ${escapeHTML(rec.employee_id)} &bull; ${escapeHTML(rec.cnic || '')}
          </div>
        </td>
        <td>
          <span class="badge badge-neutral">${escapeHTML(rec.department || 'N/A')}</span>
        </td>
        <td style="font-weight: 600;">${formatDate(rec.date)}</td>
        <td>
          <span style="font-size: 11.5px; font-weight: 600;">${escapeHTML(rec.check_in || '-')}</span> &rarr;
          <span style="font-size: 11.5px; font-weight: 600;">${escapeHTML(rec.check_out || '-')}</span>
        </td>
        <td>
          <span class="badge badge-denim">${escapeHTML(rec.shift || 'General')}</span>
        </td>
        <td>
          <span class="badge ${badgeClass}">
            <span class="badge-dot"></span>
            ${escapeHTML(rec.status)}
          </span>
        </td>
        <td style="font-weight: 700; color: ${rec.overtime_hours > 0 ? '#059669' : 'var(--text-muted)'};">
          ${rec.overtime_hours > 0 ? `+${rec.overtime_hours} hrs` : '-'}
        </td>
        <td>
          <div class="table-actions">
            <button class="action-btn edit-btn" title="Edit Entry" onclick="openEditAttendanceModal('${rec.attendance_id}', '${rec.status}', '${rec.check_in}', '${rec.check_out}', ${rec.overtime_hours}, '${rec.shift}', '${escapeHTML(rec.remarks || '')}')">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            </button>
            <button class="action-btn delete-btn" title="Delete Entry" onclick="confirmDeleteAttendance('${rec.attendance_id}')">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

/**
 * Render Department-wise Attendance Audit Table
 */
function renderDepartmentReportTable(data, date) {
  const tbody = document.getElementById('deptReportTableBody');
  const title = document.getElementById('deptReportTitle');
  if (title) title.textContent = `Department-wise Attendance Audit (${formatDate(date)})`;

  if (!tbody) return;

  tbody.innerHTML = data.map(d => `
    <tr>
      <td style="font-weight: 700; color: var(--text-primary);">${escapeHTML(d.department_name)}</td>
      <td style="font-weight: 600;">${d.total_staff}</td>
      <td style="color: #059669; font-weight: 700;">${d.present}</td>
      <td style="color: #dc2626; font-weight: 700;">${d.absent}</td>
      <td style="color: #0284c7; font-weight: 600;">${d.half_day}</td>
      <td style="color: #d97706; font-weight: 600;">${d.leave}</td>
      <td style="color: var(--text-muted);">${d.unmarked}</td>
      <td style="color: var(--denim); font-weight: 700;">${d.overtime_hours > 0 ? d.overtime_hours + ' hrs' : '-'}</td>
    </tr>
  `).join('');
}

/**
 * Open Modal to Mark New Attendance
 */
function openMarkAttendanceModal() {
  currentEditingAttId = null;
  const form = document.getElementById('attendanceForm');
  if (form) form.reset();

  document.getElementById('attDate').value = new Date().toISOString().split('T')[0];
  document.getElementById('attEmployeeGroup').style.display = 'block';
  document.getElementById('attDateGroup').style.display = 'block';
  document.getElementById('attCheckIn').value = '08:00 AM';
  document.getElementById('attCheckOut').value = '05:00 PM';
  document.getElementById('attOvertimeHours').value = 0.0;

  document.getElementById('attModalTitle').textContent = 'Mark Factory Attendance';
  document.getElementById('attSubmitBtn').textContent = 'Save Attendance Entry';
  openModal('attendanceModal');
}

/**
 * Open Modal to Edit Attendance
 */
function openEditAttendanceModal(attId, currentStatus, inTime, outTime, otHours, shift, remarks) {
  currentEditingAttId = attId;
  document.getElementById('attModalTitle').textContent = `Edit Attendance (${attId})`;
  document.getElementById('attSubmitBtn').textContent = 'Update Attendance';

  document.getElementById('attEmployeeGroup').style.display = 'none';
  document.getElementById('attDateGroup').style.display = 'none';

  document.getElementById('attStatus').value = currentStatus;
  document.getElementById('attCheckIn').value = inTime;
  document.getElementById('attCheckOut').value = outTime;
  document.getElementById('attOvertimeHours').value = otHours || 0.0;
  document.getElementById('attShift').value = shift;
  document.getElementById('attRemarks').value = remarks || '';

  openModal('attendanceModal');
}

/**
 * Handle Attendance Submit
 */
async function handleAttendanceFormSubmit(e) {
  e.preventDefault();

  try {
    if (currentEditingAttId) {
      const payload = {
        status: document.getElementById('attStatus').value,
        check_in: document.getElementById('attCheckIn').value.trim(),
        check_out: document.getElementById('attCheckOut').value.trim(),
        overtime_hours: parseFloat(document.getElementById('attOvertimeHours').value) || 0.0,
        shift: document.getElementById('attShift').value,
        remarks: document.getElementById('attRemarks').value.trim()
      };
      const res = await fetchAPI(`/api/attendance/${currentEditingAttId}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      showToast(res.message, 'success');
    } else {
      const payload = {
        employee_id: document.getElementById('attEmployeeId').value,
        date: document.getElementById('attDate').value,
        status: document.getElementById('attStatus').value,
        check_in: document.getElementById('attCheckIn').value.trim(),
        check_out: document.getElementById('attCheckOut').value.trim(),
        overtime_hours: parseFloat(document.getElementById('attOvertimeHours').value) || 0.0,
        shift: document.getElementById('attShift').value,
        remarks: document.getElementById('attRemarks').value.trim()
      };
      const res = await fetchAPI('/api/attendance', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      showToast(res.message, 'success');
    }

    closeModal('attendanceModal');
    if (currentViewMode === 'daily') loadDailyAttendance();
    else if (currentViewMode === 'monthly') loadMonthlyAttendance();
    else loadDepartmentReport();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

/**
 * Confirm and Delete Attendance
 */
function confirmDeleteAttendance(attId) {
  showConfirmDialog(
    'Delete Attendance Record',
    `Are you sure you want to delete attendance record ${attId}?`,
    'Delete Entry',
    async () => {
      try {
        const res = await fetchAPI(`/api/attendance/${attId}`, { method: 'DELETE' });
        showToast(res.message, 'success');
        if (currentViewMode === 'daily') loadDailyAttendance();
        else if (currentViewMode === 'monthly') loadMonthlyAttendance();
        else loadDepartmentReport();
      } catch (error) {
        showToast(error.message, 'danger');
      }
    }
  );
}
