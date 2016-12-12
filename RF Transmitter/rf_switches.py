# Raspberry Pi Talking To WiFi Things Part 4
# Use a push button connected to an ESP8266 to toggle a LED on a Raspberry Pi
# on and off, and a push button connected to the Pi to toggle a LED on the ESP8266
# on and off.  This version uses MQTT to send and receive LED control messages.
# Author: Tony DiCola
import time
import sys
import os
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Configuration:
NUM_ATTEMPTS = 10
TRANSMIT_PIN = 23
BUTTON_PIN = 25
mqtt_qos=1
short_delay = 0.00045
long_delay = 0.00090
extended_delay = 0.0096
protocol = 1
pulselength = 186
bedroom_fan_on = 4199731
bedroom_fan_off = 4199740
guestroom_fan_on = 4199875
guestroom_fan_off = 4199884
lr_fan_on = 4207875
lr_fan_off = 4207884
charger_ad_6p_on = 4200195
charger_ad_6p_off = 4200204
kombucha_mat_on = 4201731
kombucha_mat_off = 4201740
office_light_on = 1135923
office_light_off = 1135932
ad_nightstand_on = 1136067
ad_nightstand_off = 1136076
tree_twinkle_on = 1137923
tree_twinkle_off = 1137932
tree_solid_on = 1136387
tree_solid_off = 1136396

loop_count = 0

# Initialize GPIO for LED and button.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN)


# Setup callback functions that are called when MQTT events happen like
# connecting to the server or receiving data from a subscribed feed.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/switches/rf/bedroom_fan")
    client.subscribe("/switches/rf/guestroom_fan")
    client.subscribe("/switches/rf/lr_fan")
    client.subscribe("/switches/rf/charger_ad_6p")
    client.subscribe("/switches/rf/kombucha_mat")
    client.subscribe("/switches/rf/office_light")
    client.subscribe("/switches/rf/ad_nightstand")
    client.subscribe("/switches/rf/tree_solid")
    client.subscribe("/switches/rf/tree_twinkle")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('{0} got: {1}'.format(msg.topic, msg.payload))
    # Check if this is a message for the Pi LED.
    if msg.topic == '/switches/rf/bedroom_fan':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(bedroom_fan_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/bedroom_fan/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(bedroom_fan_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/bedroom_fan/state', 'OFF',qos=mqtt_qos)
    if msg.topic == '/switches/rf/guestroom_fan':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(guestroom_fan_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/guestroom_fan/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(guestroom_fan_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/guestroom_fan/state', 'OFF',qos=mqtt_qos)
    if msg.topic == '/switches/rf/lr_fan':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(lr_fan_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/lr_fan/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(lr_fan_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/lr_fan/state', 'OFF',qos=mqtt_qos)           
    if msg.topic == '/switches/rf/charger_ad_6p':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(charger_ad_6p_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/charger_ad_6p/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(charger_ad_6p_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/charger_ad_6p/state', 'OFF',qos=mqtt_qos)
    if msg.topic == '/switches/rf/kombucha_mat':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(kombucha_mat_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/kombucha_mat/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(kombucha_mat_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/kombucha_mat/state', 'OFF',qos=mqtt_qos)
    if msg.topic == '/switches/rf/office_light':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(office_light_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/office_light/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(office_light_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/office_light/state', 'OFF',qos=mqtt_qos)
    if msg.topic == '/switches/rf/ad_nightstand':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(ad_nightstand_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/ad_nightstand/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(ad_nightstand_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/ad_nightstand/state', 'OFF',qos=mqtt_qos)
    if msg.topic == '/switches/rf/tree_twinkle':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(tree_twinkle_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/tree_twinkle/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(tree_twinkle_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/tree_twinkle/state', 'OFF',qos=mqtt_qos)
    if msg.topic == '/switches/rf/tree_solid':
        # Look at the message data and perform the appropriate action.
        if msg.payload == b'ON':
            os.system("sudo /home/pi/codesend " + str(tree_solid_on) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/tree_solid/state', 'ON',qos=mqtt_qos)
        elif msg.payload == b'OFF':
            os.system("sudo /home/pi/codesend " + str(tree_solid_off) + " " + str(protocol) + " " + str(pulselength))
            client.publish('/switches/rf/tree_solid/state', 'OFF',qos=mqtt_qos)            

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


