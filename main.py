import re
import subprocess
import time
import json
from pathlib import Path

DEFAULT_CONFIG = {
     "threshold": 80.0,
    "interval": 5,
    "alert_sound": "sounds/alert.wav",
}

def get_cpu_temperature():
    result = subprocess.run(
        ["sensors", "k10temp-pci-00c3"],
        capture_output=True,
        text=True,
        check=True, #para generar una excepcion
        timeout=3, #para que no quede colgado
    )

    match = re.search(
        r"^\s*Tctl:\s*\+?(-?\d+(?:\.\d+)?)°C",
        result.stdout,
        re.MULTILINE
    )

    if match is None:
        raise ValueError("No se encontró una temperatura Tctl válida")

    return float(match.group(1))

def load_config():
    config_path=Path(__file__).with_name("config.json")

    if not config_path.exists():
        config_path.write_text(
            json.dumps(DEFAULT_CONFIG, indent=4) + "\n",
            encoding="utf-8",
        )
        print("Created default config.json")
        return DEFAULT_CONFIG.copy()
    
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Config.json contains invalid JSON: {error}"
        )from error

    if not isinstance(config, dict):
        raise ValueError("Config file must be JSON")
    
    for key in DEFAULT_CONFIG:
        if key not in config:
            raise ValueError(f"Missins key: {key}")
        
    threshold=config["threshold"]
    interval=config["interval"]
    alert_sound=config["alert_sound"]
    
    if(
        isinstance(threshold, bool)
        or not isinstance(threshold, (int, float))
        or not 0 < threshold < 150
    ):
        raise ValueError("threshold must be a number between 0 and 150")
    
    if (
        isinstance(interval, bool)
        or not isinstance(interval, int)
        or not 1 <= interval <= 3600
    ):
        raise ValueError("interval must be a numeber between 1 and 3600")
               
    if not isinstance(alert_sound, str) or not alert_sound.strip():
        raise ValueError("alert_sound must be a non-empty directory")

    return config

def main():
    config = load_config()

    threshold = config["threshold"]
    interval = config["interval"]
    alert_sound = config["alert_sound"]
    
    print("Aotemp running")
    print(f"Threshold: {threshold:.1f} °C")
    print(f"Comprobation interval: {interval} seconds")
    print("Press Ctrl+C to stop.\n")
   
    while True:
        temperature=get_cpu_temperature()

        print(f"CPU temperature: {temperature:.1f} °C")
        
        if temperature>=threshold:
            print("WARNING")
        else:
            print("A-OK")

        print()
        time.sleep(interval)




if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"Error de configuración: {error}")


