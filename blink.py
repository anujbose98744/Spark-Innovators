import paho.mqtt.client as mqtt
import time

# ----------------------------
# Configuration
# ----------------------------
broker_address = "10.0.0.131"  # Replace with your Raspberry Pi IP
topic = "esp/led"
blink_interval = 0.5  # seconds

# ----------------------------
# Connect to MQTT Broker
# ----------------------------
client = mqtt.Client(client_id="PiPublisher")

try:
    client.connect(broker_address)
    print(f"Connected to MQTT Broker at {broker_address}")
except Exception as e:
    print("Failed to connect to broker:", e)
    exit(1)

# ----------------------------
# Menu-based control
# ----------------------------
try:
    while True:
        print("\nSelect LED action:")
        print("1. ON")
        print("2. OFF")
        print("3. BLINK")
        choice = input("Enter choice (1/2/3): ").strip()

        if choice == "1":
            client.publish(topic, "ON")
            print("LED turned ON")

        elif choice == "2":
            client.publish(topic, "OFF")
            print("LED turned OFF")

        elif choice == "3":
            print("LED blinking. Press Ctrl+C to stop blinking...")
            led_state = "OFF"
            try:
                while True:
                    led_state = "ON" if led_state == "OFF" else "OFF"
                    client.publish(topic, led_state)
                    print(f"Sent command: {led_state}")
                    time.sleep(blink_interval)
            except KeyboardInterrupt:
                print("Stopped blinking. Returning to menu...")
                client.publish(topic, "OFF")  # Turn off LED after blinking

        else:
            print("Invalid choice! Enter 1, 2, or 3.")

except KeyboardInterrupt:
    print("\nExiting program...")
    client.publish(topic, "OFF")
    client.disconnect()