/**
 * Salary Slip Controller - Rajby Textile Industries, Karachi
 * Handles official employee pay statement rendering, PKR formatting, printing, and PDF export.
 */

document.addEventListener('DOMContentLoaded', () => {
  loadPayrollSelectorDropdown();

  const urlParams = new URLSearchParams(window.location.search);
  const payrollId = urlParams.get('id');

  if (payrollId) {
    loadSalarySlip(payrollId);
  }

  const selector = document.getElementById('slipPayrollSelector');
  if (selector) {
    selector.addEventListener('change', (e) => {
      if (e.target.value) {
        loadSalarySlip(e.target.value);
        history.pushState(null, '', `salary-slip.html?id=${e.target.value}`);
      }
    });
  }
});

/**
 * Load all generated payrolls into top selector
 */
async function loadPayrollSelectorDropdown() {
  try {
    const res = await fetchAPI('/api/payroll');
    if (res.status === 'success') {
      const payrolls = res.data;
      const selector = document.getElementById('slipPayrollSelector');
      if (!selector) return;

      if (payrolls.length === 0) {
        selector.innerHTML = '<option value="">No payroll records generated yet</option>';
        return;
      }

      const urlParams = new URLSearchParams(window.location.search);
      const currentId = urlParams.get('id') || payrolls[0].payroll_id;

      selector.innerHTML = payrolls.map(p => 
        `<option value="${p.payroll_id}" ${p.payroll_id === currentId ? 'selected' : ''}>
          ${escapeHTML(p.payroll_id)} - ${escapeHTML(p.employee_name)} [${escapeHTML(p.department)}] (${escapeHTML(p.month)})
        </option>`
      ).join('');

      if (!urlParams.get('id') && payrolls.length > 0) {
        loadSalarySlip(payrolls[0].payroll_id);
      }
    }
  } catch (error) {
    console.error('Failed to load payroll list for selector:', error);
  }
}

/**
 * Load and render specific payslip
 */
async function loadSalarySlip(payrollId) {
  const loading = document.getElementById('slipLoading');
  const content = document.getElementById('slipContent');
  if (loading) loading.style.display = 'block';
  if (content) content.style.display = 'none';

  try {
    const res = await fetchAPI(`/api/payroll/${payrollId}`);
    if (res.status === 'success') {
      const p = res.data;
      renderSalarySlip(p);
      if (loading) loading.style.display = 'none';
      if (content) content.style.display = 'block';
    }
  } catch (error) {
    if (loading) loading.style.display = 'none';
    showToast('Failed to load salary slip: ' + error.message, 'danger');
  }
}

/**
 * Populate salary slip in Pakistani Rupees (Rs.)
 */
function renderSalarySlip(p) {
  // Reference & Meta
  setText('slipIdDisplay', p.payroll_id);
  setText('slipMonthDisplay', p.month);
  setText('slipPayDateDisplay', formatDate(p.payment_date));
  setText('slipStatusDisplay', p.payment_status);

  // Employee details
  setText('slipEmpId', p.employee_id);
  setText('slipEmpName', p.employee_name);
  setText('slipEmpCnic', p.cnic || 'N/A');
  setText('slipDepartment', p.department);
  setText('slipDesignation', p.designation);
  setText('slipShift', p.shift || 'General Office Shift');
  setText('slipBank', `${p.bank_name || 'Bank'} (${p.account_number_iban || 'Account on file'})`);

  // Earnings Breakdown in PKR
  setText('slipBasicSalary', formatPKR(p.basic_salary));
  setText('slipHouseAllowance', formatPKR(p.house_allowance));
  setText('slipMedicalAllowance', formatPKR(p.medical_allowance));
  setText('slipTransportAllowance', formatPKR(p.transport_allowance));
  setText('slipOtherAllowances', formatPKR(p.other_allowances));
  setText('slipOvertime', `${formatPKR(p.overtime_payment)} (${p.overtime_hours || 0} hrs)`);
  setText('slipBonus', formatPKR(p.bonus));
  setText('slipTotalEarnings', formatPKR(p.gross_salary));

  // Deductions Breakdown in PKR
  setText('slipEobi', formatPKR(p.eobi_contribution));
  setText('slipSessi', formatPKR(p.sessi_contribution));
  setText('slipTaxDeduction', formatPKR(p.tax_deduction));
  setText('slipAdvanceSalary', formatPKR(p.advance_salary));
  setText('slipLeaveDeduction', formatPKR(p.unpaid_leave_deduction));
  setText('slipLoanDeduction', formatPKR(p.loan_deduction));
  setText('slipOtherDeductions', formatPKR(p.other_deductions));
  setText('slipTotalDeductions', formatPKR(p.total_deductions));

  // Net Salary in PKR
  setText('slipNetSalary', formatPKR(p.net_salary));
}

function setText(elementId, text) {
  const el = document.getElementById(elementId);
  if (el) el.textContent = text;
}

/**
 * Download Salary Slip as PDF using window.print()
 */
function downloadSalarySlipPDF() {
  window.print();
}
