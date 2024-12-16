document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Show loading indicator
    document.getElementById('prediction-result').innerHTML = '<p>Loading...</p>';

    // Get form data
    const formData = new FormData(event.target);

    // Send POST request to Flask API
    fetch('/predict', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Display prediction result
        document.getElementById('prediction-result').innerHTML = `<p>Resources required: ${data.prediction} %</p>`;
        
        // Show the result graph if available
        const img = document.getElementById('result-graph');
        img.src = 'data:image/png;base64,' + data.plot_url;
        img.style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});

// Function to update slider value based on text field input
function updateSlider(input, index) {
    const slider = document.getElementById('sliderValue' + index);
    const value = parseFloat(input.value);
    if (isNaN(value)) {
        input.value = slider.value;
    } else {
        slider.value = value;
    }
    updateSliderValue(slider, index);
}

// Function to update slider value (displayed value and CSS property)
function updateSliderValue(slider, index) {
    const value = parseFloat(slider.value);
    const textField = document.getElementById('textFieldValue' + index);
    textField.value = value;
    
    // Update the output of the slider
    const output = document.getElementById('output' + index);
    output.textContent = value.toLocaleString();

    // Update the corresponding --text-value CSS variable
    slider.parentNode.style.setProperty('--text-value' + index, value);
}

// Function to update text field value based on slider input
function updateTextFieldValue(slider, index) {
    const value = parseFloat(slider.value);
    const textField = document.getElementById('textFieldValue' + index);
    textField.value = value;

    // Update the output of the slider
    const output = document.getElementById('output' + index);
    output.textContent = value.toLocaleString();

    // Update the corresponding --text-value CSS variable
    slider.parentNode.style.setProperty('--text-value' + index, value);
}

document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Show loading indicator
    document.getElementById('prediction-result').innerHTML = '<p>Loading...</p>';

    // Get form data
    const formData = new FormData(event.target);

    // Send POST request to predict API
    const response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });

    // Get the response
    const result = await response.json();

    // Display prediction
    document.getElementById('prediction-result').innerText = 'Prediction: ' + result.prediction.join(', ');

    // Display the bar graph
    const img = document.getElementById('result-graph');
    img.src = 'data:image/png;base64,' + result.plot_url;
    img.style.display = 'block';
});
