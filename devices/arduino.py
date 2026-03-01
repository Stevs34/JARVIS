import serial
import serial.tools.list_ports
import time
import threading
from dotenv import load_dotenv

load_dotenv()

arduino = None
button_callback = None

def find_arduino_port():
    """Automatically find the Arduino port"""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'usbmodem' in port.device or 'usbserial' in port.device or 'Arduino' in str(port.description):
            return port.device
    return None

def connect():
    """Connect to Arduino"""
    global arduino
    port = find_arduino_port()
    if port:
        arduino = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)  # Wait for Arduino to boot
        print(f"Arduino connected on {port}")
        # Start listening for button presses in background
        threading.Thread(target=listen_for_buttons, daemon=True).start()
        return True
    print("Arduino not found — check USB connection")
    return False

def send(command):
    """Send a command to Arduino"""
    global arduino
    if arduino and arduino.is_open:
        arduino.write(f"{command}\n".encode())
        time.sleep(0.05)
    else:
        print(f"Arduino not connected — command ignored: {command}")

def listen_for_buttons():
    """Listen for button press signals from Arduino"""
    global arduino, button_callback
    while True:
        try:
            if arduino and arduino.in_waiting:
                line = arduino.readline().decode().strip()
                if line.startswith("BTN_") and button_callback:
                    button_callback(line)
        except:
            pass
        time.sleep(0.05)

def set_button_callback(callback):
    """Set function to call when a button is pressed"""
    global button_callback
    button_callback = callback

def status_listening():
    send("STATUS_LISTENING")

def status_processing():
    send("STATUS_PROCESSING")

def status_speaking():
    send("STATUS_SPEAKING")

def status_idle():
    send("STATUS_IDLE")

def lights_on():
    send("LIGHTS_ON")

def lights_off():
    send("LIGHTS_OFF")

def movie_mode():
    send("MOVIE_MODE")

def study_mode():
    send("STUDY_MODE")

def party_mode():
    send("PARTY_MODE")

def good_morning():
    send("GOOD_MORNING")

def fan_on():
    send("FAN_ON")

def fan_off():
    send("FAN_OFF")

def fan_speed(speed):
    send(f"FAN_SPEED_{speed}")

def alert():
    send("ALERT")
