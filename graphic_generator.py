from diffusers import StableDiffusionPipeline
import torch
import pandas as pd

pipe = StableDiffusionPipeline.from_pretrained(
    "nitrosocke/mo-di-diffusion",
    torch_dtype=torch.float32
).to("cpu")

df = pd.read_csv("gen_info.csv")

backgrounds = df["background"].dropna().tolist()
character_actions = df["character_action"].dropna().tolist()
character_scenes = df["character_scene"].dropna().tolist()
character_info = df["character_info"].dropna().tolist()

def build_prompt(background: str, action: str, scene: str, info: str) -> str:
    return (
        f"{action}, {info}, in {scene}, set against {background}, "
        f"vibrant colors, dramatic shading, comic book art, highly detailed illustration"
    )

for i, action in enumerate(character_actions):
    prompt = build_prompt(
        background=backgrounds[i % len(backgrounds)],
        action=action,
        scene=character_scenes[i % len(character_scenes)],
        info=character_info[i % len(character_info)]
    )
    image = pipe(prompt).images[0]
    image.save(f"comic_scene_{i+1}.png")
    print(f"Saved comic_scene_{i+1}.png with prompt:\n{prompt}\n")
