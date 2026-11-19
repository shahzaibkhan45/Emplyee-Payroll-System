/**
 * Department Management Controller - Rajby Textile Industries
 * Manages the 18 textile manufacturing departments & staff counts
 */

let allDepartments = [];
let currentEditingDeptId = null;

document.addEventListener('DOMContentLoaded', () => {
  loadDepartments();

  const searchInput = document.getElementById('deptSearchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      const filtered = allDepartments.filter(d => 
        d.name.toLowerCase().includes(q) || 
        d.dept_id.toLowerCase().includes(q) ||
        (d.description && d.description.toLowerCase().includes(q))
      );
      renderDepartmentsTable(filtered);
    });
  }

  const form = document.getElementById('departmentForm');
  if (form) {
    form.addEventListener('submit', handleDepartmentFormSubmit);
  }
});

/**
 * Fetch all departments
 */
async function loadDepartments() {
  try {
    const res = await fetchAPI('/api/departments');
    if (res.status === 'success') {
      allDepartments = res.data;
      renderDepartmentsTable(allDepartments);
    }
  } catch (error) {
    showToast('Failed to load textile departments: ' + error.message, 'danger');
  }
}

/**
 * Render Department Table
 */
function renderDepartmentsTable(departments) {
  const tbody = document.getElementById('departmentsTableBody');
  const countBadge = document.getElementById('deptCountBadge');
  if (countBadge) countBadge.textContent = `${departments.length} Operational Units`;

  if (!tbody) return;

  if (departments.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
          </svg>
          <h4 class="empty-title">No departments found</h4>
          <p class="empty-desc">Create your first department to organize factory floor staff.</p>
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = departments.map(dept => `
    <tr>
      <td>
        <span style="font-family: monospace; font-weight: 800; color: var(--denim);">
          ${escapeHTML(dept.dept_id)}
        </span>
      </td>
      <td>
        <div style="font-weight: 700; color: var(--text-primary); font-size: 13.5px;">${escapeHTML(dept.name)}</div>
      </td>
      <td style="color: var(--text-secondary); max-width: 380px; font-size: 12.5px;">
        ${escapeHTML(dept.description || 'No operational description provided')}
      </td>
      <td>
        <span class="badge ${dept.employee_count > 0 ? 'badge-denim' : 'badge-neutral'}">
          <svg style="width: 12px; height: 12px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          ${dept.employee_count} Assigned
        </span>
      </td>
      <td>
        <div class="table-actions">
          <button class="action-btn edit-btn" title="Edit Department" onclick="openEditDepartmentModal('${dept.dept_id}')">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          </button>
          <button class="action-btn delete-btn" title="Delete Department" onclick="confirmDeleteDepartment('${dept.dept_id}', '${escapeHTML(dept.name)}', ${dept.employee_count})">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </td>
    </tr>
  `).join('');
}

/**
 * Open Modal to Add Department
 */
function openAddDepartmentModal() {
  currentEditingDeptId = null;
  const form = document.getElementById('departmentForm');
  if (form) form.reset();

  document.getElementById('deptModalTitle').textContent = 'Add Textile Department';
  document.getElementById('deptSubmitBtn').textContent = 'Save Department';
  openModal('departmentModal');
}

/**
 * Open Modal to Edit Department
 */
async function openEditDepartmentModal(deptId) {
  currentEditingDeptId = deptId;
  try {
    const res = await fetchAPI(`/api/departments/${deptId}`);
    if (res.status === 'success') {
      const dept = res.data;
      document.getElementById('deptModalTitle').textContent = `Edit Department: ${dept.name}`;
      document.getElementById('deptSubmitBtn').textContent = 'Update Department';

      document.getElementById('deptName').value = dept.name;
      document.getElementById('deptDescription').value = dept.description || '';

      openModal('departmentModal');
    }
  } catch (error) {
    showToast('Failed to fetch department details: ' + error.message, 'danger');
  }
}

/**
 * Handle Department Form Submit
 */
async function handleDepartmentFormSubmit(e) {
  e.preventDefault();

  const payload = {
    name: document.getElementById('deptName').value.trim(),
    description: document.getElementById('deptDescription').value.trim()
  };

  try {
    if (currentEditingDeptId) {
      const res = await fetchAPI(`/api/departments/${currentEditingDeptId}`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      showToast(res.message, 'success');
    } else {
      const res = await fetchAPI('/api/departments', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      showToast(res.message, 'success');
    }

    closeModal('departmentModal');
    loadDepartments();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

/**
 * Confirm and Delete Department
 */
function confirmDeleteDepartment(deptId, deptName, employeeCount) {
  if (employeeCount > 0) {
    showToast(`Cannot delete department "${deptName}" because it currently has ${employeeCount} assigned staff member(s). Please reassign them first.`, 'warning', 6000);
    return;
  }

  showConfirmDialog(
    'Delete Department',
    `Are you sure you want to delete the "${deptName}" department (${deptId})?`,
    'Delete Department',
    async () => {
      try {
        const res = await fetchAPI(`/api/departments/${deptId}`, { method: 'DELETE' });
        showToast(res.message, 'success');
        loadDepartments();
      } catch (error) {
        showToast(error.message, 'danger');
      }
    }
  );
}
