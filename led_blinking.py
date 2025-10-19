from gpiozero import LED
from time import sleep

led = LED(17)  # GPIO pin where LED is connected

while True:
    led.on()
    sleep(0.5)   # Blink faster
    led.off()
    sleep(0.5)
