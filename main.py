import time

from alarm import play_alert
from config import load_config
from sensors import get_cpu_temperature

def main():
    config = load_config()

    threshold = config["threshold"]
    interval = config["interval"]
    alert_sound = config["alert_sound"]
    alarm_repeat_interval = config["alarm_repeat_interval"]
    last_alarm_time = None
    
    print("Aotemp running")
    print(f"Threshold: {threshold:.1f} °C")
    print(f"Comprobation interval: {interval} seconds")
    print("Press Ctrl+C to stop.\n")
   
    try:
        while True:
            temperature=get_cpu_temperature()
            current_time= time.monotonic()
            
            print(f"CPU temperature: {temperature:.1f} °C")
            
            if temperature>=threshold:
                print("WARNING")
                
                should_alert = (
                    last_alarm_time is None
                    or current_time - last_alarm_time >= alarm_repeat_interval
                )    
                
                if should_alert:
                    try:
                        play_alert(alert_sound)
                        last_alarm_time = current_time
                    except(RuntimeError, FileNotFoundError, OSError) as error:
                        print(f"Alarm could not be played: {error}")
            else:
                print("A-OK")
                last_alarm_time = None

            print()
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nAotemp stopped")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"Error de configuración: {error}")


