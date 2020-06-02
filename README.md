# Vouch dApp Rest API

To start, clone vouch-restapi-backend repo
```
git clone https://github.com/tuum-tech/vouch-restapi-backend.git;
cd vouch-restapi-backend;
```
# Prerequisites
- Install required packages[Only needs to be done once]
```
./install.sh
```

# Run the service

- Start API server
```
./run.sh start
```

# Verify

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



