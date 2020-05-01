import redis, json
from .mongoDatabase import MongoDatabase
class CallbackService:
    def __init__(self, client: redis.Redis):
       self.__client = client
    def start_monitor(self):
       p = self.__client.pubsub()
       p.subscribe("email-validator-response")

       while True:
            message = p.get_message()
            if message and not message['data'] == 1:
                print(f'Email-Validator-Response Received')
                doc = json.loads(message['data'].decode('utf-8'))
                db = MongoDatabase()
                db.update_transaction(doc["transactionId"], doc["response"], doc["verifiedCredential"])
                