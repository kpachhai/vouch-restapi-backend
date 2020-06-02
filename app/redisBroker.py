import redis
import json
from app import config

broker =  redis.Redis(host = config.REDIS['host'], port = config.REDIS['port'])

def send_email_validation(doc, apiKey):
    channel = "email-validator-{}".format(apiKey)
    broker.publish(channel, json.dumps(doc))

   

    

    