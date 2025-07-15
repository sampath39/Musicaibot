# app.py
from flask import Flask, request, jsonify, render_template
import joblib
import os

app = Flask(__name__)

# Load model if it exists
MODEL_PATH = 'emotion_model.pkl'
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_emotion():
    data = request.get_json()
    text = data.get('text', '')
    if not model:
        return jsonify({'error': 'Model not found'}), 500

    # Default to 'neutral' if no strong keywords are found and model returns uncertain value
    prediction = model.predict([text])[0]
    if not prediction:
        prediction = 'neutral'

    return jsonify({'emotion': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
