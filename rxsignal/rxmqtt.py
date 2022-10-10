import threading
from paho.mqtt import client as mqtt_client
import reactivex
import reactivex.subject
import time
from .observable import Subject


class mqtt_rxclient:
    def __init__(self, ip='127.0.0.1', port=1883, client_id=None):
        self.ip = ip
        self.port = port
        self.client_id = client_id
        self.client = self.connect_mqtt(ip, port)
        self.client.on_message = self.on_message
        self.handlers = {}
        if client_id is None:
            client_id = f'client_{time.time()}'

    def start_spin(self):
        thr = threading.Thread(target=self.client.loop_forever)
        thr.start()
        self.loop_thread = thr

    def connect_mqtt(self, ip, port):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.ip, self.port)
        return client

    def on_message(self, client, userdata, msg):
        for handler in self.handlers[msg.topic]:
            handler(msg.payload.decode())

    def subscribe(self, topic, func):
        self.client.subscribe(topic)
        if topic in self.handlers:
            self.handlers[topic].append(func)
        else:
            self.handlers[topic] = [func]

    def publish(self, theme, msg):
        self.client.publish(theme, msg)

    def rxsubscribe(self, theme):
        # it must be a PublishSubject. But library does not have it.
        s = reactivex.subject.Subject()
        self.subscribe(theme, lambda x: s.on_next(x))
        return Subject(s)

    def rxpublish(self, theme, collection):
        collection.subscribe(lambda x: self.client.publish(theme, x))

    # def rxpublish(theme, observable):
    #    observable.subscribe(lambda x: publish(theme, x))
