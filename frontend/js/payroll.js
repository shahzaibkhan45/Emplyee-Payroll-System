/**
 * Payroll Management Controller - Rajby Textile Industries
 * Pakistani Textile Industry Compensation, EOBI, SESSI, Overtime, & Deductions Engine
 */

let activeEmployeesList = [];
let allDepartments = [];
let allPayrolls = [];

document.addEventListener('DOMContentLoaded', () => {
  const today = new Date().toISOString().split('T')[0];
  const currentMonth = today.substring(0, 7);

  const monthFilter = document.getElementById('payrollMonthFilter');
  if (monthFilter) monthFilter.value = currentMonth;

  const modalMonth = document.getElementById('payMonth');
  if (modalMonth) modalMonth.value = currentMonth;

  const paymentDate = document.getElementById('payDate');
  if (paymentDate) paymentDate.value = today;

  loadInitialDropdowns();
  loadPayrolls();

  // Filter Listeners
  if (monthFilter) monthFilter.addEventListener('change', loadPayrolls);
  const deptFilter = document.getElementById('payrollDeptFilter');
  if (deptFilter) deptFilter.addEventListener('change', loadPayrolls);
  const empFilter = document.getElementById('payrollEmpFilter');
  if (empFilter) empFilter.addEventListener('change', loadPayrolls);
  const statusFilter = document.getElementById('payrollStatusFilter');
  if (statusFilter) statusFilter.addEventListener('change', loadPayrolls);

  // Auto-fetch & calculation listeners
  const payEmpSelect = document.getElementById('payEmployeeSelect');
  if (payEmpSelect) {
    payEmpSelect.addEventListener('change', autoFetchEmployeeSalaryInfo);
  }
  if (modalMonth) {
    modalMonth.addEventListener('change', autoFetchEmployeeSalaryInfo);
  }

  // Live calculation input fields
  const calcInputs = [
    'payBasic', 'payHouseAll', 'payMedAll', 'payTransAll', 'payOtherAll',
    'payOtHours', 'payOtRate', 'payOtPayment', 'payBonus',
    'payLeaveDed', 'payAdvanceDed', 'payLoanDed', 'payTaxDed', 'payEobiDed', 'paySessiDed', 'payOtherDed'
  ];
  calcInputs.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', updateLiveNetSalary);
  });

  // Calculate Overtime Payment from Hours & Rate
  const otHoursEl = document.getElementById('payOtHours');
  const otRateEl = document.getElementById('payOtRate');
  if (otHoursEl && otRateEl) {
    const calcOtPay = () => {
      const h = parseFloat(otHoursEl.value) || 0;
      const r = parseFloat(otRateEl.value) || 0;
      document.getElementById('payOtPayment').value = Math.round(h * r);
      updateLiveNetSalary();
    };
    otHoursEl.addEventListener('input', calcOtPay);
    otRateEl.addEventListener('input', calcOtPay);
  }

  // Form Submit
  const form = document.getElementById('payrollForm');
  if (form) form.addEventListener('submit', handlePayrollFormSubmit);
});

/**
 * Load Initial Dropdowns
 */
async function loadInitialDropdowns() {
  try {
    const [empRes, deptRes] = await Promise.all([
      fetchAPI('/api/employees'),
      fetchAPI('/api/departments')
    ]);

    if (empRes.status === 'success') {
      activeEmployeesList = empRes.data;

      const filterEmp = document.getElementById('payrollEmpFilter');
      if (filterEmp) {
        filterEmp.innerHTML = '<option value="">All Employees</option>' +
          activeEmployeesList.map(e => `<option value="${e.employee_id}">${escapeHTML(e.full_name)} (${e.employee_id})</option>`).join('');
      }

      const modalEmp = document.getElementById('payEmployeeSelect');
      if (modalEmp) {
        modalEmp.innerHTML = '<option value="">Select Employee to Process</option>' +
          activeEmployeesList.filter(e => e.status.toLowerCase() === 'active').map(e =>
            `<option value="${e.employee_id}">${escapeHTML(e.full_name)} (${e.employee_id}) - ${e.department} [${e.shift}]</option>`
          ).join('');
      }
    }

    if (deptRes.status === 'success') {
      allDepartments = deptRes.data;
      const filterDept = document.getElementById('payrollDeptFilter');
      if (filterDept) {
        filterDept.innerHTML = '<option value="">All Departments</option>' +
          allDepartments.map(d => `<option value="${escapeHTML(d.name)}">${escapeHTML(d.name)}</option>`).join('');
      }
    }
  } catch (error) {
    console.error('Error loading payroll dropdowns:', error);
  }
}

/**
 * Load Payroll History
 */
async function loadPayrolls() {
  const month = document.getElementById('payrollMonthFilter')?.value || '';
  const dept = document.getElementById('payrollDeptFilter')?.value || '';
  const empId = document.getElementById('payrollEmpFilter')?.value || '';
  const status = document.getElementById('payrollStatusFilter')?.value || '';

  const params = new URLSearchParams();
  if (month) params.append('month', month);
  if (dept) params.append('department', dept);
  if (empId) params.append('employee_id', empId);
  if (status) params.append('status', status);

  try {
    const res = await fetchAPI(`/api/payroll?${params.toString()}`);
    if (res.status === 'success') {
      allPayrolls = res.data;
      renderPayrollTable(allPayrolls, res.total_payout);
    }
  } catch (error) {
    showToast('Failed to load payroll records: ' + error.message, 'danger');
  }
}

/**
 * Render Payroll Table in Pakistani Rupees
 */
function renderPayrollTable(payrolls, totalPayout) {
  const tbody = document.getElementById('payrollTableBody');
  const countBadge = document.getElementById('payrollCountBadge');
  const totalDisplay = document.getElementById('payrollTotalDisplay');

  if (countBadge) countBadge.textContent = `${payrolls.length} Payroll Records`;
  if (totalDisplay) totalDisplay.textContent = formatPKR(totalPayout || 0);

  if (!tbody) return;

  if (payrolls.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="9" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <h4 class="empty-title">No payroll entries found</h4>
          <p class="empty-desc">Click "Generate Monthly Payroll" to compute salary for an employee.</p>
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = payrolls.map(p => {
    let statusBadge = 'badge-success';
    if (p.payment_status.toLowerCase() === 'pending') statusBadge = 'badge-danger';
    else if (p.payment_status.toLowerCase() === 'approved') statusBadge = 'badge-warning';

    const totalAllowances = (p.total_allowances || 0) + (p.overtime_payment || 0) + (p.bonus || 0);

    return `
      <tr>
        <td>
          <span style="font-family: monospace; font-weight: 800; color: var(--denim);">
            ${escapeHTML(p.payroll_id)}
          </span>
        </td>
        <td>
          <div style="font-weight: 700;">${escapeHTML(p.employee_name)}</div>
          <div style="font-size: 11px; color: var(--text-muted); font-family: monospace;">
            ${escapeHTML(p.employee_id)} &bull; ${escapeHTML(p.cnic || '')}
          </div>
        </td>
        <td>
          <span class="badge badge-neutral">${escapeHTML(p.month)}</span>
        </td>
        <td>${formatPKR(p.basic_salary)}</td>
        <td style="color: var(--success); font-weight: 600;">+${formatPKR(totalAllowances)}</td>
        <td style="color: var(--danger); font-weight: 600;">-${formatPKR(p.total_deductions)}</td>
        <td style="font-size: 14px; font-weight: 800; color: var(--primary);">
          ${formatPKR(p.net_salary)}
        </td>
        <td>
          <span class="badge ${statusBadge}">
            <span class="badge-dot"></span>
            ${escapeHTML(p.payment_status)}
          </span>
        </td>
        <td>
          <div class="table-actions">
            <a href="salary-slip.html?id=${p.payroll_id}" class="action-btn view-btn" title="View & Print Official Payslip">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            </a>
            ${p.payment_status.toLowerCase() !== 'paid' ? `
              <button class="action-btn edit-btn" title="Mark as Paid" onclick="changePayrollStatus('${p.payroll_id}', 'Paid')">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
              </button>
            ` : ''}
            <button class="action-btn delete-btn" title="Delete Payroll Entry" onclick="confirmDeletePayroll('${p.payroll_id}', '${escapeHTML(p.employee_name)}')">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

/**
 * Open Modal to Generate Payroll
 */
function openGeneratePayrollModal() {
  const form = document.getElementById('payrollForm');
  if (form) form.reset();

  const today = new Date().toISOString().split('T')[0];
  document.getElementById('payMonth').value = today.substring(0, 7);
  document.getElementById('payDate').value = today;

  document.getElementById('payrollDuplicateWarning').style.display = 'none';
  document.getElementById('paySubmitBtn').disabled = false;

  updateLiveNetSalary();
  openModal('generatePayrollModal');
}

/**
 * Auto-fetch employee salary and compute Pakistani textile components
 */
async function autoFetchEmployeeSalaryInfo() {
  const empId = document.getElementById('payEmployeeSelect')?.value;
  const month = document.getElementById('payMonth')?.value;

  if (!empId || !month) return;

  try {
    const res = await fetchAPI(`/api/payroll/calculate-preview?employee_id=${empId}&month=${month}`);
    if (res.status === 'success') {
      const d = res.data;

      // Populate Earnings in PKR
      document.getElementById('payBasic').value = d.basic_salary;
      document.getElementById('payHouseAll').value = d.house_allowance;
      document.getElementById('payMedAll').value = d.medical_allowance;
      document.getElementById('payTransAll').value = d.transport_allowance;
      document.getElementById('payOtherAll').value = d.other_allowances;
      document.getElementById('payOtHours').value = d.overtime_hours;
      document.getElementById('payOtRate').value = d.overtime_rate;
      document.getElementById('payOtPayment').value = d.overtime_payment;
      document.getElementById('payBonus').value = d.bonus || 0;

      // Populate Deductions in PKR
      document.getElementById('payLeaveDed').value = d.unpaid_leave_deduction;
      document.getElementById('payAdvanceDed').value = d.advance_salary || 0;
      document.getElementById('payLoanDed').value = d.loan_deduction || 0;
      document.getElementById('payTaxDed').value = d.tax_deduction;
      document.getElementById('payEobiDed').value = d.eobi_contribution;
      document.getElementById('paySessiDed').value = d.sessi_contribution || 0;
      document.getElementById('payOtherDed').value = d.other_deductions || 0;

      // Notice for attendance details
      const attHint = document.getElementById('payrollAttHint');
      if (attHint) {
        attHint.textContent = `Attendance Data: ${d.absent_days} unapproved absent day(s), ${d.half_days} half-day(s), ${d.overtime_hours} hrs overtime recorded.`;
      }

      // Check duplicate
      const warnBox = document.getElementById('payrollDuplicateWarning');
      const submitBtn = document.getElementById('paySubmitBtn');
      if (d.already_generated) {
        warnBox.style.display = 'block';
        warnBox.innerHTML = `<strong>Attention:</strong> Payroll for ${escapeHTML(d.employee_name)} for month ${month} is already generated (${d.existing_payroll_id}). Status: ${d.existing_status}.`;
        submitBtn.disabled = true;
      } else {
        warnBox.style.display = 'none';
        submitBtn.disabled = false;
      }

      updateLiveNetSalary();
    }
  } catch (error) {
    showToast('Failed to auto-fetch salary details: ' + error.message, 'danger');
  }
}

/**
 * Live calculation of Gross, Deductions, and Net Salary in PKR
 */
function updateLiveNetSalary() {
  const basic = parseFloat(document.getElementById('payBasic')?.value) || 0;
  const house = parseFloat(document.getElementById('payHouseAll')?.value) || 0;
  const med = parseFloat(document.getElementById('payMedAll')?.value) || 0;
  const trans = parseFloat(document.getElementById('payTransAll')?.value) || 0;
  const otherAll = parseFloat(document.getElementById('payOtherAll')?.value) || 0;
  const otPay = parseFloat(document.getElementById('payOtPayment')?.value) || 0;
  const bonus = parseFloat(document.getElementById('payBonus')?.value) || 0;

  const totalAllowances = house + med + trans + otherAll;
  const gross = basic + totalAllowances + otPay + bonus;

  const leave = parseFloat(document.getElementById('payLeaveDed')?.value) || 0;
  const advance = parseFloat(document.getElementById('payAdvanceDed')?.value) || 0;
  const loan = parseFloat(document.getElementById('payLoanDed')?.value) || 0;
  const tax = parseFloat(document.getElementById('payTaxDed')?.value) || 0;
  const eobi = parseFloat(document.getElementById('payEobiDed')?.value) || 0;
  const sessi = parseFloat(document.getElementById('paySessiDed')?.value) || 0;
  const otherDed = parseFloat(document.getElementById('payOtherDed')?.value) || 0;

  const totalDeductions = leave + advance + loan + tax + eobi + sessi + otherDed;
  const net = Math.max(0, gross - totalDeductions);

  setText('liveGrossDisplay', formatPKR(gross));
  setText('liveDedDisplay', formatPKR(totalDeductions));
  setText('liveNetDisplay', formatPKR(net));
}

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

/**
 * Handle Payroll Generation Submit
 */
async function handlePayrollFormSubmit(e) {
  e.preventDefault();

  const payload = {
    employee_id: document.getElementById('payEmployeeSelect').value,
    month: document.getElementById('payMonth').value,
    basic_salary: parseFloat(document.getElementById('payBasic').value) || 0,
    house_allowance: parseFloat(document.getElementById('payHouseAll').value) || 0,
    medical_allowance: parseFloat(document.getElementById('payMedAll').value) || 0,
    transport_allowance: parseFloat(document.getElementById('payTransAll').value) || 0,
    other_allowances: parseFloat(document.getElementById('payOtherAll').value) || 0,
    overtime_hours: parseFloat(document.getElementById('payOtHours').value) || 0,
    overtime_rate: parseFloat(document.getElementById('payOtRate').value) || 0,
    overtime_payment: parseFloat(document.getElementById('payOtPayment').value) || 0,
    bonus: parseFloat(document.getElementById('payBonus').value) || 0,
    unpaid_leave_deduction: parseFloat(document.getElementById('payLeaveDed').value) || 0,
    advance_salary: parseFloat(document.getElementById('payAdvanceDed').value) || 0,
    loan_deduction: parseFloat(document.getElementById('payLoanDed').value) || 0,
    tax_deduction: parseFloat(document.getElementById('payTaxDed').value) || 0,
    eobi_contribution: parseFloat(document.getElementById('payEobiDed').value) || 0,
    sessi_contribution: parseFloat(document.getElementById('paySessiDed').value) || 0,
    other_deductions: parseFloat(document.getElementById('payOtherDed').value) || 0,
    payment_status: document.getElementById('payStatus').value,
    payment_date: document.getElementById('payDate').value
  };

  try {
    const res = await fetchAPI('/api/payroll', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
    showToast(res.message, 'success');
    closeModal('generatePayrollModal');
    loadPayrolls();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

/**
 * Change Status (e.g. to Paid)
 */
async function changePayrollStatus(payrollId, newStatus) {
  try {
    const res = await fetchAPI(`/api/payroll/${payrollId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status: newStatus })
    });
    showToast(res.message, 'success');
    loadPayrolls();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

/**
 * Confirm and Delete Payroll
 */
function confirmDeletePayroll(payrollId, empName) {
  showConfirmDialog(
    'Delete Payroll Record',
    `Are you sure you want to delete the payroll entry ${payrollId} for ${empName}?`,
    'Delete Record',
    async () => {
      try {
        const res = await fetchAPI(`/api/payroll/${payrollId}`, { method: 'DELETE' });
        showToast(res.message, 'success');
        loadPayrolls();
      } catch (error) {
        showToast(error.message, 'danger');
      }
    }
  );
}
