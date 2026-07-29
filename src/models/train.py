import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

from src.data.load_data import load_data
from src.data.clean_text import clean_text

def build_and_train():
    print("📦 Loading datasets...")
    df = load_data()    
    # Drop missing values
    df = df.dropna(subset=['text', 'sentiment'])
    
    print("🧹 Cleaning text data...")
    df['cleaned_text'] = df['text'].astype(str).apply(clean_text)
    
    X = df['cleaned_text']
    y = df['sentiment']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("🤖 Building ML Pipeline (TF-IDF + Logistic Regression)...")
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    
    print("🏋️ Training model...")
    model_pipeline.fit(X_train, y_train)
    
    # Evaluation
    preds = model_pipeline.predict(X_test)
    print("\n--- Model Performance ---")
    print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
    print("\nClassification Report:\n", classification_report(y_test, preds))
    
    # Save Model Artifact
    model_path = "src/models/sentiment_pipeline.pkl"
    joblib.dump(model_pipeline, model_path)
    print(f"\n✅ Trained model pipeline saved successfully to {model_path}!")

if __name__ == "__main__":
    build_and_train()