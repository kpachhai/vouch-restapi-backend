# Vouch dApp Rest API

To start, clone vouch-restapi-backend repo
```
git clone https://github.com/tuum-tech/vouch-restapi-backend.git;
cd vouch-restapi-backend;
```
# Prerequisites

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

# Run the service

On Windows
```
waitress-serve --port=8000 restapi:api
```

On Mac or Linux
```
gunicorn restapi:api
```

To test, execute this exemple
```
curl "http://localhost:8000/display?didid=didexemple&email=youremail"
```

