"""
Train a simple vibration classifier using block-based features.

- Input: CSV dataset with extracted features
- Output: Trained ML model saved to disk

This script is intentionally simple and explicit, serving as a
reference training pipeline for edge deployment.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from pathlib import Path


# -----------------------------
# Configuration
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data/raw/dataset.csv"
MODEL_OUTPUT_PATH = PROJECT_ROOT / "models/idle_vibration_model.joblib"
TEST_SIZE = 0.25
RANDOM_STATE = 42


def main():
    print("Loading dataset...")

    COLUMNS = [
    "timestamp",
    "rms_x", "rms_y", "rms_z",
    "mean_x", "mean_y", "mean_z",
    "std_x", "std_y", "std_z",
    "rms_mag", "std_mag",
    "label",
    ]
    df = pd.read_csv(DATASET_PATH, names=COLUMNS, header=0)

    print(f"Dataset shape: {df.shape}")
    print(df.head())

    # -----------------------------
    # Split features / labels
    # -----------------------------
    X = df.drop(columns=["label", "timestamp"], errors="ignore")
    y = df["label"]

    print(f"Features shape: {X.shape}")
    print(f"Labels distribution:\n{y.value_counts()}")

    # -----------------------------
    # Train / test split
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # -----------------------------
    # ML pipeline
    # -----------------------------
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            max_iter=100000,
            class_weight="balanced"
        ))
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)

    # -----------------------------
    # Evaluation
    # -----------------------------
    y_pred = pipeline.predict(X_test)

    print("\nClassification report:")
    print(classification_report(y_test, y_pred, digits=3))

    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    # -----------------------------
    # Save model
    # -----------------------------
    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_OUTPUT_PATH)

    print(f"\nModel saved to: {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
