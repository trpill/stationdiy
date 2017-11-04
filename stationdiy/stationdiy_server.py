import paho.mqtt.client as mqtt
import threading
import random
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("%s/%s/%s"%(s.user_hash,device,actioner))
    


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(userdata = "lala")
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)


def worker():
    client.loop_forever()
    return

t = threading.Thread(target=worker)
t.daemon = True
t.start()

client.user_data_set("lala")
for i in range(0,200):
	time.sleep(random.randint(0,5))
	client.publish("StationDiY/baurin.lg@gmail.com/Station1/temperatura A",random.randint(0,100))




