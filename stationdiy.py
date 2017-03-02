########### Dev : Baurin Leza ############
# Cliente MQTT de pruebas


import paho.mqtt.client as mqtt
import sys
import random


def on_connect(mqttc, userdata, rc):
    mqttc.publish(topic='StationDiy/', 
                      payload='{"username":"baurin.lg@gmail.com","password":"rstuvw19","keyname_source":"Dev2","channel":"temperatura7","data":%s,"description":"Lorem Ipsium Dev2..."}'%random.randint(0,100), qos=0)

def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))

def on_message(mqttc, userdata, msg):
    print('message received...')
    print "-->%s"%userdata
    print('topic: ' + msg.topic + ', qos: ' + 
          str(msg.qos) + ', message: ' + str(msg.payload))

def on_publish(mqttc, userdata, mid):
    print('message published')
    mqttc.disconnect()

class StationDiY():

    def __init__(self, args):
        arg = args
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.on_message = on_message
        self.mqttc.on_publish = on_publish
        self.mqttc.connect(host="stationdiy.eu", port=1883, keepalive=60, bind_address="")
        self.mqttc.loop_forever()



#station = StationDiY('{"username":"baurin.lg@gmail.com","password":"rstuvw19","keyname_source":"Dev2","channel":"temperatura7","data":%s,"description":"Lorem Ipsium Dev2..."}'%random.randint(0,100))
