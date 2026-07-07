// ============================================================
// Task Manager – Client-side Logic
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    // ---- Date display ----
    const dateEl = document.getElementById('current-date');
    if (dateEl) {
        dateEl.textContent = new Date().toLocaleDateString('en-US', {
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
        });
    }

    // ---- Sidebar toggle (mobile) ----
    const menuBtn = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== menuBtn) {
                sidebar.classList.remove('open');
            }
        });
    }

    // ---- Password toggle ----
    const togglePw = document.getElementById('toggle-password');
    const pwField = document.getElementById('password');
    if (togglePw && pwField) {
        togglePw.addEventListener('click', () => {
            pwField.type = pwField.type === 'password' ? 'text' : 'password';
        });
    }

    // ---- Auto-dismiss flash messages ----
    document.querySelectorAll('.flash').forEach((el) => {
        setTimeout(() => {
            el.style.transition = 'opacity .4s ease, transform .4s ease';
            el.style.opacity = '0';
            el.style.transform = 'translateX(40px)';
            setTimeout(() => el.remove(), 400);
        }, 4000);
    });

    // ---- Close modal on Escape ----
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeEditModal();
    });

    // ---- Close modal on overlay click ----
    const overlay = document.getElementById('edit-modal');
    if (overlay) {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closeEditModal();
        });
    }
});

// ============================================================
// Toggle task completion via AJAX
// ============================================================
function toggleTask(taskId) {
    fetch(`/tasks/toggle/${taskId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            const btn = document.getElementById(`status-btn-${taskId}`);
            const row = document.getElementById(`task-row-${taskId}`);
            if (btn) {
                btn.textContent = data.completed ? 'Completed' : 'Pending';
                btn.className = `status-badge ${data.completed ? 'status-done' : 'status-pending'}`;
            }
            if (row) {
                row.classList.toggle('row-completed', data.completed);
            }
        })
        .catch(() => location.reload());
}

// ============================================================
// Edit Modal
// ============================================================
function openEditModal(taskId, empName, taskTitle, completed) {
    const modal = document.getElementById('edit-modal');
    const form = document.getElementById('edit-form');
    const label = document.getElementById('edit-task-id-label');

    if (!modal || !form) return;

    form.action = `/tasks/edit/${taskId}`;
    if (label) label.textContent = `#${taskId}`;

    document.getElementById('edit_employee_name').value = empName;
    document.getElementById('edit_task_title').value = taskTitle;
    document.getElementById('edit_completed').value = completed ? 'true' : 'false';

    modal.classList.add('active');
}

function closeEditModal() {
    const modal = document.getElementById('edit-modal');
    if (modal) modal.classList.remove('active');
}
