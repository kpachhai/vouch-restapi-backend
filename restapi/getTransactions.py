import json
from .mongoDatabase import MongoDatabase
class GetTransactions:
    def on_get(self, req, resp):
        """Handles Get requests"""
        didId = req.get_param('didid', True)
        db = MongoDatabase()
        response = db.get_transactions_from_didid(didId)
        resp.media = response