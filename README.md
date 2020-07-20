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
- [OPTIONAL]: If you want to remove previous mongodb data and start fresh, remove the mongodb directory
```
rm -rf .mongodb-data
```
- Start API server
```
./run.sh start
```

# Verify
- To check whether the API is working:
```
curl http://localhost:8080
```

To get all providers from a validationType:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/providers
```

To create a transaction, execute this example
```
curl -XPOST  -H "Authorization: vouch-restapi-secret-key" -H "Content-Type: application/json" -H "Accept: application/json" -d @test/emailValidation.json http://localhost:8080/v1/validationtx/create
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
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/confirmation_id/5ef3a5440136e7bd17775e23
```

# Deploy to production
- Deploy
```
eb deploy
```

# How to be a validator
- Currently, there is a Redis Broker that each validator will need to connect to and subscribe to different channels. There is a specific channel that each validator will be subscribed to where the user data to be verified are pushed. The job 
of the validator is to listen to these incoming messages, process the request, validate appropriate data, sign the data with their own DID, generate the verifiable credentials and then pass the verified credentials back to another redis channel that 
Vouch REST API is subscribed to. This is how the Vouch REST API and Validators communicate with each other. 
- Check out an example of a DID Email Validator service provided by Tuum Tech at [https://github.com/tuum-tech/did-email-validator](https://github.com/tuum-tech/did-email-validator)
- For testing purposes, you can append to .env file with the following environment variables: PROVIDER2_NAME, PROVIDER2_LOGO_PATH, PROVIDER2_API_KEY, PROVIDER2_VALIDATION_TYPES
- Create your own validator service(written in any programming language - Choice is up to you)
- There are two steps to being a validator for Vouch:
    - Create a validator service that will take certain data(that contains user DID and user data) and then generate a verifiable credential using own's DID
    - Send the verified credentials to a designated channel. Currently, only the following channels are supported:
        - "email-validator-response": For sending verifiable credential that has someone's email address verified
 