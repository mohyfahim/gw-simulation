from email import message
import json
from random import randint
import paho.mqtt.client as mqtt
import threading
import time
from constants import *
from jsonschema import validate
import random
import signal
import sys

receive_schema = {"type": "object",
                  "properties": {"oneOf": [{"tt": {"type": "string"}, "time": {"type": "string"},
                                            "conf": {"type": "array", "items": [{"type": "object",
                                                                                "properties": {"id": {"type": "string"}, "setT": {"type": "array"},
                                                                                               "permission": {"type": "number"}, "workmode": {"type": "number"},
                                                                                               "hvac": {"type": "number"}, "fan_command": {"type": "array"},
                                                                                               "valve_command": {"type": "array"}}}]}},
                                           {"tt": {"type": "string"}, "time": {"type": "string"},
                                            "conf": {"type": "object", "properties": {"out_temp": {"type": "number"},
                                                                                      "engine_temp": {"type": "number"}, "other_temp": {"type": "number"}}}}]}}
# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(SUB_TOPIC)

    message = None
    with open("init.json") as f:
        message = json.load(f)

    client.publish(PUB_TOPIC, json.dumps(message))
# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    if msg.topic == SUB_TOPIC:
        print(msg.topic+" "+str(msg.payload))
        data = json.loads(msg.payload)
        if data["type"] == "33":
            for co in data["conf"]:
                if(len(co["setT"]) != 4):
                    print("warn")
                print(co["id"], co["setT"], co["permission"], co["workmode"],
                      co["hvac"], co["fan_command"], co["valve_command"])
        elif data["type"] == "34":
            print(data["conf"]["out_temp"], data["conf"]
                  ["engine_temp"], data["conf"]["other_temp"])
        else:
            print("error in type code")
    else:
        print("error: invalid topic ", msg.topic)


def send_task(clnt):

    message = dict()
    message["type"] = "02"
    message["time"] = time.time()
    message["data"] = []
    for add in ADDRESSES:
        s = dict()
        s["id"] = add
        s["setT"] = 25
        s["homeT"] = 25 + random.randint(-2, 2)
        s["analogSensors"] = [255, 255]
        s["light"] = 88 + random.randint(-2, 2)
        s["humidity"] = 76 + random.randint(-2, 2)
        s["fancoilT"] = [
            26 + random.randint(-2, 2), 26 + random.randint(-2, 2), 27 + random.randint(-2, 2)]
        s["valveState"] = [1, 1, 1]
        s["fanState"] = [1, 0]
        s["present"] = 1
        message["data"].append(s)

    while True:
        clnt.publish(PUB_TOPIC, json.dumps(message))
        time.sleep(DELAY_TIMER)


if __name__ == "__main__":

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_URL, BROKER_PORT, 60)
    client.loop_start()

    t1 = threading.Thread(target=send_task, args=(client,))
    t1.start()
    t1.join()
    print("main task finished")
