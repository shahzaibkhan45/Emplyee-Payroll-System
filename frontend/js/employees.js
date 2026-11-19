/**
 * Employee Management Controller - Rajby Textile Industries
 * Pakistani Textile Workforce CRUD, CNIC Formatting & Modal Scrolling Controller
 */

let allEmployees = [];
let departmentsList = [];
let currentEditingId = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadConfigDropdowns();
  loadEmployees();

  // Search & Filters Listeners
  const searchInput = document.getElementById('employeeSearchInput');
  const deptFilter = document.getElementById('employeeDeptFilter');
  const statusFilter = document.getElementById('employeeStatusFilter');
  const shiftFilter = document.getElementById('employeeShiftFilter');
  const typeFilter = document.getElementById('employeeTypeFilter');

  if (searchInput) searchInput.addEventListener('input', debounce(loadEmployees, 300));
  if (deptFilter) deptFilter.addEventListener('change', loadEmployees);
  if (statusFilter) statusFilter.addEventListener('change', loadEmployees);
  if (shiftFilter) shiftFilter.addEventListener('change', loadEmployees);
  if (typeFilter) typeFilter.addEventListener('change', loadEmployees);

  // Form Submit Listener
  const empForm = document.getElementById('employeeForm');
  if (empForm) {
    empForm.addEventListener('submit', handleEmployeeFormSubmit);
  }

  // CNIC input auto-formatter
  const cnicInput = document.getElementById('empCnic');
  if (cnicInput) {
    cnicInput.addEventListener('input', (e) => {
      e.target.value = formatCNICInput(e.target.value);
    });
  }
});

function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

/**
 * Load Departments, Shifts, and Banks into form & filter dropdowns
 */
async function loadConfigDropdowns() {
  try {
    const [deptRes, configRes] = await Promise.all([
      fetchAPI('/api/departments'),
      fetchAPI('/api/config')
    ]);

    if (deptRes.status === 'success') {
      departmentsList = deptRes.data;

      // Filter select
      const filterDept = document.getElementById('employeeDeptFilter');
      if (filterDept) {
        filterDept.innerHTML = '<option value="">All Departments</option>' +
          departmentsList.map(d => `<option value="${escapeHTML(d.name)}">${escapeHTML(d.name)}</option>`).join('');
      }

      // Modal select
      const modalDept = document.getElementById('empDepartment');
      if (modalDept) {
        modalDept.innerHTML = '<option value="">Select Department</option>' +
          departmentsList.map(d => `<option value="${escapeHTML(d.name)}">${escapeHTML(d.name)}</option>`).join('');
      }
    }

    if (configRes.status === 'success') {
      const { shifts, designations, banks } = configRes;

      // Shifts in filter & modal
      const filterShift = document.getElementById('employeeShiftFilter');
      if (filterShift) {
        filterShift.innerHTML = '<option value="">All Shifts</option>' +
          shifts.map(s => `<option value="${s.name}">${s.name} (${s.timing})</option>`).join('');
      }

      const modalShift = document.getElementById('empShift');
      if (modalShift) {
        modalShift.innerHTML = shifts.map(s => `<option value="${s.name}">${s.name} (${s.timing})</option>`).join('');
      }

      // Designations datalist or select
      const desigList = document.getElementById('designationDatalist');
      if (desigList && designations) {
        desigList.innerHTML = designations.map(d => `<option value="${escapeHTML(d)}">`).join('');
      }

      // Banks in modal
      const modalBank = document.getElementById('empBankName');
      if (modalBank && banks) {
        modalBank.innerHTML = banks.map(b => `<option value="${b}">${b}</option>`).join('');
      }
    }
  } catch (error) {
    console.error('Error loading configuration dropdowns:', error);
  }
}

/**
 * Load and render employees
 */
async function loadEmployees() {
  const search = document.getElementById('employeeSearchInput')?.value.trim() || '';
  const dept = document.getElementById('employeeDeptFilter')?.value || '';
  const status = document.getElementById('employeeStatusFilter')?.value || '';
  const shift = document.getElementById('employeeShiftFilter')?.value || '';
  const empType = document.getElementById('employeeTypeFilter')?.value || '';

  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (dept) params.append('department', dept);
  if (status) params.append('status', status);
  if (shift) params.append('shift', shift);
  if (empType) params.append('employee_type', empType);

  try {
    const res = await fetchAPI(`/api/employees?${params.toString()}`);
    if (res.status === 'success') {
      allEmployees = res.data;
      renderEmployeeTable(allEmployees);
    }
  } catch (error) {
    showToast('Failed to load textile workforce: ' + error.message, 'danger');
  }
}

/**
 * Render Employee Table
 */
function renderEmployeeTable(employees) {
  const tbody = document.getElementById('employeesTableBody');
  const countBadge = document.getElementById('employeeCountBadge');
  if (countBadge) countBadge.textContent = `${employees.length} Staff Members`;

  if (!tbody) return;

  if (employees.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          <h4 class="empty-title">No employees found</h4>
          <p class="empty-desc">No records match the current filter criteria.</p>
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = employees.map(emp => `
    <tr>
      <td>
        <span style="font-family: monospace; font-weight: 800; color: var(--denim);">
          ${escapeHTML(emp.employee_id)}
        </span>
      </td>
      <td>
        <div style="font-weight: 700; color: var(--text-primary);">${escapeHTML(emp.full_name)}</div>
        <div style="font-size: 11px; color: var(--text-muted);">
          S/D/W of: ${escapeHTML(emp.father_name || 'N/A')}
        </div>
      </td>
      <td>
        <span style="font-family: monospace; font-size: 12px; font-weight: 600; color: #1e3a8a;">
          ${escapeHTML(emp.cnic || 'N/A')}
        </span>
        <div style="font-size: 11px; color: var(--text-muted);">${escapeHTML(emp.phone)}</div>
      </td>
      <td>
        <span class="badge badge-neutral">${escapeHTML(emp.department)}</span>
      </td>
      <td>
        <div style="font-weight: 500;">${escapeHTML(emp.designation)}</div>
        <div style="font-size: 11px; color: var(--text-muted);">${escapeHTML(emp.employee_type)}</div>
      </td>
      <td>
        <span class="badge badge-denim">${escapeHTML(emp.shift)}</span>
      </td>
      <td>
        <span class="badge ${getStatusBadgeClass(emp.status)}">
          <span class="badge-dot"></span>
          ${escapeHTML(emp.status)}
        </span>
      </td>
      <td style="font-weight: 700; color: var(--primary);">
        ${formatPKR(emp.basic_salary)}
      </td>
      <td>
        <div class="table-actions">
          <button class="action-btn view-btn" title="View Detailed Profile" onclick="viewEmployeeProfile('${emp.employee_id}')">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
          </button>
          <button class="action-btn edit-btn" title="Edit Employee" onclick="openEditEmployeeModal('${emp.employee_id}')">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          </button>
          <button class="action-btn delete-btn" title="Delete Employee" onclick="confirmDeleteEmployee('${emp.employee_id}', '${escapeHTML(emp.full_name)}')">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

function getStatusBadgeClass(status) {
  const st = (status || '').toLowerCase();
  if (st === 'active') return 'badge-success';
  if (st === 'inactive' || st === 'terminated') return 'badge-danger';
  if (st === 'on leave') return 'badge-warning';
  return 'badge-neutral';
}

/**
 * Open Modal to Add New Employee
 */
function openAddEmployeeModal() {
  currentEditingId = null;
  const form = document.getElementById('employeeForm');
  if (form) form.reset();

  document.getElementById('empModalTitle').textContent = 'Register New Employee - Rajby Textiles';
  document.getElementById('empSubmitBtn').textContent = 'Save Employee Record';
  
  // Set defaults
  document.getElementById('empCity').value = 'Karachi';
  document.getElementById('empStatus').value = 'Active';
  document.getElementById('empType').value = 'Permanent';
  document.getElementById('empJoiningDate').value = new Date().toISOString().split('T')[0];

  openModal('employeeModal');
}

/**
 * Open Modal to Edit Employee
 */
async function openEditEmployeeModal(empId) {
  currentEditingId = empId;
  try {
    const res = await fetchAPI(`/api/employees/${empId}`);
    if (res.status === 'success') {
      const emp = res.data;
      document.getElementById('empModalTitle').textContent = `Edit Employee: ${emp.full_name} (${emp.employee_id})`;
      document.getElementById('empSubmitBtn').textContent = 'Update Record';

      // Personal
      document.getElementById('empFullName').value = emp.full_name || '';
      document.getElementById('empFatherName').value = emp.father_name || '';
      document.getElementById('empCnic').value = emp.cnic || '';
      document.getElementById('empPhone').value = emp.phone || '';
      document.getElementById('empEmail').value = emp.email || '';
      document.getElementById('empGender').value = emp.gender || 'Male';
      document.getElementById('empDob').value = emp.dob || '';
      document.getElementById('empAddress').value = emp.address || '';
      document.getElementById('empCity').value = emp.city || 'Karachi';
      document.getElementById('empEmergencyContact').value = emp.emergency_contact || '';

      // Job
      document.getElementById('empDepartment').value = emp.department || '';
      document.getElementById('empDesignation').value = emp.designation || '';
      document.getElementById('empType').value = emp.employee_type || 'Permanent';
      document.getElementById('empJoiningDate').value = emp.joining_date || '';
      document.getElementById('empStatus').value = emp.status || 'Active';
      document.getElementById('empShift').value = emp.shift || 'General Office Shift';

      // Compensation & Banking
      document.getElementById('empBasicSalary').value = emp.basic_salary || 0;
      document.getElementById('empBankName').value = emp.bank_name || 'Meezan Bank Ltd';
      document.getElementById('empAccountTitle').value = emp.account_title || '';
      document.getElementById('empAccountNumber').value = emp.account_number_iban || '';

      openModal('employeeModal');
    }
  } catch (error) {
    showToast('Failed to load employee details: ' + error.message, 'danger');
  }
}

/**
 * Handle Employee Form Submit (Create or Update)
 */
async function handleEmployeeFormSubmit(e) {
  e.preventDefault();

  const cnicVal = document.getElementById('empCnic').value.trim();
  const cnicPattern = /^\d{5}-\d{7}-\d{1}$/;
  if (!cnicPattern.test(cnicVal)) {
    showToast('Invalid Pakistani CNIC format! Must be 13 digits: 42101-1234567-1', 'danger');
    document.getElementById('empCnic').focus();
    return;
  }

  const payload = {
    full_name: document.getElementById('empFullName').value.trim(),
    father_name: document.getElementById('empFatherName').value.trim(),
    cnic: cnicVal,
    phone: document.getElementById('empPhone').value.trim(),
    email: document.getElementById('empEmail').value.trim(),
    gender: document.getElementById('empGender').value,
    dob: document.getElementById('empDob').value,
    address: document.getElementById('empAddress').value.trim(),
    city: document.getElementById('empCity').value.trim() || 'Karachi',
    emergency_contact: document.getElementById('empEmergencyContact').value.trim(),
    department: document.getElementById('empDepartment').value,
    designation: document.getElementById('empDesignation').value.trim(),
    employee_type: document.getElementById('empType').value,
    joining_date: document.getElementById('empJoiningDate').value,
    status: document.getElementById('empStatus').value,
    shift: document.getElementById('empShift').value,
    basic_salary: parseFloat(document.getElementById('empBasicSalary').value) || 0,
    bank_name: document.getElementById('empBankName').value,
    account_title: document.getElementById('empAccountTitle').value.trim(),
    account_number_iban: document.getElementById('empAccountNumber').value.trim()
  };

  try {
    if (currentEditingId) {
      const res = await fetchAPI(`/api/employees/${currentEditingId}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      showToast(res.message, 'success');
    } else {
      const res = await fetchAPI('/api/employees', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      showToast(res.message, 'success');
    }

    closeModal('employeeModal');
    loadEmployees();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

/**
 * Confirm and Delete Employee
 */
function confirmDeleteEmployee(empId, empName) {
  showConfirmDialog(
    'Delete Employee Record',
    `Are you sure you want to permanently delete staff member "${empName}" (${empId}) from Rajby Textile Industries?`,
    'Delete Record',
    async () => {
      try {
        const res = await fetchAPI(`/api/employees/${empId}`, { method: 'DELETE' });
        showToast(res.message, 'success');
        loadEmployees();
      } catch (error) {
        showToast(error.message, 'danger');
      }
    }
  );
}

/**
 * View Detailed Pakistani Textile Profile Modal
 */
async function viewEmployeeProfile(empId) {
  try {
    const res = await fetchAPI(`/api/employees/${empId}`);
    if (res.status === 'success') {
      const emp = res.data;
      const content = document.getElementById('employeeDetailsContent');
      if (content) {
        content.innerHTML = `
          <div style="display: flex; align-items: center; gap: 16px; padding-bottom: 20px; border-bottom: 1.5px solid var(--border-color); margin-bottom: 20px;">
            <div class="user-avatar" style="width: 60px; height: 60px; font-size: 22px; font-weight: 800;">
              ${escapeHTML(emp.full_name.charAt(0))}
            </div>
            <div>
              <h3 style="font-size: 18px; font-weight: 800; color: var(--text-primary);">${escapeHTML(emp.full_name)}</h3>
              <p style="font-size: 13px; color: var(--text-secondary); margin-top: 2px;">
                ${escapeHTML(emp.designation)} &bull; ${escapeHTML(emp.department)}
              </p>
              <div style="display: flex; gap: 6px; margin-top: 8px;">
                <span class="badge ${getStatusBadgeClass(emp.status)}">
                  <span class="badge-dot"></span>
                  ${escapeHTML(emp.status)}
                </span>
                <span class="badge badge-denim">ID: ${escapeHTML(emp.employee_id)}</span>
                <span class="badge badge-neutral">${escapeHTML(emp.employee_type)}</span>
              </div>
            </div>
          </div>

          <!-- Personal Information Section -->
          <div class="form-section-heading">Personal & Identification</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; margin-bottom: 18px;">
            <div>
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Father's Name</span>
              <strong>${escapeHTML(emp.father_name || 'N/A')}</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Pakistani CNIC</span>
              <strong style="color: #1e3a8a; font-family: monospace;">${escapeHTML(emp.cnic || 'N/A')}</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Phone Number</span>
              <strong>${escapeHTML(emp.phone)}</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Emergency Contact</span>
              <strong>${escapeHTML(emp.emergency_contact || 'N/A')}</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Date of Birth</span>
              <strong>${formatDate(emp.dob)}</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Gender</span>
              <strong>${escapeHTML(emp.gender)}</strong>
            </div>
            <div style="grid-column: 1 / -1;">
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Residential Address</span>
              <strong>${escapeHTML(emp.address || 'N/A')}, ${escapeHTML(emp.city || 'Karachi')}</strong>
            </div>
          </div>

          <!-- Organizational Details -->
          <div class="form-section-heading">Factory Floor & Shift Assignment</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; margin-bottom: 18px;">
            <div>
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Assigned Shift</span>
              <strong style="color: var(--denim);">${escapeHTML(emp.shift)}</strong>
            </div>
            <div>
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Joining Date</span>
              <strong>${formatDate(emp.joining_date)}</strong>
            </div>
          </div>

          <!-- Compensation & Banking -->
          <div class="form-section-heading">Salary & Bank Account (PKR)</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px;">
            <div style="background: #f1f5f9; padding: 10px 14px; border-radius: 8px;">
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Basic Salary (PKR)</span>
              <strong style="font-size: 17px; color: var(--primary);">${formatPKR(emp.basic_salary)}</strong>
            </div>
            <div style="background: #f1f5f9; padding: 10px 14px; border-radius: 8px;">
              <span style="color: var(--text-muted); font-size: 11px; display: block;">Bank Name</span>
              <strong style="color: var(--text-primary);">${escapeHTML(emp.bank_name || 'N/A')}</strong>
            </div>
            <div style="grid-column: 1 / -1;">
              <span style="color: var(--text-muted); font-size: 11px; display: block;">IBAN / Account Number</span>
              <strong style="font-family: monospace; letter-spacing: 0.05em;">${escapeHTML(emp.account_number_iban || 'N/A')}</strong>
            </div>
          </div>
        `;
        openModal('employeeDetailsModal');
      }
    }
  } catch (error) {
    showToast('Failed to load employee profile: ' + error.message, 'danger');
  }
}
