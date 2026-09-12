document.addEventListener('DOMContentLoaded', () => {
    // Select the form - assuming it's the first form on the page since index.html is currently empty
    const form = document.querySelector('form');

    if (form) {
        form.addEventListener('submit', function(event) {
            let isValid = true;

            // Clear previous error messages
            const existingErrors = form.querySelectorAll('.error-message');
            existingErrors.forEach(error => error.remove());

            // Get all inputs that might be required
            // You can adjust the selector based on the actual form fields once index.html is populated
            const requiredFields = form.querySelectorAll('input[required], textarea[required], select[required]');

            requiredFields.forEach(field => {
                if (field.value.trim() === '') {
                    isValid = false;
                    
                    // Create dynamic error message element
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-message';
                    errorDiv.style.color = 'red';
                    errorDiv.style.fontSize = '0.875em';
                    errorDiv.style.marginTop = '4px';
                    errorDiv.innerText = 'This field is required.';
                    
                    // Insert error message just below the input field
                    field.parentNode.insertBefore(errorDiv, field.nextSibling);
                }
            });

            // Prevent default submission if any required fields are empty
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
});
