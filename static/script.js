document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('predictionForm');
    const loader = document.querySelector('.loader-container');
    const resultCard = document.querySelector('.result-card');
    const predictionCard = document.querySelector('.prediction-card');
    const predictionText = document.getElementById('prediction');
    const confidenceValue = document.getElementById('confidence');
    const confidenceBar = document.getElementById('confidence-bar-fill');
    const resultIcon = document.getElementById('result-icon');
    const newPredictionBtn = document.getElementById('new-prediction');

    // Form submission handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Validate form
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        // Show loader and hide results
        loader.style.display = 'flex';
        resultCard.style.display = 'none';
        predictionCard.style.opacity = '0.5';
        predictionCard.style.pointerEvents = 'none';

        try {
            // Prepare form data
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = parseFloat(value);
            });

            // Simulate API call delay for demo (remove in production)
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Send POST request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error processing your request');
            }

            const result = await response.json();

            // Update UI with results
            updateResultUI(result);
            
        } catch (error) {
            showError(error.message);
        } finally {
            // Hide loader and show results
            loader.style.display = 'none';
            resultCard.style.display = 'block';
            predictionCard.style.opacity = '1';
            predictionCard.style.pointerEvents = 'auto';
            
            // Scroll to results
            resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });

    // New prediction button handler
    newPredictionBtn.addEventListener('click', () => {
        // Reset form and show prediction card
        form.reset();
        resultCard.style.display = 'none';
        predictionCard.style.opacity = '1';
        predictionCard.style.pointerEvents = 'auto';
        predictionCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    // Update result UI with prediction data
    function updateResultUI(data) {
        const isChurn = data.prediction.includes('more likely to Churn');
        
        // Update result card
        resultIcon.className = 'result-icon ' + (isChurn ? 'danger' : 'success');
        resultIcon.innerHTML = isChurn ? '<i class="fas fa-exclamation-triangle"></i>' : '<i class="fas fa-check-circle"></i>';
        
        predictionText.textContent = data.prediction;
        
        // Animate confidence bar
        const confidence = parseFloat(data.confidence) || 0;
        confidenceBar.style.width = '0%';
        setTimeout(() => {
            confidenceBar.style.width = `${confidence}%`;
        }, 100);
        
        confidenceValue.textContent = `${confidence.toFixed(2)}%`;
    }

    // Show error message
    function showError(message) {
        resultIcon.className = 'result-icon danger';
        resultIcon.innerHTML = '<i class="fas fa-exclamation-circle"></i>';
        predictionText.textContent = 'Error: ' + message;
        confidenceBar.style.width = '0%';
        confidenceValue.textContent = '0%';
    }

    // Input validation and formatting
    const totalChargesInput = document.getElementById('totalcharges');
    if (totalChargesInput) {
        totalChargesInput.addEventListener('input', (e) => {
            // Allow only numbers and one decimal point
            e.target.value = e.target.value.replace(/[^0-9.]/g, '')
                .replace(/(\..*)\./g, '$1');
        });
    }

    // Add animation to form elements on page load
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        group.style.transition = `opacity 0.3s ease ${index * 0.1}s, transform 0.3s ease ${index * 0.1}s`;
        
        // Trigger reflow
        void group.offsetWidth;
        
        group.style.opacity = '1';
        group.style.transform = 'translateY(0)';
    });
});
