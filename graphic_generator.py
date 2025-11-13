from diffusers import StableDiffusionPipeline
import torch
import pandas as pd

# Load the Stable Diffusion model once
pipe = StableDiffusionPipeline.from_pretrained(
    "nitrosocke/mo-di-diffusion",
    torch_dtype=torch.float32
).to("cpu")


def generate_comic_images(csv_path: str):
    """
    Reads script.csv and generates comic-style images using the Stable Diffusion model.
    
    Expected columns in CSV:
    - Background
    - Character
    - Character's Information
    """
    # Read CSV file
    df = pd.read_csv(csv_path)

    # Check for required columns
    required_cols = ["Background", "Character", "Character's Information"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"CSV file must contain these columns: {required_cols}")

    # Drop rows with missing values in essential columns
    # df = df.dropna(subset=required_cols).reset_index(drop=True)

    # Loop through each row and generate an image
    for i, row in df.iterrows():
        background = row["Background"]
        character = row["Character"]
        info = row["Character's Information"]

        # Build the prompt
        prompt = (
            f"{character}, {info}, set against {background}, "
            f"vibrant colors, dynamic composition, comic book art style, "
            f"dramatic lighting, highly detailed illustration"
        )

        # Generate the image
        image = pipe(prompt).images[0]
        
        # Save image with sequential numbering
        filename = f"comic_scene_{i+1}.png"
        image.save(filename)

        print(f" Saved {filename}")
        print(f"Prompt: {prompt}\n")

        print(" All comic scenes generated successfully!")


# Example usage:
# generate_comic_images("script.csv")
