"""Build self-contained index.html by inlining mp3 base64 into template.

Run: `python3 assets/build.py`
Reads: assets/template.html + assets/*.mp3
Writes: index.html (root)
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CLIPS = {
    "AUDIO_PASSAGE": "passage.mp3",
    "AUDIO_VOCAB_FAVORITE": "vocab_favorite.mp3",
    "AUDIO_VOCAB_YOUNGER_SISTER": "vocab_younger_sister.mp3",
    "AUDIO_VOCAB_TOOK_PICTURES": "vocab_took_pictures.mp3",
    "AUDIO_VOCAB_GOOD_TIME": "vocab_good_time.mp3",
}


def main():
    with open(os.path.join(HERE, "template.html"), "r", encoding="utf-8") as f:
        html = f.read()
    for placeholder, fname in CLIPS.items():
        path = os.path.join(HERE, fname)
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        html = html.replace("{{" + placeholder + "}}", b64)
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    size_kb = os.path.getsize(out) / 1024
    print(f"built {out} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
