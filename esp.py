import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# ----------------------------
# Configuration
# ----------------------------
broker_address = "10.0.0.131"  # If running on same Pi
topic = "esp/led"
ledPin = 18  # GPIO pin for external LED

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, GPIO.LOW)

# ----------------------------
# MQTT Callback
# ----------------------------
def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8").upper()
    print(f"Received: {msg}")

    if msg == "ON":
        GPIO.output(ledPin, GPIO.HIGH)
    elif msg == "OFF":
        GPIO.output(ledPin, GPIO.LOW)
    elif msg.startswith("BLINK"):
        # Optional: BLINK 200 ? blink interval in ms
        parts = msg.split()
        interval = 500  # default
        if len(parts) == 2:
            try:
                interval = int(parts[1])
            except:
                pass
        # Blink LED 5 times
        for _ in range(5):
            GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(interval / 1000)
            GPIO.output(ledPin, GPIO.LOW)
            time.sleep(interval / 1000)

# ----------------------------
# Connect to MQTT Broker
# ----------------------------
client = mqtt.Client(client_id="PiSubscriber")
client.connect(broker_address)
client.subscribe(topic)
client.on_message = on_message

print("Waiting for messages from ESP32...")
try:
    client.loop_forever()
except KeyboardInterrupt:
    GPIO.cleanup()
