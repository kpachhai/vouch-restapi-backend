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
- Copy example environment file
```
cp .env.example .env
```
- Modify .env file with your own values
- Start API server
```
./run.sh start
```

# Verify
- To check whether the API is working:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080
```

To get all providers from a validationType:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/providers
```

To create a transaction, execute this example
```
curl -X POST -H "Authorization: vouch-restapi-secret-key" -H "Content-Type: application/json" -H "Accept: application/json" -d @test/emailValidation.json http://localhost:8080/v1/validationtx/create
```

To get all transactions from a DidId, execute this exemple
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/did/iouMSXKHNcwdbPzb58pXpmGBDBxrMzfq2c
```

To get transaction details using confirmationID, execute this example
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/confirmation_id/5ef3a5440136e7bd17775e23
```

To update isSavedOnProfile transaction information, execute this example
```
curl -X POST "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/is_saved/confirmation_id/5ef3a5440136e7bd17775e23
```



