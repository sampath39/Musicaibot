# train_emotion_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

# Training data
data = {
    'text': [
        "I feel happy today", "This is amazing!", "I'm very sad right now", "I'm feeling low and depressed",
        "What a wonderful day", "I am so angry!", "I'm confused about everything", "Life is beautiful",
        "I feel great and joyful", "I'm anxious and nervous", "I'm under pressure and stressed",
        "I feel relaxed and calm", "This is terrible and I hate it", "I'm full of joy and energy",
        "I hate this situation", "This is the best thing ever", "hello", "good morning", "hey",
        "just normal day", "nothing much", "it’s an okay day", "not too bad", "I'm feeling okay",
        "only happy", "just sad", "neutral", "angry", "anxious", "bored"
    ],
    'emotion': [
        "happy", "happy", "sad", "sad",
        "happy", "angry", "confused", "happy",
        "happy", "anxious", "anxious",
        "neutral", "angry", "happy",
        "angry", "happy", "neutral", "neutral", "neutral",
        "neutral", "neutral", "neutral", "neutral", "neutral",
        "happy", "sad", "neutral", "angry", "anxious", "neutral"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Split into training and test data
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['emotion'], test_size=0.2, random_state=42
)

# Build pipeline
model = make_pipeline(
    TfidfVectorizer(stop_words='english', lowercase=True),
    MultinomialNB()
)

# Train model
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'emotion_model.pkl')
print("Model saved as 'emotion_model.pkl'")
