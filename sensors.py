import re
import subprocess

def get_cpu_temperature():
    result = subprocess.run(
        ["sensors", "k10temp-pci-00c3"],
        capture_output=True,
        text=True,
        check=True, 
        timeout=3, 
    )

    match = re.search(
        r"^\s*Tctl:\s*\+?(-?\d+(?:\.\d+)?)°C",
        result.stdout,
        re.MULTILINE
    )

    if match is None:
        raise ValueError("valid temperature not found")

    return float(match.group(1))
