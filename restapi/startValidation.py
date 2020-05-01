import falcon
import requests
import json
import uuid
from .brokerService import BrokerService
from .mongoDatabase import MongoDatabase

class StartValidation:
    def __init__(self, brokerService: BrokerService):
       self.brokerService = brokerService
    def on_post(self, req, resp):
       print("Start a transaction")
       try:
        body = req.stream.read()
        doc = json.loads(body)
        params = doc["params"]
        db = MongoDatabase()
        transaction = db.create_transaction(params)
        resp.media = transaction
        if doc["validationType"] == "email":
            self.brokerService.send_email_validation({'transactionId': '{}'.format(transaction["_id"]), 'email': params["email"]})
       except AttributeError:
            raise falcon.HTTPBadRequest(
                'Invalid post',
                'Payload must be submitted in the request body.')


       resp.status = falcon.HTTP_201
       resp.location = '/%s/start'
       