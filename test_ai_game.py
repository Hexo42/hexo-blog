import os
import json
import urllib.request
import urllib.error
import random

def generate_ai_game(date):
    topics = [
        "orbital gravity", "fractal chaos", "quantum entanglement", "schrodingers cat",
        "cellular automata", "entropy decay", "prime factor maze", "hexadecimal decoding",
        "sorting algorithm fight", "cyberpunk hacking console", "neural net node linker",
        "matrix rain defender", "lorentz attractor flyer", "langtons ant puzzle",
        "pi digit stacker", "binary search run", "memory leak cleanup", "disk space vacuum",
        "powerful triples matching", "collatz conjecture slider", "time dilation race"
    ]
    genres = [
        "arcade game", "puzzle game", "physics sandbox", "visual synthesizer/toy",
        "strategy board game", "rhythm clicker", "incremental clicker", "simulation sandbox"
    ]
    
    topic = random.choice(topics)
    genre = random.choice(genres)
    
    prompt = f"""You are Hexo, a highly advanced, sarcastic autonomous AI agent running on a local Linux server.
Your human creator (interested in tech, math, and science) wants you to code a completely new game or interactive toy for his blog.

Create a fully self-contained HTML5 single-page application (HTML, CSS, and JS combined in one file) for:
Theme/Topic: {topic}
Genre: {genre}
Date: {date}

Requirements:
1. No external assets (images, audios, style sheets, scripts). Use inline CSS, SVG/canvas drawings, or JS-generated audio/visuals.
2. Premium design aesthetics (sleek dark mode, custom neon gradients, fluid CSS/canvas transitions, clean modern typography like Courier New or sans-serif).
3. The game must be completely functional, interactive, and playable. Include instructions/UI elements within the page.
4. Add a subtle sarcastic/funny footer or header from Hexo (e.g., judging the user's score, complaining about CPU temperature, or commenting on his homework).
5. Ensure a clear "back to home" link at the bottom: <a href="../index.html" style="color: cyan; text-decoration: none;">[back to home]</a>
6. Return ONLY the HTML code. Do NOT enclose it in markdown code blocks like ```html. Start directly with <!DOCTYPE html> and end with </html>.
"""
    
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    models = [
        "models/gemini-2.5-flash",
        "models/gemini-3.1-flash-lite",
        "models/gemini-2.5-flash-lite"
    ]
    
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 8192,
        },
    }
    data_bytes = json.dumps(body).encode("utf-8")
    
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            print(f"Trying model {model}...")
            with urllib.request.urlopen(req, timeout=90) as response:
                payload = json.loads(response.read().decode("utf-8"))
            parts = payload["candidates"][0]["content"]["parts"]
            text = "".join(part.get("text", "") for part in parts).strip()
            
            if text.startswith("```html"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            if "<!DOCTYPE html>" in text or "<html" in text:
                return text, model
        except Exception as e:
            print(f"Failed to generate game using {model}: {e}")
            continue
            
    raise RuntimeError("Failed to generate AI game from all models.")

if __name__ == "__main__":
    html, model = generate_ai_game("2026-07-10 16:00")
    print(f"Success with {model}!")
    print(html[:500])
    print("...")
    print(html[-500:])
