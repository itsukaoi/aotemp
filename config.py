import json
import math
from pathlib import Path


CONFIG_PATH = Path(__file__).with_name("config.json")

DEFAULT_CONFIG = {
    "threshold": 80.0,
    "interval": 5,
    "alarm_repeat_interval": 60,
    "alert_sound": "sounds/alert.mp3",
}


def load_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(
            json.dumps(DEFAULT_CONFIG, indent=4) + "\n",
            encoding="utf-8",
        )
        print("default config.json created")
        return DEFAULT_CONFIG.copy()

    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(
            f"invalid JSON: {error}"
        ) from error

    if not isinstance(config, dict):
        raise ValueError("config must be JSON")

    for key in DEFAULT_CONFIG:
        if key not in config:
            raise ValueError(f"Missing key '{key}' at config.json.")

    threshold = config["threshold"]
    interval = config["interval"]
    repeat_interval = config["alarm_repeat_interval"]
    alert_sound = config["alert_sound"]

    if (
        isinstance(threshold, bool)
        or not isinstance(threshold, (int, float))
        or not math.isfinite(threshold)
        or not 0 < threshold < 150
    ):
        raise ValueError("threshold must be a number between 0 and 150.")

    if (
        isinstance(interval, bool)
        or not isinstance(interval, int)
        or not 1 <= interval <= 3600
    ):
        raise ValueError("interval must be a number between 1 and 3600.")

    if (
        isinstance(repeat_interval, bool)
        or not isinstance(repeat_interval, int)
        or not 1 <= repeat_interval <= 86400
    ):
        raise ValueError(
            "alarm_repeat_interval must be an integer between 1 and 86400."
        )

    if not isinstance(alert_sound, str) or not alert_sound.strip():
        raise ValueError("alert_sound must be a non-empty file path")

    return config
