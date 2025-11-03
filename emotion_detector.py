# src/emotion_detector.py

from transformers import pipeline
import os

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


def analyze_file(input_file, output_file):
    """
    Analyze emotions in a text file and save results to another file.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"⚠️ No text found in {input_file}")
        return

    detected_emotions = detect_emotion(text)

    # Save results in Python file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"emotions = {detected_emotions}\n")

    print(f"Analysis complete. Results saved in {output_file}")
    print("Top Emotions:", detected_emotions)


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))

    input_file = os.path.join(folder, "input.txt")
    output_file = os.path.join(folder, "emotion_results.py")

    analyze_file(input_file, output_file)
