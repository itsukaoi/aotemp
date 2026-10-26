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

    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    return config

def main():
    config = load_config()

    threshold=config["threshold"]
    interval=config["interval"]
    alert_sound=config["alert_sound"]

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
    main()


