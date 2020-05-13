import json
from .mongoDatabase import MongoDatabase
class GetListProviders:
    def on_get(self, req, resp):
        """Handles Get requests"""
        validationType = req.get_param('validationType', True)
        db = MongoDatabase()
        response = db.get_providers_from_validationType(validationType)
        resp.media = response