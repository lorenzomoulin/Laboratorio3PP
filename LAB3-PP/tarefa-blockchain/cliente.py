import paho.mqtt.client as mqtt
import time
import multiprocessing

def brute(tdata, n):
    

def on_message(client, userdata, message):
    msg=str(message.payload.decode("utf-8"))
    print(msg)
    msg_chunks = msg.split('/')
    if(message.topic=='ppd/challenge'):
        challenge={"transactionID":msg_chunks[0],"challenge":msg_chunks[1]}

        #brute
    if(message.topic=='ppd/result'):
        result={"transactionID":msg_chunks[0],"clientID":msg_chunks[1],"seed":msg_chunks[2]}



#mqttBroker = "172.31.89.188"
mqttBroker = "broker.emqx.io"
client = mqtt.Client("Node_3")
client.connect(mqttBroker)
client.loop_start()
client.subscribe("ppd/challenge", qos=1)
client.subscribe("ppd/result", qos=1)


seed=0



client.on_message=on_message
time.sleep(30000)
client.loop_stop()