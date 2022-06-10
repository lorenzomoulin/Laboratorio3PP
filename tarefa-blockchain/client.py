import hashlib
import random
import string
import paho.mqtt.client as mqtt
import time
import multiprocessing
import desafios
import json
import random

kill_threads = False
cur_tid = -1
cur_challenge = -1
# mqttBroker = 'broker.emqx.io'
# mqttBroker = '127.0.0.1'
clientID = 777
seed = ""
resolveu = False
mqttBroker = "test.mosquitto.org"

def on_publish(client, userdata, mid):
    print(f"Client: renan é gay published message: {mid}")

def testHash(challengeTuple):
    str = challengeTuple["seed"]
    id= challengeTuple["transactionID"]
    challenge= challengeTuple['challenge']
    
    
    encoded_str = str.encode()

    # create a sha1 hash object initialized with the encoded string
    hash_obj = hashlib.sha1(encoded_str)

    # convert the hash object to a hexadecimal value
    hash = hash_obj.hexdigest()

    i=0 
    bin_value=[]
    count=0 
    valid=1 
    
    while(i<40 and count<challenge and valid==1):
        bin_value = bin(int(hash[i], base=16))[2:].zfill(4)
        # print(bin_value)
        for element in bin_value:
            if element =='0':
                count+=1
            else: 
                valid=0
                return 0
        i+=1           
    return 1
    
def brute(tdata: desafios.Challenge):
    finish=0
    global kill_threads
    global resolveu
    resultado=False
    i=0
    while(finish==0 and not kill_threads):
        #status=1 ainda tem desafio
        # status=proxy.getTransactionStatus(tdata['tID'])

        res = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k = 7))
        ct=desafios.Challenge(tdata.transactionID,tdata.challenge,seed=str(res))
        
        resultado=ct.check_seed(ct.seed)

        if(resultado):
            print(vars(ct))
            break
            
       
    if(resultado):
        vars(ct)["clientID"]=clientID
        resolveu = True
        seed = ct.seed
        client.publish("ppd/seed",json.dumps(vars(ct)), qos=2)
        print("ok")     


def on_message(client, userdata, message):
    msg=json.loads(message.payload.decode("utf-8"))
    print(msg)
    global kill_threads
    global cur_tid
    global resolveu
    global cur_challenge
    if(message.topic=='ppd/challenge'):
        if cur_tid == -1:
            print("aqui")
            challenge=desafios.Challenge(transactionID=msg["transactionID"],challenge=msg["challenge"])
            cur_challenge = challenge.challenge
            kill_threads = False
            cur_tid = int(msg["transactionID"])
            processes = []
            # for i in range(10):
            #     p = multiprocessing.Process(target=brute, args=(challenge,))
            #     processes.append(p)
            #     p.start()
            # for proc in processes:
            #     proc.join()
            # print("xddddd")
            brute(challenge)
            ct=desafios.Challenge(cur_tid,challenge.challenge,clientID=clientID,seed=seed)
            obj = vars(ct).copy()
            obj.__delitem__("challenge")
            print("chegou")
            
    if(message.topic=='ppd/result'):
        if cur_tid == msg["transactionID"]:
            kill_threads = True
            cur_tid = -1
            print("msg")
            pass

client = mqtt.Client("Node_3")
client.connect(mqttBroker)
# client.loop_start()
client.subscribe("ppd/challenge")
client.subscribe("ppd/result")


client.on_message=on_message
client.on_publish = on_publish
# time.sleep(30000)
# client.loop_stop()
client.loop_forever()