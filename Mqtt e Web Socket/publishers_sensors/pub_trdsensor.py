from datetime import datetime
import time
import random
import json
import paho.mqtt.client as mqtt

#BROKER = "test.mosquitto.org"
BROKER = "mqtt.ssh.edu.it"  #broker scolastico
TOPIC = "sensor/??"

client = mqtt.Client()
client.connect(BROKER, 1883)

print("Sensore simulato avviato")

while True:
    value = round(random.uniform(18, 30), 2)

    payload = {
        "sensor": "??",
        "value": value,
        "unit": "C",#cambiala
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

    client.publish(TOPIC, json.dumps(payload))
    print("Pubblicato:", payload)

    time.sleep(1)