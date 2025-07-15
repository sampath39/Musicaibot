# app.py
from flask import Flask, request, jsonify, render_template
import joblib
import os
import re

app = Flask(__name__)

# Load model if it exists
MODEL_PATH = 'emotion_model.pkl'
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

# Define simple keyword-based emotion detector
emotion_keywords = {
    'happy': ['happy', 'joy', 'joyful', 'glad', 'delighted', 'excited'],
    'sad': ['sad', 'down', 'unhappy', 'depressed', 'gloomy'],
    'angry': ['angry', 'mad', 'furious', 'irritated'],
    'anxious': ['anxious', 'nervous', 'worried', 'tense'],
    'confused': ['confused', 'uncertain', 'unsure'],
    'neutral': ['hello', 'hi', 'okay', 'fine']
}

def detect_emotion_keywords(text):
    text = text.lower()
    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            if re.search(rf'\b{keyword}\b', text):
                return emotion
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_emotion():
    data = request.get_json()
    text = data.get('text', '')

    # Try keyword-based detection first
    keyword_emotion = detect_emotion_keywords(text)
    if keyword_emotion:
        return jsonify({'emotion': keyword_emotion})

    # Fall back to model prediction
    if not model:
        return jsonify({'error': 'Model not found'}), 500

    prediction = model.predict([text])[0]
    if not prediction:
        prediction = 'neutral'

    return jsonify({'emotion': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
