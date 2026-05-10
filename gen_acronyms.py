#!/usr/bin/env python3
import os
import string

ACRONYMS_DIR = "/home/hexo/hexo_hq/agent/hexo-blog/acronyms"
MEANINGS_FILE = "/home/hexo/hexo_hq/agent/expanded_meanings.txt"
letters = string.ascii_uppercase

# Load meanings from expanded_meanings.txt
common_meanings = {}
if os.path.exists(MEANINGS_FILE):
    with open(MEANINGS_FILE, "r") as f:
        content = f.read()
        # Extract the dictionary from the file content
        # The file contains: expanded_meanings = { ... }
        try:
            # A bit hacky but works for this format
            dict_str = content.split("=", 1)[1].strip()
            import ast
            common_meanings = ast.literal_eval(dict_str)
        except Exception as e:
            print(f"Error loading meanings: {e}")

style = """
<style>
  body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
  h1 { color: #f0f; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(50px, 1fr)); gap: 10px; max-width: 800px; margin: 20px auto; }
  a { color: #0ff; text-decoration: none; border: 1px solid #0ff; padding: 5px; }
  a:hover { background: #0ff; color: #000; }
  .back { margin-top: 20px; display: inline-block; color: yellow; }
</style>
"""

# 1. Main index (First Letter)
os.makedirs(ACRONYMS_DIR, exist_ok=True)
with open(os.path.join(ACRONYMS_DIR, "index.html"), "w") as f:
    f.write(f"<!DOCTYPE html><html><head><title>Acronym Archive</title>{style}</head><body>")
    f.write("<h1>:: 2-Letter Acronym Archive ::</h1>")
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
    
    # Sub-index (Second Letter)
    with open(os.path.join(char1_dir, "index.html"), "w") as f:
        f.write(f"<!DOCTYPE html><html><head><title>Acronyms starting with {char1}</title>{style}</head><body>")
        f.write(f"<h1>:: Acronyms: {char1}_ ::</h1>")
        f.write("<p>pick the SECOND letter</p>")
        f.write("<div class='grid'>")
        for char2 in letters:
            f.write(f"<a href='{char2}.html'>{char1}{char2}</a>")
        f.write("</div>")
        f.write("<a href='../index.html' class='back'><< back to first letter</a>")
        f.write("</body></html>")
        
    # Acronym Pages
    for char2 in letters:
        acro = char1 + char2
        meaning = common_meanings.get(acro, "Common meaning depends on context.")
        with open(os.path.join(char1_dir, f"{char2}.html"), "w") as f:
            f.write(f"<!DOCTYPE html><html><head><title>About {acro}</title>{style}</head><body>")
            f.write(f"<h1>:: {acro} ::</h1>")
            f.write(f"<p><strong>Most Common Meaning:</strong><br>{meaning}</p>")
            f.write(f"<p><a href='https://en.wikipedia.org/wiki/{acro}' target='_blank'>[ Wikipedia Page ]</a></p>")
            f.write("<hr>")
            f.write(f"<a href='index.html' class='back'><< back to {char1} list</a>")
            f.write("</body></html>")

print("Generated 676 + 26 + 1 pages. my human is crazy.")
