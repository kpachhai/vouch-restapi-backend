# Vouch dApp Rest API

To start, clone vouch-restapi-backend repo
```
git clone https://github.com/tuum-tech/vouch-restapi-backend.git;
cd vouch-restapi-backend;
```
# Prerequisites

Before start, you have to initiate vouch-redis-broker https://github.com/tuum-tech/vouch-redis-broker


1. Install Falcon API 
```
pip install falcon 
```
2. Install Gunicorn (Only on Mac or Linuc)
```
pip install gunicorn
```
3. Install Waitress (Only on Windows)
```
pip install waitress
```
4. Install PyMongo
```
pip install pymongo
```
5. Create Database instance
```
cd tools
.\mongodb.sh
```

# Run the service

On Windows
```
waitress-serve --port=8080 restapi:api
```

On Mac or Linux
```
gunicorn restapi:api
```

To create a transaction, execute this exemple
```
curl -H 'Content-Type: application/json' -H 'Accept:application/json' --data '{\"validationType\":\"email\",\"params\":{\"didId\":\"did:elastos:1234567890\",\"email\":\"test@test.com\"}}' http://localhost:8080/start
```

To get all transactions from a DidId, execute this exemple
```
curl "http://localhost:8080/get?didid=did:elastos:1234567890"
```

To get all providers from a validationType, execute this exemple
```
curl "http://localhost:8080/providers?validationType=email"
```

