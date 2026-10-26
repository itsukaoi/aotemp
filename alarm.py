
import shutil
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def play_alert(sound_path):
    player = shutil.which("pw-play")

    if player is None:
        raise RuntimeError("pw-play not found.")

    sound_file = (BASE_DIR / sound_path).resolve()

    if not sound_file.is_file():
        raise FileNotFoundError(
            f"sound file not found: {sound_file}"
        )

    subprocess.Popen(
        [player, str(sound_file)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
