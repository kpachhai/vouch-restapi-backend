import redis
import json
from .callbackService import CallbackService

class BrokerService:
    def __init__(self):
        self.__redis = redis.Redis(host = '127.0.0.1', port = 6379)
    
    def __send_message(self, doc, channel):
        print("Send message to broker")
        self.__redis.publish(channel, json.dumps(doc))

    def send_email_validation(self, doc):
        self.__send_message(doc, "email-validator")

    def start_monitors(self):
        callback = CallbackService(self.__redis)
        callback.start_monitor()