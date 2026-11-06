"""
generate_audio.py - (re)create the voice-scam audio clips in assets/audio/.

The app already ships with all clips, so you only need this to ADD or CHANGE voices.

    pip install edge-tts
    python generate_audio.py            # create missing clips
    python generate_audio.py --force    # recreate all clips

Voices: free Microsoft Edge neural voices (Malay, English-SG/IN/GB/US, Mandarin, Tamil...).
List them with:  edge-tts --list-voices
If ffmpeg is installed, a "phone line" effect is added (narrow band + light line noise).

ETHICS: use synthetic voices or voices of people who gave written consent. Never clone a real
person's voice without permission.
"""
import asyncio
import os
import shutil
import ssl
import subprocess
import sys

from content_expert import AUDIO_CLIPS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio")


def phone_effect(src, dst):
    """Band-limit to 300-3400 Hz (like a phone line) and mix in faint line noise."""
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-i", src,
        "-f", "lavfi", "-i", "anoisesrc=color=pink:amplitude=0.008:duration=120",
        "-filter_complex",
        "[0:a]adelay=350|350,highpass=f=300,lowpass=f=3400,acompressor=threshold=-18dB:ratio=3[v];"
        "[1:a]highpass=f=300,lowpass=f=3400[n];"
        "[v][n]amix=inputs=2:duration=first:weights='1 0.5',volume=1.8",
        "-ac", "1", "-ar", "22050", "-b:a", "48k", dst,
    ]
    subprocess.run(cmd, check=True)


async def make(name, cfg, force=False):
    import edge_tts
    import edge_tts.communicate as comm_mod

    dst = os.path.join(OUT, name)
    if os.path.exists(dst) and not force:
        return "skip"
    # Optional: corporate networks with their own CA bundle
    if os.environ.get("TTS_CA_BUNDLE"):
        comm_mod._SSL_CTX = ssl.create_default_context(cafile=os.environ["TTS_CA_BUNDLE"])
    raw = dst + ".raw.mp3"
    comm = edge_tts.Communicate(cfg["text"], cfg["voice"], rate=cfg.get("rate", "+0%"),
                                pitch=cfg.get("pitch", "+0Hz"), proxy=os.environ.get("HTTPS_PROXY"))
    await comm.save(raw)
    if cfg.get("phone") and shutil.which("ffmpeg"):
        phone_effect(raw, dst)
        os.remove(raw)
    else:
        os.replace(raw, dst)
    return "made"


async def main():
    os.makedirs(OUT, exist_ok=True)
    force = "--force" in sys.argv
    for name, cfg in AUDIO_CLIPS.items():
        try:
            print(f"{await make(name, cfg, force):5}  {name}  ({cfg['voice']})")
        except Exception as e:  # noqa: BLE001
            print(f"FAIL   {name}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
