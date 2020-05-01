import falcon
import requests
import json
from .mongoDatabase import MongoDatabase
class Callback:
    def on_post(self, req, resp):
       print("Transaction Callback")
       try:
        body = req.stream.read()
        doc = json.loads(body.decode('utf-8'))
        db = MongoDatabase()
        db.update_transaction(doc["transactionId"], doc["response"], doc["verifiedCredential"])
       except AttributeError:
            raise falcon.HTTPBadRequest(
                'Invalid post',
                'Payload must be submitted in the request body.')


       resp.status = falcon.HTTP_201
       resp.location = '/%s/callback'
       resp.media = "OK"