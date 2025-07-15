from flask import Flask, request, jsonify, render_template
import joblib
import os

app = Flask(__name__)

# Load the trained model (ensure this file exists in your project directory)
model_path = os.path.join(os.path.dirname(__file__), 'emotion_model.pkl')
model = joblib.load(model_path)

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

# Predict emotion from text
@app.route('/predict', methods=['POST'])
def predict_emotion():
    try:
        data = request.get_json()
        text = data.get('text', '')
        prediction = model.predict([text])[0]
        return jsonify({'emotion': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run app locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
