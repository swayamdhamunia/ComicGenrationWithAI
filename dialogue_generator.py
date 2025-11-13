import ollama
import os
import csv
from graphic_generator import generate_comic_images

def generate_comic_csv(input_file: str, emotion_file: str, output_csv: str):
    """
    Reads input text and detected emotions from files,
    uses the LLaMA model to generate a structured 6-scene comic script,
    and saves the result in CSV format.

    CSV Format: Scene, Background, Character, Dialogues
    """

    def read_file(file_path):
        """Reads content from a file."""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        else:
            print(f"File not found: {file_path}")
            return ""

    def prompt(user_text, emotions):
        """Generates a structured comic script using LLaMA model."""
        desired_model = 'llama3.2:3b'

        ask = f"""
You are a creative comic writer. Based on the following text and detected emotions,
generate exactly 6 comic scenes in a structured CSV-like format with the following columns:

Scene, Background, Character, Dialogues, Character's Information

Guidelines:
- Each scene should have a short, clear description of the background and setting.
- The background and character’s information should evolve sequentially, 
  as in a continuous comic storyline (e.g., if the first scene is a sunny park, 
  the next might shift subtly to a nearby café or the same park in the evening).
- Include color tones, lighting, and small environmental details (like "soft golden light", "rustling leaves").
- Each scene must include at least one character with a short dialogue (1–2 lines).
- Include brief character information (appearance, attire, or emotional expression).
- Keep the tone and expressions aligned with the detected emotions.
- Do not add any extra explanations, markdown, or commentary.
- Output should strictly look like CSV rows (comma-separated).
-Provide full background details like scene, light and every necessary details to ensure that if needed , the same background is generated again,dont use (the same....) for backgrounds, provide full again .Only if needed else new background.

Example format:
Scene 1, A sunny park with soft golden light, Alex, "I feel the breeze today!", A young man in casual clothes, smiling confidently.
Scene 2, A sunny park with soft golden light,near a cafe, Mia, "This coffee smells amazing.", A cheerful woman with short hair, wearing a yellow jacket.

Now generate 6 such scenes below based on the input.


Text:
{user_text}

Detected Emotions:
{emotions}
        """

        response = ollama.chat(
            model=desired_model,
            messages=[{
                'role': 'user',
                'content': ask,
            }]
        )

        return response['message']['content']

    # Read input and emotion files
    user_text = read_file(input_file)
    detected_emotions = read_file(emotion_file)

    if not user_text:
        print("Input text file is empty or missing!")
        return None
    if not detected_emotions:
        print("Emotion results file is empty or missing!")
        return None

    # Generate the structured CSV data from LLaMA
    csv_text = prompt(user_text, detected_emotions)

    # Clean and parse into rows
    lines = [line.strip() for line in csv_text.split("\n") if line.strip()]
    csv_rows = [line.split(",", 3) for line in lines if "," in line]

    # Save the data to CSV
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Scene", "Background", "Character", "Dialogues","Character's Information"])
        writer.writerows(csv_rows)

    print(f" Comic scene CSV generated and saved to {output_csv}")
    generate_comic_images("script.csv")

    


# Example usage:
# generate_comic_csv("input.txt", "emotion_results.txt", "comic_script.csv")
