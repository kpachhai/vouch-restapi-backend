import base64
import os
import json

from decouple import config

from app.service import DidRetrieval

BRAND_NAME = "Vouch REST API"

PRODUCTION = config('PRODUCTION', default=False, cast=bool)

LOG_LEVEL = "DEBUG"

CRON_INTERVAL = config('CRON_INTERVAL', default=60, cast=int)

TRANSACTION_RETRIES = config('TRANSACTION_RETRIES', default=5, cast=int)

DEBUG = True

SECRET_KEY = config('SECRET_KEY', default='vouch-restapi-secret-key', cast=str)

DID_SIDECHAIN_RPC_URL = config('DID_SIDECHAIN_RPC_URL', default='http://api.elastos.io:20606', cast=str)

MONGO = {
    "DATABASE": config('MONGO_DATABASE', default='vouchdb', cast=str),
    "HOST": config('MONGO_HOST', default='localhost', cast=str),
    "PORT": config('MONGO_PORT', default=27018, cast=int),
    "USERNAME": config('MONGO_USERNAME', default='mongoadmin', cast=str),
    "PASSWORD": config('MONGO_PASSWORD', default='vouchmongo', cast=str)
}

REDIS = {
    "HOST": config('REDIS_HOST', default='localhost', cast=str),
    "PORT": config('REDIS_PORT', default=6379, cast=int),
    "PASSWORD": config('REDIS_PASSWORD', default="", cast=str)
}


def get_providers():
    config_path = os.path.dirname(os.path.abspath(__file__)).split("/")
    config_path = "/".join(config_path[:-1]) + "/validator-config/"
    provider_files = [file_name for file_name in os.listdir(config_path) if file_name.endswith('.json')]
    providers = []
    for provider_file in provider_files:
        with open(config_path + provider_file, "rb") as f:
            provider = json.load(f)
            did = provider["did"].replace("did:elastos:", "").split("#")[0]
            name = provider["name"]
            validation = provider["validation"]
            logo = None
            did_retrieval = DidRetrieval(did)
            document = did_retrieval.get_current_did_document()
            if document:
                verifiable_creds = document["verifiable_creds"]
                for cred in verifiable_creds:
                    cred_subject = cred["subject"]
                    if "avatar" in cred_subject.keys():
                        logo = "data:" + cred_subject["avatar"]["content-type"] + ";base64," + cred_subject["avatar"]["data"]
            if not logo:
                logo_path = config_path + "default.png"
                with open(logo_path, "rb") as image_file:
                    logo = f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
            provider = {
                "did": did,
                "name": name,
                "logo": logo,
                "validation": validation
            }
            providers.append(provider)
    return providers


# Retrieve provider details
PROVIDERS = get_providers()
