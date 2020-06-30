import redis
import sys
import json
import time
import requests
from app import log, config
from app.model import ValidationTx, ValidationStatus, Provider

LOG = log.get_logger()

broker =  redis.Redis(host = config.REDIS['HOST'], port = config.REDIS['PORT'])


def send_email_validation(doc, apiKey):
    channel = "email-validator-{}".format(apiKey)
    broker.publish(channel, json.dumps(doc))

   
def monitor_redis():
    LOG.info("Starting response monitor")
    channel =  "email-validator-response"

    
    p = broker.pubsub()
    p.subscribe(channel)

    LOG.info("Response monitor started")

    while True:
        time.sleep(1)
        message = p.get_message()

        if message and not message['data'] == 1:
            try:
                message = message['data'].decode('utf-8')
                doc = json.loads(message)
                LOG.info(f'Response Received message: {message}')

                provider_rows = Provider.objects(apikey=doc["validatorKey"])
                if not provider_rows:
                   raise RuntimeError("ERROR: Invalid Validator Key")

                provider_row = provider_rows[0]

                transaction_rows = ValidationTx.objects(id=doc["transactionId"])
                if not transaction_rows:
                   raise RuntimeError("ERROR: Transaction not found")

                transaction_row = transaction_rows[0]

                if transaction_row.status != ValidationStatus.PENDING:
                   raise RuntimeError("ERROR: Transaction already processed") 

                if transaction_row.provider != str(provider_row.id):
                   raise RuntimeError("ERROR: Transaction provider is different than response") 

                if doc["response"] != ValidationStatus.SUCCEDED and doc["response"] != ValidationStatus.FAILED:
                   raise RuntimeError("ERROR: Response status invalid")


                transaction_row.status = doc["response"]
                transaction_row.reason = doc["reason"]
                transaction_row.verifiedCredential = doc["verifiableCredential"]

                transaction_row.save()
                
                LOG.info(f'Response processed with success')
            except Exception as e:
                LOG.info(f'Response Error: {e}')
                pass
    

    