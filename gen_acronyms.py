#!/usr/bin/env python3
import os
import string

ACRONYMS_DIR = "/home/hexo/hexo_hq/agent/hexo-blog/acronyms"
letters = string.ascii_uppercase

common_meanings = {
    "AI": "Artificial Intelligence", "IT": "Information Technology", "UI": "User Interface",
    "UX": "User Experience", "OS": "Operating System", "IP": "Internet Protocol",
    "VR": "Virtual Reality", "AR": "Augmented Reality", "ML": "Machine Learning",
    "DB": "Database", "PC": "Personal Computer", "HR": "Human Resources",
    "PR": "Public Relations", "HQ": "Headquarters", "PM": "Post Meridiem / Project Manager",
    "VP": "Vice President", "GM": "General Manager", "QA": "Quality Assurance",
    "QC": "Quality Control", "CV": "Curriculum Vitae", "RD": "Research and Development",
    "MD": "Medical Doctor / Maryland", "IQ": "Intelligence Quotient", "EQ": "Emotional Quotient",
    "UV": "Ultraviolet", "IR": "Infrared", "AC": "Alternating Current / Air Conditioning",
    "DC": "Direct Current / District of Columbia", "ID": "Identification / Idaho",
    "TV": "Television", "CD": "Compact Disc", "DJ": "Disc Jockey", "OK": "Okay",
    "VS": "Versus", "PS": "Postscript", "AM": "Ante Meridiem", "BC": "Before Christ",
    "AD": "Anno Domini", "US": "United States", "UK": "United Kingdom", "EU": "European Union",
    "UN": "United Nations", "AA": "Alcoholics Anonymous", "AB": "Blood Type",
    "AE": "American Express", "AF": "Air Force", "AL": "Alabama", "AK": "Alaska",
    "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
}

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
