def generate_comic_page():
    """
    generate_comic_page()

    Generates a stylish 6-panel anime-themed comic HTML page and layout XML
    using all images from ./res (or RES_DIR below).
    """

    import os
    import random
    from pathlib import Path
    from xml.etree.ElementTree import Element, SubElement, ElementTree

    # ---------------- CONFIG ----------------
    RES_DIR = Path(r"C:\Users\Lenovo\OneDrive\Desktop\Shruti\New folder\ComicGenrationWithAI\res")
    OUTPUT_HTML = Path("comic_page.html")
    OUTPUT_XML = Path("layout.xml")
    RNG_SEED = 42
    CAPTIONS = {}
    # -----------------------------------------

    random.seed(RNG_SEED)

    # Gather images
    if not RES_DIR.exists() or not RES_DIR.is_dir():
        raise SystemExit(f"Folder '{RES_DIR}' not found. Create it and add images.")

    images = sorted([p for p in RES_DIR.iterdir() if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp')])
    if not images:
        raise SystemExit(f"No supported images found in '{RES_DIR}'.")

    # Only use first 6 images (as requested)
    images = images[:6]

    # Panels metadata
    panels = []
    for i, img in enumerate(images):
        panels.append({
            "id": f"panel{i+1}",
            "src": str(img).replace("\\", "/"),
            "caption": CAPTIONS.get(img.name, "")
        })

    # Generate XML
    root = Element("comic")
    for p in panels:
        pe = SubElement(root, "panel", attrib={"id": p["id"]})
        SubElement(pe, "src").text = p["src"]
        SubElement(pe, "caption").text = p["caption"]
    ElementTree(root).write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)
    print(f"XML layout saved: {OUTPUT_XML}")

    # HTML + CSS
    html_start = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Anime Comic</title>
<link href="https://fonts.googleapis.com/css2?family=Bangers&family=Roboto:wght@400;700&family=Luckiest+Guy&display=swap" rel="stylesheet">
<style>
body {
    margin: 0;
    background: radial-gradient(circle at top left, #1b0034, #090016 70%);
    background-attachment: fixed;
    font-family: 'Roboto', sans-serif;
    overflow-x: hidden;
    color: #fff;
}

header {
    font-family: 'Luckiest Guy', cursive;
    font-size: 58px;
    color: #ff3df0;
    text-align: center;
    text-shadow: 3px 3px 0 #000, 0 0 15px #ff9dff, 0 0 30px #ff47f5;
    padding: 25px 10px;
    background: linear-gradient(180deg, #2c0059, #1b0034);
    border-bottom: 6px solid #ff3df0;
    letter-spacing: 2px;
}

.comic-page {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 22px;
    padding: 40px;
}

.panel {
    background: linear-gradient(135deg, #2b004a, #120027);
    border: 5px solid #ff47f5;
    border-radius: 10px;
    padding: 6px;
    box-shadow: 0 0 25px rgba(255, 71, 245, 0.4), 8px 8px 0 rgba(0,0,0,0.5);
    transform: rotate(calc(var(--tilt) * 1deg));
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.panel:hover {
    transform: rotate(0deg) scale(1.05);
    box-shadow: 0 0 35px rgba(255, 71, 245, 0.8);
    z-index: 3;
}
.panel img {
    width: 100%;
    height: auto;
    object-fit: contain;
    display: block;
    background: #000;
    border: 3px solid #ff47f5;
    border-radius: 8px;
    filter: contrast(1.15) saturate(1.3);
}

.caption {
    font-family: 'Bangers', cursive;
    background: rgba(255, 255, 255, 0.12);
    border: 2px solid #ff47f5;
    border-radius: 6px;
    padding: 6px 12px;
    position: absolute;
    bottom: 12px;
    left: 12px;
    font-size: 20px;
    color: #ffecff;
    text-shadow: 2px 2px 0 #000;
    backdrop-filter: blur(5px);
    box-shadow: 0 0 12px rgba(255, 71, 245, 0.6);
}

#lightbox {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(10, 0, 20, 0.95);
    align-items: center;
    justify-content: center;
    z-index: 9999;
}
#lightbox img {
    max-width: 90%;
    max-height: 90%;
    border: 6px solid #ff47f5;
    border-radius: 10px;
    box-shadow: 0 0 40px rgba(255, 71, 245, 0.8);
}
</style>
</head>
<body>
<header>✨ Anime Adventures ✨</header>
<main class="comic-page">
"""

    html_panels = ""
    for p in panels:
        tilt = random.choice([-2, -1, 0, 1, 2])
        cap_html = f'<div class="caption">{p["caption"]}</div>' if p["caption"] else ""
        html_panels += f"""
<div class="panel" style="--tilt: {tilt};" id="{p['id']}">
  <img src="{p['src']}" alt="{p['id']}" loading="lazy">
  {cap_html}
</div>
"""

    html_end = """
</main>
<div id="lightbox">
  <img id="lightboxImg" src="">
</div>
<script>
document.addEventListener('click', function(e){
  const panel = e.target.closest('.panel');
  if(panel){
    const img = panel.querySelector('img');
    if(img){
      const lb = document.getElementById('lightbox');
      const lbimg = document.getElementById('lightboxImg');
      lbimg.src = img.src;
      lb.style.display = 'flex';
    }
  }
  if(e.target.id === 'lightbox'){
    e.target.style.display = 'none';
    document.getElementById('lightboxImg').src = '';
  }
});
</script>
</body>
</html>
"""

    OUTPUT_HTML.write_text(html_start + html_panels + html_end, encoding="utf-8")
    print(f"HTML page saved: {OUTPUT_HTML}")
    print("✨ Open comic_page.html in your browser to view your anime-style comic!")

