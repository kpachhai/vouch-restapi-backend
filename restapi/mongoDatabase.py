import pymongo, uuid, json
from datetime import datetime, timedelta

class TransactionStatus(object):
      PENDING = "Pending"
      WAITING_RESPONSE = "Waiting response"
      SUCCEDED = "Succeded"
      FAILED = "Failed"



class MongoDatabase:
   
   def __init__(self):
      self.__client = pymongo.MongoClient("mongodb://mongoadmin:vouchmongo@localhost:27018/")
      self.__db = self.__client["vouchdb"]
      self.__TRANSACTIONS_COLLECTION = "Transactions"

   def create_transaction(self, params):
      collection = self.__db[self.__TRANSACTIONS_COLLECTION]
      transactionId = uuid.uuid4().hex
      transaction = {"_id": transactionId, "didid": params["didId"], "params": params, "createdIn": str( datetime.utcnow() ), "status": TransactionStatus.PENDING, "lastUpdate": None, "verifiedCredential": None  }
      collection.insert(transaction)
      return transaction
   
   def get_transaction(self, transactionId):
      collection = self.__db[self.__TRANSACTIONS_COLLECTION]
      query = {"_id": transactionId}
      response = collection.find(query)
      return response

   def get_transactions_from_didid(self, didId):
      collection = self.__db[self.__TRANSACTIONS_COLLECTION]
      query = {"didid": didId}
      found = collection.find(query)
      response = []; 
      for item in found:
          response.append(json.loads(json.dumps(item)))
      return response

   def update_transaction(self, transactionId, status, verifiedCredential):
      collection = self.__db[self.__TRANSACTIONS_COLLECTION]
      query = {"_id": transactionId}
      updatedValues = { "$set": { "status": status, "lastUpdate": str( datetime.utcnow()), "verifiedCredential": verifiedCredential } }
      collection.update_one(query, updatedValues)



   
