from datetime import datetime
import random
import asyncio
import json
import logging
import paho.mqtt.client as mqtt

#BROKER = "test.mosquitto.org"
BROKER = "mqtt.ssh.edu.it"  #broker scolastico
client = mqtt.Client()
client.connect(BROKER, 1883)
print("Sensore simulato avviato")

async def mqtt_pubisher(type_sensor):
    if type_sensor == "temperature":
        pass


#si sceglie un sensore e si inviano i dati
async def main():
    logging.basicConfig(level=logging.INFO)




    TOPIC = "sensor/temperature"

    asyncio.create_task(mqtt_pubisher("temperature"))

    await asyncio.Event().wait()




if __name__ == "__main__":
    asyncio.run(main())