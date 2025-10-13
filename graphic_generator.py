from diffusers import StableDiffusionPipeline
import torch


pipe = StableDiffusionPipeline.from_pretrained(
    "nitrosocke/mo-di-diffusion",
    torch_dtype=torch.float32
).to("cpu")


background = "a bustling futuristic city street at sunset, glowing neon signs, detailed buildings, cyberpunk comic style"


actions = [
    "a masked vigilante leaping across rooftops",
    "a superhero flying through the sky with a trail of light",
    "a robot chasing a thief through the crowd",
    "a mysterious figure standing in the rain, holding a glowing sword"
]


for i, action in enumerate(actions):
    prompt = f"{action}, {background}, vibrant colors, dramatic shading, comic book art"
    image = pipe(prompt).images[0]
    image.save(f"comic_scene_{i+1}.png")
    print(f"Saved comic_scene_{i+1}.png")
