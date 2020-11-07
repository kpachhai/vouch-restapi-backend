# Vouch dApp Rest API

To start, clone vouch-restapi-backend repo
```
git clone https://github.com/tuum-tech/vouch-restapi-backend.git;
cd vouch-restapi-backend;
```
# Prerequisites
- Install docker at [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
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

To get all providers:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/providers
```

To get providers for a specific validationType for something like "email":
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/providers/validationType/email
```

To get all services of a provider by its DidId:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/provider/services/did/imxNkhKuuXaefyFKQuzFnkfRdedDVLYmKV
```

To register a provider manually,
```
curl -XPOST  -H "Authorization: vouch-restapi-secret-key" -H "Content-Type: application/json" -H "Accept: application/json" -d @test/newProvider.json http://localhost:8080/v1/providers/create
```

To create a transaction:
```
curl -XPOST  -H "Authorization: vouch-restapi-secret-key" -H "Content-Type: application/json" -H "Accept: application/json" -d @test/emailValidation.json http://localhost:8080/v1/validationtx/create
```

To get all transactions from a DidId:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/did/igZjRKt1HN7toSK3ZPZmNy5NuhfKDhzkUy
```

To get all transactions from a providerId:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/provider_id/5f3ff44d7e80c08c288072dc
```


To get transaction details using confirmationID:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/confirmation_id/5f221ca77d6d25afa44ea4fe
```

To get total transaction count for a specific provider:
```
curl -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/count/provider_id/5f17a02afbe8980577674011
```

To update isSavedOnProfile transaction information:
```
curl -XPOST -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/is_saved/confirmation_id/5f17a02afbe8980577674011
```

To cancel a transaction using confirmationID:
```
curl -XPOST -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/cancel/confirmation_id/5f221ca77d6d25afa44ea4fe
```

To approve a transaction using confirmationID:
```
curl -X POST \
  http://0.0.0.0:8080/v1/validationtx/approve/confirmation_id/5f9089dcd8850661b1f1c3d3 \
  -H 'Authorization: vouch-restapi-secret-key' \
  -H 'Content-Type: application/json' \
  -d '{
        "id": "did:elastos:ifKeiEqaPuMpZKniH4jaHWoL3XobrHiKrm#ifKeiEqaPuMpZKniH4jaHWoL3XobrHiKrm#email",
        "type": [
            "BasicProfileCredential"
        ],
        "issuer": "did:elastos:iddJESh7ymo3xoVEpsC5476NSS8eepBJo8",
        "issuanceDate": "2020-10-29T16:00:43.000Z",
        "expirationDate": "2020-11-02T16:00:43.000Z",
        "credentialSubject": {
            "id": "did:elastos:ifKeiEqaPuMpZKniH4jaHWoL3XobrHiKrm",
            "email": "rong.chen4@elastos.internet"
        },
        "proof": {
            "type": "ECDSAsecp256r1",
            "verificationMethod": "did:elastos:iddJESh7ymo3xoVEpsC5476NSS8eepBJo8#primary",
            "signature": "xlGZqi-nDHVi8wtDU0L06uB8HRt4so-v1VyXLwpsecKhh3MMOM8U95hc-oTa6n_M4xE_r7BJ3mJnjc3WuXTdwg"
        }
    }'
```

To reject a transaction using confirmationID:
```
curl -XPOST -H "Authorization: vouch-restapi-secret-key" http://localhost:8080/v1/validationtx/reject/confirmation_id/5f221ca77d6d25afa44ea4fe
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
 