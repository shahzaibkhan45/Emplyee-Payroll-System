/**
 * Dashboard Controller - Rajby Textile Industries
 * Fetches real-time textile mill workforce metrics in Pakistani Rupees (PKR / Rs.)
 */

let deptDistributionChart = null;
let payrollExpenseChart = null;

async function loadDashboard() {
  try {
    const res = await fetchAPI('/api/dashboard');
    if (res.status === 'success') {
      const { stats, recent_employees, department_distribution, payroll_summary, today_attendance } = res;

      // 1. Primary Metrics Cards in PKR
      setText('metricTotalEmployees', stats.total_employees);
      setText('metricActiveEmployees', stats.active_employees);
      setText('metricInactiveEmployees', stats.inactive_employees);
      setText('metricLeaveEmployees', stats.leave_employees);
      setText('metricPresentToday', stats.present_employees);
      setText('metricAbsentToday', stats.absent_employees);

      // Financials in PKR
      setText('metricMonthlyPayroll', formatPKR(stats.total_monthly_payroll));
      setText('metricPendingPayroll', formatPKR(stats.pending_payroll));
      setText('metricPaidPayroll', formatPKR(stats.paid_payroll));
      setText('metricTotalDepartments', stats.total_departments);

      // 2. Render Recent Employees
      renderRecentEmployees(recent_employees);

      // 3. Render Attendance Overview
      renderAttendanceOverview(today_attendance);

      // 4. Render Charts in PKR
      renderCharts(department_distribution, payroll_summary.department_payouts);
    }
  } catch (error) {
    showToast('Failed to load textile dashboard metrics: ' + error.message, 'danger');
  }
}

function setText(elementId, text) {
  const el = document.getElementById(elementId);
  if (el) el.textContent = text;
}

function renderRecentEmployees(employees) {
  const tbody = document.getElementById('recentEmployeesTableBody');
  if (!tbody) return;

  if (!employees || employees.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="6" class="empty-state">
          <p class="empty-desc">No employee records registered yet.</p>
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = employees.map(emp => `
    <tr>
      <td>
        <div style="font-weight: 700; color: var(--text-primary);">${escapeHTML(emp.full_name)}</div>
        <div style="font-size: 11px; font-family: monospace; color: var(--denim); font-weight: 600;">
          ${escapeHTML(emp.employee_id)} &bull; ${escapeHTML(emp.cnic || 'CNIC N/A')}
        </div>
      </td>
      <td>
        <span class="badge badge-neutral">${escapeHTML(emp.department)}</span>
      </td>
      <td>${escapeHTML(emp.designation)}</td>
      <td>
        <span class="badge badge-denim">${escapeHTML(emp.shift || 'General')}</span>
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

function renderAttendanceOverview(today) {
  setText('attPresentCount', today.present || 0);
  setText('attAbsentCount', today.absent || 0);
  setText('attLeaveCount', today.leave || 0);
  setText('attHalfDayCount', today.half_day || 0);
  setText('attLateCount', today.late_arrival || 0);
  setText('attUnmarkedCount', today.unmarked || 0);
  setText('attTotalOTHours', (today.total_overtime_hours || 0) + ' hrs');
}

function renderCharts(deptDistribution, deptPayouts) {
  // Chart 1: Department Distribution (Doughnut)
  const ctxDept = document.getElementById('departmentDistributionChart');
  if (ctxDept && window.Chart) {
    if (deptDistributionChart) deptDistributionChart.destroy();

    const labels = deptDistribution.map(d => d.name);
    const data = deptDistribution.map(d => d.count);
    const colors = [
      '#1b3a5b', '#2b5c8f', '#0284c7', '#059669', '#d97706',
      '#7c3aed', '#db2777', '#475569', '#0d9488', '#ea580c'
    ];

    deptDistributionChart = new Chart(ctxDept, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: colors.slice(0, labels.length),
          borderWidth: 2,
          borderColor: '#ffffff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 10,
              padding: 10,
              font: { size: 10.5, family: 'Inter' }
            }
          }
        },
        cutout: '66%'
      }
    });
  }

  // Chart 2: Monthly Payroll Expenditure by Department (Bar in PKR)
  const ctxPay = document.getElementById('payrollExpenseChart');
  if (ctxPay && window.Chart) {
    if (payrollExpenseChart) payrollExpenseChart.destroy();

    const pLabels = Object.keys(deptPayouts || {});
    const pData = Object.values(deptPayouts || {});

    payrollExpenseChart = new Chart(ctxPay, {
      type: 'bar',
      data: {
        labels: pLabels.length > 0 ? pLabels : ['No Data'],
        datasets: [{
          label: 'Payroll Disbursement (PKR)',
          data: pData.length > 0 ? pData : [0],
          backgroundColor: '#2b5c8f',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (item) => 'Disbursement: ' + formatPKR(item.raw)
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: val => 'Rs. ' + (val >= 1000 ? (val / 1000).toLocaleString() + 'k' : val)
            },
            grid: { color: '#f1f5f9' }
          },
          x: {
            grid: { display: false },
            ticks: {
              font: { size: 10.5 },
              maxRotation: 45,
              minRotation: 20
            }
          }
        }
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', loadDashboard);
