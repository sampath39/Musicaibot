import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

# Sample data
data = {
    'text': [
        "I feel so happy today!",
        "I'm feeling really sad",
        "This is a wonderful experience",
        "I am very angry right now",
        "I feel so great and joyful",
        "I don't know what to do, I feel confused",
        "I'm really stressed and anxious",
        "I'm full of joy",
        "This makes me sad",
        "I'm in a great mood today"
    ],
    'emotion': [
        "happy", "sad", "happy", "angry", "happy", "neutral",
        "anxious", "happy", "sad", "happy"
    ]
}

# Dataframe
df = pd.DataFrame(data)
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['emotion'], test_size=0.2, random_state=42)

# Train model
model = make_pipeline(TfidfVectorizer(stop_words='english'), MultinomialNB())
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'emotion_model.pkl')
print("Model saved as emotion_model.pkl")
