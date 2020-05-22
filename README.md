# Vouch Rest API

To start, clone vouch-restapi-backend repo
```
git clone https://github.com/tuum-tech/vouch-restapi-backend.git;
cd vouch-restapi-backend;
```
# Prerequisites
- Python3 is needed
```
brew install python3 // On Mac
sudo apt-get install python3 // On linux
```
- Virtualenv
```
pip3 install virtualenv
```

# Setup
Before you start, you have to initiate vouch-redis-broker https://github.com/tuum-tech/vouch-redis-broker
- Create a python virtual environment
```
virtualenv -p `which python3` venv
```
- Activate the virtualenv environment
```
source venv/bin/activate
```
- Install the dependencies
```
pip install -r requirements.txt
```
- Run mongodb
```
cd tools
./mongodb.sh
```

# Run
- Start API server
```
waitress-serve --port=8080 restapi:api // On Windows
gunicorn restapi:api --bind='0.0.0.0:8080' // On mac/linux
```

# Verify
- To get all providers from a validationType, run the following:
```
curl http://localhost:8080/providers?validationType=email
```
- To create a transaction, run the following:
```
curl -H 'Content-Type: application/json' -H 'Accept:application/json' --data '{\"validationType\":\"email\", \"providerId\":\"USE A VALID ID FROM A PROVIDER IN THE COLLECTION\" \"params\":{\"didId\":\"did:elastos:1234567890\",\"email\":\"test@test.com\"}}' http://localhost:8080/start
```
- To get all transactions from a DidId, run the following:
```
curl "http://localhost:8080/get?didid=did:elastos:1234567890"
```



