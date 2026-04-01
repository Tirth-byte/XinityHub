document.addEventListener('DOMContentLoaded', () => {
    // File upload area logic
    const fileInput = document.querySelector('.file-input');
    const fileDropArea = document.querySelector('.file-drop-area');
    const fileMsg = document.querySelector('.file-msg');

    if (fileInput && fileDropArea) {
        // Drag over effects
        ['dragenter', 'dragover'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                fileDropArea.classList.add('is-active');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            fileDropArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                fileDropArea.classList.remove('is-active');
            }, false);
        });

        // Handle drop or selection
        fileInput.addEventListener('change', (e) => {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                fileMsg.textContent = fileName;
                fileMsg.style.color = "var(--primary-color)";
            } else {
                fileMsg.textContent = "Drag & drop or click to choose an image";
                fileMsg.style.color = "var(--text-muted)";
            }
        });
    }

    // View details button interaction (mock)
    const detailButtons = document.querySelectorAll('.view-details-btn');
    detailButtons.forEach(btn => {
        btn.addEventListener('click', () => {
             alert('This could navigate to a detailed project view in a full production app.');
        });
    });

    // Form logic and loading state
    const submitForm = document.getElementById('submitForm');
    if (submitForm) {
        submitForm.addEventListener('submit', (e) => {
            // Wait for basic HTML5 validation
            if (!submitForm.checkValidity()) return;
            
            const btn = submitForm.querySelector('.submit-btn');
            const submitText = btn.querySelector('.submit-text');
            const submitIcon = btn.querySelector('.submit-icon');
            
            if (submitText && submitIcon) {
                submitText.textContent = 'Publishing Project...';
                submitIcon.innerHTML = '<div class="spinner"></div>';
            }
            
            btn.style.opacity = '0.7';
            btn.style.cursor = 'not-allowed';
        });
    }
});
