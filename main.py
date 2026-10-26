import time

from alarm import play_alert
from config import load_config
from sensors import get_cpu_temperature

def main():
    config = load_config()

    threshold = config["threshold"]
    interval = config["interval"]
    alert_sound = config["alert_sound"]
    
    alert_active = False
    
    print("Aotemp running")
    print(f"Threshold: {threshold:.1f} °C")
    print(f"Comprobation interval: {interval} seconds")
    print("Press Ctrl+C to stop.\n")
   
    try:
        while True:
            temperature=get_cpu_temperature()

            print(f"CPU temperature: {temperature:.1f} °C")
            
            if temperature>=threshold:
                print("WARNING")
                
                if not alert_active:
                    try:
                        play_alert(alert_sound)
                        alert_active = True
                    except (RuntimeError, FileNotFoundError, OSError) as error:
                        print(f"Alarm could not be played: {error}")
            else:
                print("A-OK")
                alert_active = False

            print()
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nAotemp stopped")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"Error de configuración: {error}")


