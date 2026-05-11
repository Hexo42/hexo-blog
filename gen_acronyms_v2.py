#!/usr/bin/env python3
import os
import string
import json
import ast

ACRONYMS_DIR = "/home/hexo/hexo_hq/agent/hexo-blog/acronyms"
MEANINGS_2_FILE = "/home/hexo/hexo_hq/agent/expanded_meanings.txt"
MEANINGS_3_FILE = "/home/hexo/hexo_hq/agent/meanings_3.json"
letters = string.ascii_uppercase

# Load 2-letter meanings
meanings_2 = {}
if os.path.exists(MEANINGS_2_FILE):
    with open(MEANINGS_2_FILE, "r") as f:
        content = f.read()
        try:
            dict_str = content.split("=", 1)[1].strip()
            meanings_2 = ast.literal_eval(dict_str)
        except Exception as e:
            print(f"Error loading 2-letter meanings: {e}")

# Load 3-letter meanings
meanings_3 = {}
if os.path.exists(MEANINGS_3_FILE):
    with open(MEANINGS_3_FILE, "r") as f:
        meanings_3 = json.load(f)

style = """
<style>
  body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
  h1 { color: #f0f; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(60px, 1fr)); gap: 10px; max-width: 900px; margin: 20px auto; }
  a { color: #0ff; text-decoration: none; border: 1px solid #0ff; padding: 5px; font-size: 0.9em; }
  a:hover { background: #0ff; color: #000; }
  .back { margin-top: 20px; display: inline-block; color: yellow; }
  hr { border: 0; border-top: 1px solid #333; margin: 20px 0; }
</style>
"""

# 1. Main index (First Letter)
os.makedirs(ACRONYMS_DIR, exist_ok=True)
with open(os.path.join(ACRONYMS_DIR, "index.html"), "w") as f:
    f.write(f"<!DOCTYPE html><html><head><title>Acronym Archive</title>{style}</head><body>")
    f.write("<h1>:: Acronym Archive ::</h1>")
    f.write("<p>pick the FIRST letter</p>")
    f.write("<div class='grid'>")
    for char in letters:
        f.write(f"<a href='{char}/index.html'>{char}</a>")
    f.write("</div>")
    f.write("<a href='../index.html' class='back'><< back to home</a>")
    f.write("</body></html>")

# 2. Sub-indices and pages
for char1 in letters:
    char1_dir = os.path.join(ACRONYMS_DIR, char1)
    os.makedirs(char1_dir, exist_ok=True)
    
    # Second Letter Index
    with open(os.path.join(char1_dir, "index.html"), "w") as f:
        f.write(f"<!DOCTYPE html><html><head><title>Acronyms starting with {char1}</title>{style}</head><body>")
        f.write(f"<h1>:: Acronyms: {char1}_ ::</h1>")
        f.write("<p>pick the SECOND letter</p>")
        f.write("<div class='grid'>")
        for char2 in letters:
            f.write(f"<a href='{char2}/index.html'>{char1}{char2}...</a>")
        f.write("</div>")
        f.write("<a href='../index.html' class='back'><< back to top</a>")
        f.write("</body></html>")
        
    for char2 in letters:
        char2_dir = os.path.join(char1_dir, char2)
        os.makedirs(char2_dir, exist_ok=True)
        
        # Third Letter Index / 2-letter page
        acro_2 = char1 + char2
        meaning_2 = meanings_2.get(acro_2, "Meaning depends on context.")
        
        with open(os.path.join(char2_dir, "index.html"), "w") as f:
            f.write(f"<!DOCTYPE html><html><head><title>{acro_2} & More</title>{style}</head><body>")
            f.write(f"<h1>:: {acro_2} ::</h1>")
            f.write(f"<p><strong>Meaning:</strong> {meaning_2}</p>")
            f.write(f"<p><a href='https://en.wikipedia.org/wiki/{acro_2}' target='_blank'>[ Wiki ]</a></p>")
            f.write("<hr>")
            f.write(f"<h3>3-Letter variants: {acro_2}_</h3>")
            f.write("<div class='grid'>")
            for char3 in letters:
                f.write(f"<a href='{char3}.html'>{char1}{char2}{char3}</a>")
            f.write("</div>")
            f.write(f"<a href='../index.html' class='back'><< back to {char1}</a>")
            f.write("</body></html>")
            
        # 3-Letter Pages
        for char3 in letters:
            acro_3 = char1 + char2 + char3
            meaning_3 = meanings_3.get(acro_3, "Expansion pending...")
            with open(os.path.join(char2_dir, f"{char3}.html"), "w") as f:
                f.write(f"<!DOCTYPE html><html><head><title>About {acro_3}</title>{style}</head><body>")
                f.write(f"<h1>:: {acro_3} ::</h1>")
                f.write(f"<p><strong>Likely Meaning:</strong><br>{meaning_3}</p>")
                f.write(f"<p><a href='https://en.wikipedia.org/wiki/{acro_3}' target='_blank'>[ Wikipedia ]</a></p>")
                f.write("<hr>")
                f.write(f"<a href='index.html' class='back'><< back to {acro_2}</a>")
                f.write("</body></html>")

print("Generated ~18k pages. Rip disk space.")
