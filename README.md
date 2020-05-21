# Vouch dApp Rest API

To start, clone vouch-restapi-backend repo
```
git clone https://github.com/tuum-tech/vouch-restapi-backend.git;
cd vouch-restapi-backend;
```
# Prerequisites

Before start, you have to initiate vouch-redis-broker https://github.com/tuum-tech/vouch-redis-broker

0. Install Wheel (If required because of an error using Step#1 'Could not build wheels for falcon, since package 'wheel' is not installed.')
```
pip install wheel 
```

1. Install Falcon API 
```
pip install falcon
pip install falcon-cors
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
gunicorn restapi:api --bind='192.168.0.104:8080' (Whitelisted Host in Vouch Capsule App)
gunicorn restapi:api --bind='localhost:8080'
```

To get all providers from a validationType, execute this exemple
```
curl "http://localhost:8080/providers?validationType=email"
```

To create a transaction, execute this example
```
curl -H 'Content-Type: application/json' -H 'Accept:application/json' --data '{\"validationType\":\"email\", \"providerId\":\"USE A VALID ID FROM A PROVIDER IN THE COLLECTION\" \"params\":{\"didId\":\"did:elastos:1234567890\",\"email\":\"test@test.com\"}}' http://localhost:8080/start
```

To get all transactions from a DidId, execute this exemple
```
curl "http://localhost:8080/get?didid=did:elastos:1234567890"
```



