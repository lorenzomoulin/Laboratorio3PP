import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
import multiprocessing
import desafios

def oi(tdata):
    print("thread")

def on_message(client, userdata, message):
    print(message.payload.decode("utf-8"))
    dcd_msg = message.payload.decode("utf-8").split("/")
    print(dcd_msg)

# mqttBroker = '127.0.0.1'
mqttBroker = 'broker.emqx.io'

client = mqtt.Client("Node_1")
client.connect(mqttBroker)

client.loop_start()

listaDesafios = [desafios.Challenge(0, 1)]

client.publish("ppd/challenge", listaDesafios[-1].encode_challenge(), qos=1)

print("Just published ", 
        listaDesafios[-1].encode_challenge(), 
        " to topic ppd/challenge")

client.subscribe("ppd/seed")
client.on_message=on_message

while True:
    ultimo_desafio = listaDesafios[-1]
    if ultimo_desafio.get_winner() != -1:
        listaDesafios.append(desafios.Challenge(ultimo_desafio.transactionID+1, ultimo_desafio.challenge+1))
        client.publish("ppd/challenge", listaDesafios[-1].encode_challenge())
        print("Just published ", listaDesafios[-1].encode_challenge(), " to topic ppd/challenge")
    time.sleep(1)

client.loop_stop()