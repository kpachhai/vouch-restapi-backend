import redis
import json
import time
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
                handle_response(doc)
                LOG.info(f'Response processed with success')
            except Exception as e:
                LOG.info(f'Response Error: {e}')
                pass


def handle_response(doc):
    tx_type = doc["action"]
    if tx_type not in ["create", "cancel", "update"]:
        LOG.info(f'Transaction type "{tx_type}" passed is not valid')
        return
    provider_rows = Provider.objects(apikey=doc["validatorKey"])
    if not provider_rows:
        LOG.info(f'Validator key "{doc["validatorKey"]} is invalid')
        return

    provider_row = provider_rows[0]

    transaction_rows = ValidationTx.objects(id=doc["transactionId"])
    if not transaction_rows:
        LOG.info(f'Transaction ID "{doc["transactionId"]} not found')
        return

    transaction_row = transaction_rows[0]

    if transaction_row.provider != str(provider_row.id):
        LOG.info(f'Provider "{provider_row.name} cannot perform this action')
        return

    if tx_type == "create":
        if transaction_row.status != ValidationStatus.NEW:
            LOG.info(f'Transaction ID "{str(transaction_row.id)}" is already being processed')
            return
        transaction_row.status = ValidationStatus.IN_PROGRESS
    elif tx_type == "cancel":
        if transaction_row.status != ValidationStatus.CANCELATION_IN_PROGRESS:
            LOG.info(f'Transaction ID "{str(transaction_row.id)}" cannot be cancelled because no '
                     f'cancellation is in progress for this request')
            return
        transaction_row.status = ValidationStatus.CANCELED
    elif tx_type == "update":
        if transaction_row.status != ValidationStatus.IN_PROGRESS:
            LOG.info(f'Transaction ID "{str(transaction_row.id)}" is already being processed')
            return
        if doc["response"] != ValidationStatus.APPROVED and doc["response"] != ValidationStatus.REJECTED:
            LOG.info(f'Response status "{doc["response"]}" is invalid')
            return
        transaction_row.status = doc["response"]
        transaction_row.reason = doc["reason"]
        transaction_row.verifiedCredential = doc["verifiableCredential"]
    transaction_row.save()

