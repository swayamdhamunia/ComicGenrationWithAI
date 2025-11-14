import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas as pd
from comic_maker import generate_comic_page


def add_caption_to_6_images(res_folder="res", 
                             script_file="script.csv",
                             output_folder="Graphics_with_dialogue",
                             font_path="comic.ttf",
                             font_size=40,
                             max_width=25):
    """
    Reads 6 images from res/, reads Dialogues from script.csv,
    adds one dialogue to each image, and saves them into Graphics_with_dialogue/.
    """

    # ---- Step 1: Load 6 images ----
    images = sorted([
        os.path.join(res_folder, img)
        for img in os.listdir(res_folder)
        if img.lower().endswith((".png", ".jpg", ".jpeg"))
    ])[:6]

    if len(images) < 6:
        print(" ERROR: Less than 6 images found inside the 'res' folder.")
        return

    # ---- Step 2: Load script.csv and extract Dialogues column ----
    df = pd.read_csv(script_file)

    if "Dialogues" not in df.columns:
        print(" ERROR: No 'Dialogues' column found in script.csv.")
        return

    dialogues1 = df["Dialogues"].tolist()
    dialogues=[]
    for i in dialogues1:
        temp_d=i.split(",")
        dialogues.append(temp_d[0])

    if len(dialogues) < 6:
        print(" ERROR: script.csv must contain at least 6 dialogue lines.")
        return

    # ---- Step 3: Create output folder ----
    os.makedirs(output_folder, exist_ok=True)

    # ---- Step 4: Process images one by one ----
    for idx, (image_path, caption) in enumerate(zip(images, dialogues)):
        output_path = os.path.join(output_folder, f"comic_with_caption_{idx+1}.png")

        add_comic_caption_single(
            image_path=image_path,
            output_path=output_path,
            caption=caption,
            position=(50, 50),
            font_path=font_path,
            font_size=font_size,
            max_width=max_width
        )

    print(f" All 6 images processed and saved in: {output_folder}")


def add_comic_caption_single(image_path, output_path, caption, position=(50, 50),
                             font_path="comic.ttf", font_size=40, max_width=25):
    """
    Adds a single comic-style caption to one image.
    (Original logic preserved exactly)
    """

    img = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()
        print(" Comic font not found. Using default font.")

    wrapped_text = textwrap.fill(caption, width=max_width)

    text_bbox = draw.multiline_textbbox(position, wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    padding = 10
    bubble_x0 = position[0] - padding
    bubble_y0 = position[1] - padding
    bubble_x1 = position[0] + text_width + padding
    bubble_y1 = position[1] + text_height + padding

    draw.rounded_rectangle(
        [bubble_x0, bubble_y0, bubble_x1, bubble_y1],
        radius=20,
        fill=(255, 255, 255, 230),
        outline=(0, 0, 0),
        width=3
    )

    draw.multiline_text(position, wrapped_text, font=font, fill=(0, 0, 0))
    img.save(output_path)

    print(f"Caption added : {output_path}")
    generate_comic_page()
