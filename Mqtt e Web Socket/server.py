import asyncio
import json
import logging

import tornado.web
import tornado.websocket
import aiomqtt

#BROKER = "test.mosquitto.org"
BROKER = "mqtt.ssh.edu.it"  #broker scolastico
#TOPIC = "Bianchini/sensor/"

clients = set()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class TempHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("temperature.html")
        self.TOPIC = "Bianchini/sensor/temperature"
        asyncio.create_task(mqtt_listener(self.TOPIC))

class HumidityHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("humidity.html")
        self.TOPIC = "Bianchini/sensor/humidity"
        asyncio.create_task(mqtt_listener(self.TOPIC))

class PressureHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pressure.html")
        self.TOPIC = "Bianchini/sensor/pressure"
        asyncio.create_task(mqtt_listener(self.TOPIC))

class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket aperto")
        clients.add(self)

    def on_close(self):
        print("WebSocket chiuso")
        clients.remove(self)


async def mqtt_listener(TOPIC):

    logging.info("Connessione al broker MQTT...")

    async with aiomqtt.Client(BROKER) as client:
        await client.subscribe(TOPIC)
        logging.info(f"Iscritto al topic: {TOPIC}")

        async for message in client.messages:
            payload = message.payload.decode()
            data = json.loads(payload)

            ws_message = json.dumps({
                "type": "sensor",
                "data": data
            })

            # inoltro ai client WebSocket
            for c in list(clients):
                await c.write_message(ws_message)


async def main():
    logging.basicConfig(level=logging.INFO)

    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/ws", WSHandler),
            (r"/temperature.html", TempHandler),
            (r"/humidity.html", HumidityHandler),
            (r"/pressure.html", PressureHandler),
            (r"/templates/(.*)", tornado.web.StaticFileHandler, {"path": "templates"}),
        ],
        template_path="templates",
    )

    app.listen(8888)
    print("Server Tornado avviato su http://localhost:8888")


    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())