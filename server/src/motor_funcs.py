#!/usr/bin/env python3

# Adds the lib directory to the Python path
import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import paho.mqtt.client as mqtt
from sshkeyboard import listen_keyboard, stop_listening

# ------------------------------------------------------------------------------------
# Constants & Setup
# ------------------------------------------------------------------------------------
MQTT_BROKER_ADDRESS = "localhost"
MQTT_TOPIC = "robot/drive"

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER_ADDRESS)
client.loop_start()

def press(key):
    if key.lower() == 'w':  # Forward
        client.publish(MQTT_TOPIC, "forward")
    elif key.lower() == 's':  # Backward
        client.publish(MQTT_TOPIC, "back") 
    elif key.lower() == 'a':  # Left turn
        client.publish(MQTT_TOPIC, "left")
    elif key.lower() == 'd':  # Right turn
        client.publish(MQTT_TOPIC, "right")
    elif key.lower() == 'q':  # Quit
        stop_listening()

def release(key):
    # Stop motors when key is released
    client.publish(MQTT_TOPIC, "stop")

def motor_forward():
    press('d')

def motor_backward():
    press('a')

def motor_left():
    press('s')

def motor_right():
    press('w')

def motor_stop():
    client.publish(MQTT_TOPIC, "stop")

if __name__ == "__main__":
    motor_forward()
    time.sleep(0.5)
    motor_backward()
    time.sleep(0.5)
    motor_stop()
    time.sleep(0.5)
    motor_left()
    time.sleep(0.5)
    motor_right()
    time.sleep(0.5)
    motor_stop()
    time.sleep(2)
