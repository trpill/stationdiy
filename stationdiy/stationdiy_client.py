
import paho.mqtt.client as mqtt
import threading
import random
import time


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    print "-"*10

client = mqtt.Client()
client.on_message = on_message

client.connect("localhost", 1883, 60)


def worker():
    client.loop_forever()
    return

t = threading.Thread(target=worker)
t.daemon = True
t.start()

client.subscribe("StationDiY/baurin.lg@gmail.com/Station1/temperatura A")

s.user_hash, device, 
# "%s/%s/%s"%(data["user_hash"],data["device"],data["sensor"]),data["data"]
mqttc.publish("%s/%s/%s"%(s.user_hash,device,actioner)