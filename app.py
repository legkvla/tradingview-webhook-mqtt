import os
import time
from fastapi import FastAPI, Request
from paho.mqtt import client as mqtt_client
from typing import Dict, Any
from dotenv import load_dotenv

MQTT_HOST=os.getenv("MQTT_HOST", 'localhost')
MQTT_PORT=int(os.getenv("MQTT_PORT", '1883'))
MQTT_USERNAME=os.getenv("MQTT_USERNAME", '')
MQTT_PASSWORD=os.getenv("MQTT_PASSWORD", '')
MQTT_TOPIC=os.getenv("MQTT_TOPIC", 'signals')
SEC_KEY=os.getenv("SEC_KEY", 'DEFAULT_KEY')


app = FastAPI()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client("ibkr")
    client.tls_set(ca_certs='./emqxsl-ca.crt')
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT)
    return client

topic = MQTT_TOPIC

def publish(client):
    client.loop_start()
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break
    client.loop_stop()

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()

@app.get("/")
async def root():
    return {"message": "TradingView-Webhook-MQTT-Bridge"}


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    headers = request.headers
    qparams = request.query_params
    pparams = request.path_params

    if 'text/plain' in headers['content-type']:
        raise ValueError('Alert Message must be of type application/json')
    elif 'application/json' in headers['content-type']:
        data = await request.json()
        if 'key' not in data:
            raise ValueError('Missing key!')
        key = data['key']
        if key == SEC_KEY:
            if 'data' not in data:
                raise ValueError(
                    'Wrong Alert message format, "data" field not found!')
                return 400
            msg = TradingViewAlert(data=data['data'])
            if 'topic' in data:
                topic = data['topic']
                if topic == '':
                    topic = MQTT_TOPIC
            else:
                topic = MQTT_TOPIC
            print(f'Publishing TradingView Alert @ {topic}')
            mqtt_pub.publish(msg, topic)
            return 200
        else:
            return 400
