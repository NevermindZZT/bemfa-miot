# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt

import config
from module.projector import Projector


HOST = config.HOST
PORT = config.PORT
CLIENT_ID = config.CLIENT_ID
PROJECTOR_BT_ADDRESS = config.PROJECTOR_BT_ADDRESS

client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
projector = Projector(client, PROJECTOR_BT_ADDRESS)

#连接并订阅
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    projector.subscribe()  # 订阅投影仪相关主题

#消息接收
def on_message(client, userdata, msg):
    print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('utf-8')))
    if msg.topic.startswith("Projector"):
        projector.on_massage(msg.topic, msg.payload.decode('utf-8'))

#订阅成功
def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)

# 失去连接
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


client.username_pw_set("userName", "passwd")
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect
client.connect(HOST, PORT, 60)
client.loop_forever()