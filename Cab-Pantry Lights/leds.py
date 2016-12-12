# Raspberry Pi Talking To WiFi Things Part 4
# Use a push button connected to an ESP8266 to toggle a LED on a Raspberry Pi
# on and off, and a push button connected to the Pi to toggle a LED on the ESP8266
# on and off.  This version uses MQTT to send and receive LED control messages.
# Author: Tony DiCola
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Configuration:
STOVE_RIGHT_PIN = 24
STOVE_LEFT_PIN	= 23
SINK_RIGHT_PIN  = 17
SINK_LEFT_PIN   = 21
BUTTON_PIN      = 18
PANTRY_PIN      = 25
mqtt_qos=1

loop_count = 0

# Initialize GPIO for LED and button.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(STOVE_RIGHT_PIN, GPIO.OUT)
GPIO.setup(STOVE_LEFT_PIN, GPIO.OUT)
GPIO.setup(SINK_RIGHT_PIN, GPIO.OUT)
GPIO.setup(SINK_LEFT_PIN, GPIO.OUT)
GPIO.setup(PANTRY_PIN, GPIO.OUT)
GPIO.output(PANTRY_PIN, GPIO.HIGH)
GPIO.output(STOVE_RIGHT_PIN, GPIO.HIGH)
GPIO.output(STOVE_LEFT_PIN, GPIO.HIGH)
GPIO.output(SINK_RIGHT_PIN, GPIO.HIGH)
GPIO.output(SINK_LEFT_PIN, GPIO.HIGH)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup callback functions that are called when MQTT events happen like
# connecting to the server or receiving data from a subscribed feed.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/lights/kitchen/stoveleft")
    client.subscribe("/lights/kitchen/stoveright")
    client.subscribe("/lights/kitchen/sinkleft")
    client.subscribe("/lights/kitchen/sinkright")
    client.subscribe("/lights/kitchen/command")
    client.subscribe("/lights/kitchen/pantry")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('{0} got: {1}'.format(msg.topic, msg.payload))
    # Check if this is a message for the Pi LED.
    if msg.topic == '/lights/kitchen/stoveright':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            GPIO.output(STOVE_RIGHT_PIN, GPIO.LOW)
            client.publish('/lights/kitchen/stoveright/state', 'ON', qos=mqtt_qos)
        elif msg.payload == b'OFF':
            GPIO.output(STOVE_RIGHT_PIN, GPIO.HIGH)
            client.publish('/lights/kitchen/stoveright/state', 'OFF',qos=mqtt_qos)
        elif msg.payload == b'TOGGLE':
            GPIO.output(STOVE_RIGHT_PIN, not GPIO.input(STOVE_RIGHT_PIN))
    if msg.topic == '/lights/kitchen/stoveleft':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            GPIO.output(STOVE_LEFT_PIN, GPIO.LOW)
            client.publish('/lights/kitchen/stoveleft/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            GPIO.output(STOVE_LEFT_PIN, GPIO.HIGH)
            client.publish('/lights/kitchen/stoveleft/state', 'OFF',qos=mqtt_qos)
        elif msg.payload == b'TOGGLE':
            GPIO.output(STOVE_LEFT_PIN, not GPIO.input(STOVE_LEFT_PIN))
    if msg.topic == '/lights/kitchen/sinkleft':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            GPIO.output(SINK_LEFT_PIN, GPIO.LOW)
            client.publish('/lights/kitchen/sinkleft/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            GPIO.output(SINK_LEFT_PIN, GPIO.HIGH)
            client.publish('/lights/kitchen/sinkleft/state', 'OFF',qos=mqtt_qos) 
        elif msg.payload == b'TOGGLE':
            GPIO.output(SINK_LEFT_PIN, not GPIO.input(SINK_LEFT_PIN))
    if msg.topic == '/lights/kitchen/sinkright':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            GPIO.output(SINK_RIGHT_PIN, GPIO.LOW)
            client.publish('/lights/kitchen/sinkright/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            GPIO.output(SINK_RIGHT_PIN, GPIO.HIGH)
            client.publish('/lights/kitchen/sinkright/state', 'OFF',qos=mqtt_qos)
        elif msg.payload == b'TOGGLE':
            GPIO.output(SINK_RIGHT_PIN, not GPIO.input(SINK_RIGHT_PIN))
    if msg.topic == '/lights/kitchen/pantry':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            GPIO.output(PANTRY_PIN, GPIO.LOW)
            client.publish('/lights/kitchen/pantry/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            GPIO.output(PANTRY_PIN, GPIO.HIGH)
            client.publish('/lights/kitchen/pantry/state', 'OFF',qos=mqtt_qos)
        elif msg.payload == b'TOGGLE':
            GPIO.output(PANTRY_PIN, not GPIO.input(PANTRY_PIN))


    if msg.topic == '/lights/kitchen/command':
       # Look at the message data and perform the appropriate action.
        if msg.payload == b'status':
            if GPIO.input(STOVE_RIGHT_PIN) == 0:
                client.publish('/lights/kitchen/stoveright/state', 'ON',qos=mqtt_qos)
            else:
                client.publish('/lights/kitchen/stoveright/state', 'OFF',qos=mqtt_qos)
            if GPIO.input(STOVE_LEFT_PIN) == 0:
                client.publish('/lights/kitchen/stoveleft/state', 'ON',qos=mqtt_qos)
            else:
                client.publish('/lights/kitchen/stoveleft/state', 'OFF',qos=mqtt_qos)
            if GPIO.input(SINK_RIGHT_PIN) == 0:
                client.publish('/lights/kitchen/sinkright/state', 'ON',qos=mqtt_qos)
            else:
                client.publish('/lights/kitchen/sinkright/state', 'OFF',qos=mqtt_qos)
            if GPIO.input(SINK_LEFT_PIN) == 0:
                client.publish('/lights/kitchen/sinkleft/state', 'ON',qos=mqtt_qos)
            else:
                client.publish('/lights/kitchen/sinkleft/state', 'OFF',qos=mqtt_qos)
            if GPIO.input(PANTRY_PIN) == 0:
                client.publish('/lights/kitchen/pantry/state', 'ON',qos=mqtt_qos)
            else:
                client.publish('/lights/kitchen/pantry/state', 'OFF',qos=mqtt_qos)




# Create MQTT client and connect to localhost, i.e. the Raspberry Pi running
# this script and the MQTT server.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('10.10.10.122', 1883, 60)

# Connect to the MQTT server and process messages in a background thread.
client.loop_start()

# Main loop to listen for button presses.
print('Script is running, press Ctrl-C to quit...')

#if loop_count == 1000:
#  if GPIO.input(STOVE_RIGHT_PIN) == LOW:
#    client.publish('/lights/kitchen/stoveright/state', 'ON')
#  else:
#    client.publish('/lights/kitchen/stoverigth/state', 'OFF')
#  if GPIO.input(STOVE_LEFT_PIN) == LOW:
#    client.publish('/lights/kitchen/stoveleft/state', 'ON')
#  else:
#    client.publish('/lights/kitchen/stoveleft/state', 'OFF')
#  if GPIO.input(SINK_RIGHT_PIN) == LOW:
#    client.publish('/lights/kitchen/sinkright/state', 'ON')
#  else:
#    client.publish('/lights/kitchen/sinkright/state', 'OFF')
#  if GPIO.input(STOVE_LEFT_PIN) == LOW:
#    client.publish('/lights/kitchen/sinkleft/state', 'ON')
#  else:
#    client.publish('/lights/kitchen/sinkleft/state', 'OFF')
#  loop_count = 0

#print("loop %s" % loop_count)

#loop_count = loop_count + 1

while True:
    # Look for a change from high to low value on the button input to
    # signal a button press.
    button_first = GPIO.input(BUTTON_PIN)
    time.sleep(0.02)  # Delay for about 20 milliseconds to debounce.
    button_second = GPIO.input(BUTTON_PIN)
    if button_first == GPIO.HIGH and button_second == GPIO.LOW:
        print('Button pressed!')
        # Send a toggle message to the ESP8266 LED topic.
        client.publish('/leds/esp8266', 'TOGGLE')

