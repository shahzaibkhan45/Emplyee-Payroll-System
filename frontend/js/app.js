/**
 * Global Utility Functions & Shared Helpers - Rajby Textile Industries
 * Pakistani Localization (PKR, DD-MM-YYYY, CNIC formatting) & Modal Engine
 */

const API_BASE_URL = window.location.origin.includes('5000') 
  ? window.location.origin 
  : 'http://127.0.0.1:5000';

/**
 * Universal Fetch wrapper
 */
async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers || {})
    }
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || `Server Error: ${response.status} ${response.statusText}`);
    }
    return data;
  } catch (error) {
    console.error(`API Error on ${endpoint}:`, error);
    throw error;
  }
}

/**
 * Pakistani Rupee (PKR) Formatter
 * Outputs: Rs. 85,000 or Rs. 1,25,000 (No USD / dollar anywhere!)
 */
function formatPKR(amount) {
  const num = Math.round(parseFloat(amount) || 0);
  return 'Rs. ' + num.toLocaleString('en-PK');
}

// Alias for seamless backward compatibility
function formatCurrency(amount) {
  return formatPKR(amount);
}

/**
 * Date Formatter: Formats to Pakistani Standard DD-MM-YYYY
 */
function formatDate(dateStr) {
  if (!dateStr || dateStr === '-') return '-';
  try {
    // If format is YYYY-MM-DD
    if (dateStr.includes('-') && dateStr.length === 10 && dateStr.indexOf('-') === 4) {
      const [y, m, d] = dateStr.split('-');
      return `${d}-${m}-${y}`;
    }
    // If format is already DD-MM-YYYY
    return dateStr;
  } catch (e) {
    return dateStr;
  }
}

/**
 * Pakistani CNIC Formatter / Auto-Hyphenator
 * Transforms 4210112345671 into 42101-1234567-1
 */
function formatCNICInput(val) {
  const cleaned = val.replace(/\D/g, '').substring(0, 13);
  let formatted = cleaned;
  if (cleaned.length > 5 && cleaned.length <= 12) {
    formatted = `${cleaned.substring(0, 5)}-${cleaned.substring(5)}`;
  } else if (cleaned.length > 12) {
    formatted = `${cleaned.substring(0, 5)}-${cleaned.substring(5, 12)}-${cleaned.substring(12, 13)}`;
  }
  return formatted;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHTML(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Toast Notification System
 */
function showToast(message, type = 'info', duration = 4000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;

  const iconMap = {
    success: `<svg class="toast-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`,
    danger: `<svg class="toast-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`,
    warning: `<svg class="toast-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`,
    info: `<svg class="toast-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
  };

  toast.innerHTML = `
    ${iconMap[type] || iconMap.info}
    <div class="toast-message">${escapeHTML(message)}</div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(40px)';
    setTimeout(() => toast.remove(), 250);
  }, duration);
}

/**
 * Modal Open / Close Helpers (Locks background page scroll)
 */
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Auto-focus first input in the modal if available
    const firstInput = modal.querySelector('input, select, textarea');
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 100);
    }
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

/**
 * Delete Confirmation Dialog
 */
let pendingConfirmCallback = null;

function showConfirmDialog(title, message, confirmBtnText = 'Confirm Delete', onConfirm = null) {
  let modal = document.getElementById('confirmModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'confirmModal';
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal-dialog" style="max-width: 420px;">
        <div class="modal-body" style="text-align: center; padding: 28px 24px;">
          <div style="width: 52px; height: 52px; border-radius: 50%; background: #fee2e2; color: #dc2626; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px;">
            <svg style="width:26px;height:26px;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
          </div>
          <h3 id="confirmTitle" class="modal-title" style="justify-content: center; margin-bottom: 8px;">Confirm Action</h3>
          <p id="confirmMessage" style="color: var(--text-secondary); font-size: 13px; line-height: 1.5;">Are you sure you want to proceed?</p>
        </div>
        <div class="modal-footer" style="justify-content: center; gap: 12px; background: #f8fafc;">
          <button type="button" class="btn btn-secondary" onclick="closeModal('confirmModal')">Cancel</button>
          <button type="button" id="confirmProceedBtn" class="btn btn-danger">Confirm</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    document.getElementById('confirmProceedBtn').addEventListener('click', () => {
      if (typeof pendingConfirmCallback === 'function') {
        const cb = pendingConfirmCallback;
        pendingConfirmCallback = null;
        closeModal('confirmModal');
        cb();
      }
    });

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal('confirmModal');
    });
  }

  document.getElementById('confirmTitle').textContent = title;
  document.getElementById('confirmMessage').textContent = message;
  const proceedBtn = document.getElementById('confirmProceedBtn');
  proceedBtn.textContent = confirmBtnText;

  pendingConfirmCallback = onConfirm;
  openModal('confirmModal');
}

// Global Initialization
document.addEventListener('DOMContentLoaded', () => {
  // Mobile sidebar toggle
  const toggleBtn = document.querySelector('.mobile-menu-btn');
  const sidebar = document.querySelector('.sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('mobile-open');
    });
  }

  // Set today's date in Pakistani DD-MM-YYYY format
  const dateBadge = document.getElementById('currentDateBadge');
  if (dateBadge) {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const weekday = today.toLocaleDateString('en-US', { weekday: 'short' });
    dateBadge.textContent = `${weekday}, ${day}-${month}-${year}`;
  }

  // Close modals on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const activeModal = document.querySelector('.modal-overlay.active');
      if (activeModal) {
        closeModal(activeModal.id);
      }
    }
  });
});
