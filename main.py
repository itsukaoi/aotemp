import re
import subprocess

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


def main():
    temperature=get_cpu_temperature()
    print(f"Temperatura actual de la CPU: {temperature:.1f} °C")


if __name__ == "__main__":
    main()


