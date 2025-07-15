import os
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('emotion_model.pkl')

@app.route('/predict', methods=['POST'])
def predict_emotion():
    data = request.get_json()
    text = data['text']
    prediction = model.predict([text])[0]
    return jsonify({'emotion': prediction})

if __name__ == '__main__':
    # Get PORT from environment variable (Render will set this)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
