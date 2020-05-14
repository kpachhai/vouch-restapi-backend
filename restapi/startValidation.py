import falcon
import requests
import json
import uuid
import sys
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

        provider = db.get_provider_from_id(doc["providerId"])

        
        transaction = db.create_transaction(doc["validationType"], doc["providerId"], params)
        resp.media = transaction
        if doc["validationType"] == "email":
            self.brokerService.send_email_validation({'transactionId': '{}'.format(transaction["_id"]), 'email': params["email"]}, provider["apiKey"])
       except AttributeError:
            print(sys.exc_info()[1])
            raise falcon.HTTPBadRequest(
                'Invalid post',
                'Payload must be submitted in the request body.')


       resp.status = falcon.HTTP_201
       resp.location = '/%s/start'
       