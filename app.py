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

# Extended keyword-based emotion detector with broader vocabulary
emotion_keywords = {
    'happy': [
        'happy', 'joy', 'joyful', 'glad', 'delighted', 'excited', 'cheerful', 'elated', 'grateful', 'content', 'satisfied', 'awesome', 'great', 'fantastic', 'good', 'ecstatic', 'smiling', 'pleased', 'blissful', 'amused', 'euphoric', 'merry', 'sunny', 'lively', 'chipper', 'upbeat',
        'got a gift', 'won a prize', 'promotion', 'holiday', 'vacation', 'birthday surprise', 'got flowers', 'party', 'friends reunion', 'good news', 'best day', 'I feel amazing', 'I feel so lucky', 'so blessed', 'peaceful', 'positive', 'smiling inside', 'hug', 'laugh', 'I got my dream job'
    ],
    'sad': [
        'sad', 'crying', 'tears', 'tearful', 'unhappy', 'depressed', 'gloomy', 'miserable', 'grief', 'heartbroken', 'melancholy', 'sorrow', 'blue', 'downcast', 'weeping', 'painful', 'hurt', 'lost', 'lonely', 'devastated', 'empty', 'hopeless', 'despair', 'wailing', 'aching',
        'funeral', 'miss someone', 'lost my job', 'rejected', 'failed', 'ignored', 'disappointed', 'argument', 'broke up', 'forgotten', 'overwhelmed', 'laid off', 'homesick', 'missed opportunity'
    ],
    'angry': [
        'angry', 'mad', 'furious', 'irritated', 'annoyed', 'rage', 'hate', 'frustrated', 'hostile', 'resentful', 'offended', 'vengeful', 'agitated', 'provoked', 'grumpy', 'snappy', 'infuriated', 'outraged', 'wrathful', 'enraged',
        'screaming', 'yelling', 'fight', 'lost temper', 'arguing', 'injustice', 'cut off', 'disrespected', 'lied to'
    ],
    'anxious': [
        'anxious', 'nervous', 'worried', 'tense', 'uneasy', 'stressed', 'afraid', 'scared', 'panicked', 'apprehensive', 'uncertain', 'fearful', 'fidgety', 'jittery', 'restless', 'dread',
        'exam tomorrow', 'interview', 'meeting', 'deadline', 'unknown', 'fear of future', 'tight chest', 'shaky hands', 'racing thoughts'
    ],
    'confused': [
        'confused', 'unsure', 'uncertain', 'puzzled', 'doubtful', 'lost', 'baffled', 'disoriented', 'unclear', 'muddled', 'foggy', 'hesitant', 'unsettled',
        'don\'t understand', 'what to do', 'no idea', 'hard to decide', 'mixed signals'
    ],
    'neutral': [
        'hello', 'hi', 'okay', 'fine', 'normal', 'routine', 'alright', 'nothing much', 'good morning', 'good evening', 'hey', 'what\'s up', 'neutral', 'typical', 'usual', 'standard', 'okayish', 'decent', 'so-so',
        'just a day', 'average', 'working', 'boring', 'plain', 'neutral mood', 'blah', 'meh'
    ]
}

# Emoji for each emotion
emotion_emoji = {
    'happy': '😊',
    'sad': '😢',
    'angry': '😠',
    'anxious': '😰',
    'confused': '😕',
    'neutral': '🙂'
}

def detect_emotion_keywords(text):
    text = text.lower()
    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', text):
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
        emoji = emotion_emoji.get(keyword_emotion, '')
        return jsonify({'emotion': keyword_emotion, 'emoji': emoji})

    # Fall back to model prediction
    if not model:
        return jsonify({'error': 'Model not found'}), 500

    prediction = model.predict([text])[0]
    if not prediction:
        prediction = 'neutral'

    emoji = emotion_emoji.get(prediction, '')
    return jsonify({'emotion': prediction, 'emoji': emoji})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
