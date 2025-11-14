# src/emotion_detector.py

from transformers import pipeline
import os
from dialogue_generator import generate_comic_csv

# Load Hugging Face emotion detection pipeline
emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

THRESHOLD = 0.05  # 5% threshold


def detect_emotion(text):
    """
    Detect top emotions in the given text with filtering rules.
    """
    results = emotion_pipeline(text)[0]

    # Convert results to dictionary
    emotions = {res["label"]: res["score"] for res in results}

    # Filter emotions below threshold
    filtered = {k: v for k, v in emotions.items() if v >= THRESHOLD}

    if not filtered:
        # If everything is below threshold, pick max
        max_emotion = max(emotions, key=emotions.get)
        return {max_emotion: emotions[max_emotion]}

    # Find the max confidence score
    max_score = max(filtered.values())

    # Get all emotions that match the max confidence
    top_emotions = {k: v for k, v in filtered.items() if abs(v - max_score) < 1e-5}

    return top_emotions


def run_emotion_analysis():
    """
    Combines analyze_file() and the script's main behavior into one function.
    Functionality is unchanged. This simply wraps the entire main workflow.
    """
    folder = os.path.dirname(os.path.abspath(__file__))

    input_file = os.path.join(folder, "input.txt")
    output_file = os.path.join(folder, "emotion_results.txt")

    # --- analyze_file logic preserved exactly ---
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"No text found in {input_file}")
        return

    detected_emotions = detect_emotion(text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"emotions = {detected_emotions}\n")

    print(f"Analysis complete. Results saved in {output_file}")
    print("Top Emotions:", detected_emotions)

    # Original final line preserved exactly
    generate_comic_csv("input.txt", "emotion_results.txt", "script.csv")


# HOW TO CALL:
# run_emotion_analysis()
