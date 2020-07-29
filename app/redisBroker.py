import redis
import sys
import json
import time
import requests
from app import log, config
from app.model import ValidationTx, ValidationStatus, Provider

LOG = log.get_logger()

broker = redis.Redis(host=config.REDIS['HOST'], port=config.REDIS['PORT'], password=config.REDIS['PASSWORD'])


def send_validator_message(doc, apiKey):
    channel = "validator-{}".format(apiKey)
    broker.publish(channel, json.dumps(doc))
    


def monitor_redis():
    LOG.info("Starting response monitor")
    channel = "validator-response"

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

                if doc["action"] == "create":
                   response_create(doc)

                if doc["action"] == "cancel":
                   response_cancel(doc)

                if doc["action"] == "update":
                   response_update(doc)
                

                LOG.info(f'Response processed with success')
            except Exception as e:
                LOG.info(f'Response Error: {e}')
                pass




def response_create(doc):
    provider_rows = Provider.objects(apikey=doc["validatorKey"])
    if not provider_rows:
        raise RuntimeError("ERROR: Invalid Validator Key")

    provider_row = provider_rows[0]

    transaction_rows = ValidationTx.objects(id=doc["transactionId"])
    if not transaction_rows:
        raise RuntimeError("ERROR: Transaction not found")

    transaction_row = transaction_rows[0]

    if transaction_row.provider != str(provider_row.id):
        raise RuntimeError("ERROR: Transaction provider is different than response")

    if transaction_row.status != ValidationStatus.NEW:
        raise RuntimeError("ERROR: Transaction already processed")

    transaction_row.status = ValidationStatus.IN_PROGRESS
    transaction_row.save()

def response_cancel(doc):
    provider_rows = Provider.objects(apikey=doc["validatorKey"])
    if not provider_rows:
        raise RuntimeError("ERROR: Invalid Validator Key")

    provider_row = provider_rows[0]

    transaction_rows = ValidationTx.objects(id=doc["transactionId"])
    if not transaction_rows:
        raise RuntimeError("ERROR: Transaction not found")

    transaction_row = transaction_rows[0]

    if transaction_row.provider != str(provider_row.id):
        raise RuntimeError("ERROR: Transaction provider is different than response")

    if transaction_row.status != ValidationStatus.CANCELATION_IN_PROGRESS:
        raise RuntimeError("ERROR: Transaction not prepared to cancel")

    transaction_row.status = ValidationStatus.CANCELED
    transaction_row.save()

def response_update(doc):
    provider_rows = Provider.objects(apikey=doc["validatorKey"])
    if not provider_rows:
        raise RuntimeError("ERROR: Invalid Validator Key")

    provider_row = provider_rows[0]

    transaction_rows = ValidationTx.objects(id=doc["transactionId"])
    if not transaction_rows:
        raise RuntimeError("ERROR: Transaction not found")

    transaction_row = transaction_rows[0]

    if transaction_row.status != ValidationStatus.IN_PROGRESS:
        raise RuntimeError("ERROR: Transaction already processed")

    if transaction_row.provider != str(provider_row.id):
        raise RuntimeError("ERROR: Transaction provider is different than response")

    if doc["response"] != ValidationStatus.APPROVED and doc["response"] != ValidationStatus.REJECTED:
        raise RuntimeError("ERROR: Response status invalid")

    transaction_row.status = doc["response"]
    transaction_row.reason = doc["reason"]
    transaction_row.verifiedCredential = doc["verifiableCredential"]

    transaction_row.save()
