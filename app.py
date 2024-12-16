from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from datetime import datetime
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load the trained CatBoost model
catboost_model = joblib.load('trained_catboost_model.joblib')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()

    # Set default values for checkboxes
    checkbox_keys = [
        'Application_Type_Video_Call',
        'Application_Type_Web_Browsing',
        'Application_Type_Background_Download',
        'Application_Type_Emergency_Service',
        'Application_Type_File_Download',
        'Application_Type_IoT_Temperature',
        'Application_Type_Online_Gaming',
        'Application_Type_Streaming',
        'Application_Type_Video_Streaming',
        'Application_Type_VoIP_Call',
        'Application_Type_Voice_Call'
    ]
    for key in checkbox_keys:
        data[key] = 1 if key in data else 0

    # Convert other inputs to float
    for key in ['Signal_Strength', 'Latency', 'Bandwidth_Utilization_Ratio']:
        if key in data:
            data[key] = float(data[key])

    # Convert data to DataFrame
    input_data = pd.DataFrame([data])

    # Make predictions
    prediction = np.around(catboost_model.predict(input_data) * 100, decimals=2)

    # Calculate resource allocation
    resource_allocation = {key: (data[key] * prediction[0]) for key in checkbox_keys}

    # Create bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(resource_allocation.keys(), resource_allocation.values(), color='skyblue')
    plt.xlabel('Application Types')
    plt.ylabel('Resource Allocation (%)')
    plt.title('Resource Allocation by Application Type')
    plt.xticks(rotation=45, ha='right')
    
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return jsonify({'prediction': prediction.tolist(), 'plot_url': plot_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
