from flask import Flask, request, jsonify, render_template
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load('emotion_model.pkl')

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Emotion prediction API
@app.route('/predict', methods=['POST'])
def predict_emotion():
    data = request.get_json()
    text = data['text']
    prediction = model.predict([text])[0]
    return jsonify({'emotion': prediction})

if __name__ == '__main__':
    app.run(debug=True)
