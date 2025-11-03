import ollama
import os

# llama model implementation
def prompt(user_text, emotions):
    desired_model = 'llama3.2:3b'

    # Construct a prompt that includes both text and detected emotions
    ask = f"""
You are a creative comic writer. Based on the following text and detected emotions, 
generate a short comic scene script with dialogues and storyline.

Text:
{user_text}

Detected Emotions:
{emotions}

Please provide the output in a script-like format with characters, dialogues, and narration.
    """

    response = ollama.chat(
        model=desired_model,
        messages=[{
            'role': 'user',
            'content': ask,
        }]
    )

    final = response['message']['content']
    return final


def read_file(file_path):
    """Reads content from a file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    else:
        print(f"File not found: {file_path}")
        return ""


if __name__ == "__main__":
    folder = os.path.dirname(os.path.abspath(__file__))

    input_file = os.path.join(folder, "input.txt")
    emotion_file = os.path.join(folder, "emotion_results.txt")
    script_file = os.path.join(folder, "script.txt")

    # Read input and emotions
    user_text = read_file(input_file)
    detected_emotions = read_file(emotion_file)

    if not user_text:
        print("Input text file is empty or missing!")
    elif not detected_emotions:
        print("Emotion results file is empty or missing!")
    else:
        # Generate script using LLaMA
        script = prompt(user_text, detected_emotions)

        # Save the script
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script)

        print("Comic scene script generated and saved to script.txt")
