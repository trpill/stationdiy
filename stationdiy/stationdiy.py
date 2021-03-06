########### Dev : Baurin Leza ############
# Cliente MQTT de pruebas


import paho.mqtt.client as mqtt
import sys
import random
import requests
import threading
import json



class StationDiY():

    def __init__(self, host="stationdiy.eu", username = "", port = 80, \
        password = "", device = "", actioner = "", data_actioner = "", \
        sensor = "", data = "", longitud = "", latitud = "", type_data = "string", max_value = "", min_value = ""):
        
        self.host = host
        self.device = device
        self.sensor = sensor
        self.data = data
        self.actioner = actioner
        self.data_actioner = data_actioner
        self.longitud = longitud
        self.latitud = latitud
        self.port = port
        self.type_data = type_data
        self.max_value, self.min_value = max_value, min_value
        self.url = "http://%s:%s/api/"%(self.host, self.port)


    def login(self, username, password):
        """ Save auth credentials to objects return """

        self.action = "authenticate"
        payload = {'password': password, 'username': username}
        response = requests.post(self.url+"login/", data=payload)

        if response.status_code == 200 :
            self.username = username
            self.password = password
            self.authenticated = True
            self.user_hash = response.json()["user_hash"]
        else : 
            self.authenticated = False

    def register(self, username, password, last_name = "", first_name = ""):
        """ Save auth credentials to objects return """

        self.action = "register"
        payload = {'password1': password,"password2":password, 'username': username, "first_name" : first_name, "last_name":last_name}
        response = requests.post(self.url+"register/", data=payload)

        if response.status_code == 200 :
            print ("New user has been created")
        else : 
            print ("Error")
            print (response.text)

    
    def subscribe_actioner(self, device, actioner, on_data):
        
        """
        Subscribe to concrete actioner
        """

        def on_publish(mqttc, userdata, mid):
            mqttc.disconnect()

        def on_message(mqtcc, userdata, message):
            on_data(json.loads(message.payload))

        client = mqtt.Client()
        client.on_message = on_message
        client.connect(host=self.host, port=1883, keepalive=60, bind_address="")
        print ("Subscribe to --->  %s - %s"%(device,actioner))

        def worker():
            client.loop_forever()
            return

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        client.subscribe("StationDiy/actioner/%s/%s/%s"%(self.user_hash,device,actioner))

    def subscribe_sensor(self, device, sensor, on_data):
        
        """
        Subscribe to concrete actioner
        """



        def on_publish(mqttc, userdata, mid):
            mqttc.disconnect()

        def on_message(mqtcc, userdata, message):

            on_data(json.loads(message.payload))

        client = mqtt.Client()
        client.on_message = on_message
        client.connect(host=self.host, port=1883, keepalive=60, bind_address="")
        print ("Subscribe to --->  %s - %s"%(device,sensor))
        
        def worker():
            # print "WORKER"
            client.loop_forever()
            return

        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        # print "subscrito a ->"
        # print "StationDiy/sensor/%s/%s/%s"%(self.user_hash,device,sensor)
        client.subscribe("StationDiy/sensor/%s/%s/%s"%(self.user_hash,device,sensor))

    def sendMQTT(self, **kwargs):
        """ Send message """

        def on_connect(mqttc, userdata, rc):

            if "sensor" in kwargs:
                self.actioner = ""
                topic='StationDiy/sensor/%s/%s/%s'%(self.user_hash,kwargs["device"],  kwargs["sensor"])
            else:
                self.sensor = ""
                topic='StationDiy/actioner/%s/%s/%s'%(self.user_hash, kwargs["device"], kwargs["actioner"])

            #print "enviado a -> %s"%topic


            mqttc.publish(topic=topic,  payload='{ \
                "action":"%s","device":"%s",\
                "sensor":"%s","data":"%s", "actioner":"%s", "data_actioner":"%s", \
                "longitud":"%s", "latitud": "%s",\
                "description":"Lorem Ipsium Dev2...", "type_data":"%s", "max_value":"%s", \
                "min_value":"%s"}'%( \
                    self.action, \
                    self.device, self.sensor, self.data, self.actioner, \
                    self.data_actioner, self.longitud, self.latitud, self.type_data, \
                    self.max_value, self.min_value), qos=0)

        def on_disconnect(mqttc, userdata, rc):
            pass
            # print('Disconnect...rc=' + str(rc))

        def on_subscribe(mqttc, userdata, mid, granted_qos):
            print('subscribed (qos=' + str(granted_qos) + ')')
            

        def on_unsubscribe(mqttc, userdata, mid, granted_qos):
            print('unsubscribed (qos=' + str(granted_qos) + ')')

        def on_message(mqttc, userdata, msg):
            print('message received...')
            print ("-->%s"%userdata)
            print('topic: ' + msg.topic + ', qos: ' + 
                  str(msg.qos) + ', message: ' + str(msg.payload))

        def on_publish(mqttc, userdata, mid):
            mqttc.disconnect()

        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.on_message = on_message
        self.mqttc.on_publish = on_publish

        self.mqttc.connect(host=self.host, port=1883, keepalive=60, bind_address="")
        self.mqttc.loop_forever()

    def setSensor(self, **kwargs ):
        """ Set sensor by mqtt """

        self.device = kwargs["device"]
        self.sensor = kwargs["sensor"]
        self.data = kwargs["data"]
        if self.authenticated == True : self.sendMQTT(**kwargs)
        else: print ("No authenticated request api") 
        self.clear()

    def clear(self):
        self.device = ""
        self.sensor = ""
        self.actioner = ""

    def getSensorData(self,device,sensor):
        """ Get sensor by http method """
        # Get data
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username, 'sensor':sensor, 'device':device}
        response = requests.post(self.url+"getsensordata/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 


    def getSensors(self, device):
        """ Get Actioner data by http method """
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username, 'device':device}
        response = requests.post(self.url+"getsensors/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 


    def setActioner(self, **kwargs):
        """ Set actioner data by mqtt """
        self.device = kwargs["device"]
        self.actioner = kwargs["actioner"]
        self.data_actioner = kwargs["data"]
        if self.authenticated == True : self.sendMQTT(**kwargs)
        else: print ("No authenticated request api" )
        self.clear()

    def getActionerData(self, device, actioner):
        """ Get Actioner data by http method """
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username, 'actioner':actioner, 'device':device}
        response = requests.post(self.url+"getactionerdata/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 

    def getActioners(self, device):
        """ Get Actioner data by http method """
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username, 'device':device}
        response = requests.post(self.url+"getactioners/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 


    def getDevices(self):
        """ Get Actioner data by http method """
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username}
        response = requests.post(self.url+"getdevices/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 

    def removeDevices(self,device):
        """ Get Actioner data by http method """
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username, "device" : device }
        response = requests.post(self.url+"removedevice/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 

    def removeActioner(self, device, actioner):
        """ Get Actioner data by http method """
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username, "device":device, "actioner":actioner}
        response = requests.post(self.url+"removeactioner/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 

    def removeSensor(self,device,sensor):
        """ Get Actioner data by http method """
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username, "device":device, "sensor":sensor}
        response = requests.post(self.url+"removesensor/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 

    def setAlert(self, sensor, actioners, device_sensor, devices_actioners, minim, maxim, data):
        """ Set Action """
        if self.authenticated == False : 
            return -1

        payload = {'password': self.password, 'username': self.username, 'min':minim, 'max':maxim, "device_sensor":device_sensor, "devices_actioners":devices_actioners, "data":data, "sensor":sensor, "actioners": actioners}
        response = requests.post(self.url+"setalert/", data=payload)
        if response.status_code == 200 : return response.text
        else : return -1 

        
    # def setRemoteAlert(self, device, sensor, actioners):
    #     """ One sensor is able to actioner more than one actioners """
    #     # set remote alert
    # def subscribeSensor(self, device, sensor, callback):
    #     """ Subscribe to sensor """
    #     subscribe_client = mqtt.Client()
    #     subscribe_client.on_connect = on_connect
    #     subscribe_client.on_disconnect = on_disconnect
    #     subscribe_client.on_message = on_message
    #     subscribe_client.on_subscribe = on_subscribe

# python setup.py register -r pypitest
# python setup.py sdist upload -r pypitest
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
