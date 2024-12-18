import base64
import io
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
from datetime import datetime
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

app = Flask(__name__)

# Load the trained CatBoost model
MODEL_PATH = 'trained_catboost_model.joblib'
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found.")
catboost_model = joblib.load(MODEL_PATH)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the form data
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

        # Convert numerical inputs to float and handle missing values
        numerical_keys = ['Signal_Strength',
                          'Latency', 'Bandwidth_Utilization_Ratio']
        for key in numerical_keys:
            if key in data:
                try:
                    data[key] = float(data[key])
                except ValueError:
                    return jsonify({'error': f"Invalid value for {key}. Please provide a valid number."}), 400
            else:
                return jsonify({'error': f"Missing required field: {key}"}), 400

        # Convert data to DataFrame
        input_data = pd.DataFrame([data])

        # Make predictions
        prediction = np.around(catboost_model.predict(
            input_data) * 100, decimals=2)

        # Calculate resource allocation
        resource_allocation = {
            key: (data[key] * prediction[0]) for key in checkbox_keys}

        # Create bar graph
        plt.figure(figsize=(10, 6))
        plt.bar(resource_allocation.keys(),
                resource_allocation.values(), color='skyblue')
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

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Use HTTPS in production environments
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
