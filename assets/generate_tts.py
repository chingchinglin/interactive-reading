"""Generate TTS audio clips with Gemini, convert PCM->WAV->MP3.

Run once: `python3 assets/generate_tts.py`
Outputs: assets/*.mp3
"""
import base64
import json
import os
import struct
import subprocess
import sys
import urllib.request

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise SystemExit("Missing GEMINI_API_KEY env var. Run: export GEMINI_API_KEY=...")
MODEL = "gemini-2.5-flash-preview-tts"
VOICE = "Aoede"
SAMPLE_RATE = 24000

CLIPS = {
    "passage": (
        "Last Sunday I went to the zoo with my family. We saw many animals. "
        "Tigers are my favorite animals. My younger sister likes bears and monkeys. "
        "It was a sunny day, and we took many pictures. We had a good time."
    ),
    "vocab_favorite": "favorite. Tigers are my favorite animals.",
    "vocab_younger_sister": "younger sister. My younger sister likes bears and monkeys.",
    "vocab_took_pictures": "took pictures. We took many pictures.",
    "vocab_good_time": "have a good time. We had a good time.",
}


def synth(text: str) -> bytes:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{MODEL}:generateContent?key={API_KEY}"
    )
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}
            },
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    b64 = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    return base64.b64decode(b64)


def wav_wrap(pcm: bytes, rate: int = SAMPLE_RATE) -> bytes:
    # 16-bit mono PCM -> WAV
    n = len(pcm)
    header = b"RIFF" + struct.pack("<I", 36 + n) + b"WAVE"
    fmt = b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16)
    data = b"data" + struct.pack("<I", n) + pcm
    return header + fmt + data


def to_mp3(wav_bytes: bytes, out_path: str) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", "pipe:0", "-codec:a", "libmp3lame",
         "-b:a", "64k", out_path],
        input=wav_bytes, check=True,
    )


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    for name, text in CLIPS.items():
        out = os.path.join(out_dir, f"{name}.mp3")
        if os.path.exists(out):
            print(f"skip {name} (exists)")
            continue
        print(f"synth {name}...", end=" ", flush=True)
        pcm = synth(text)
        wav = wav_wrap(pcm)
        to_mp3(wav, out)
        size = os.path.getsize(out)
        print(f"ok ({size} bytes)")


if __name__ == "__main__":
    main()
