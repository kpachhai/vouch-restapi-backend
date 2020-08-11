import base64

from decouple import config

BRAND_NAME = "Vouch REST API"

PRODUCTION = config('PRODUCTION', default=False, cast=bool)

LOG_LEVEL = "DEBUG"

CRON_INTERVAL = config('CRON_INTERVAL', default=60, cast=int)

TRANSACTION_RETRIES = config('TRANSACTION_RETRIES', default=5, cast=int)

DEBUG = True

SECRET_KEY = config('SECRET_KEY', default='vouch-restapi-secret-key', cast=str)

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
    providers = []
    i = 1
    while True:
        name = config(f"PROVIDER{i}_NAME", default=None)
        logo_path = config(f"PROVIDER{i}_LOGO_PATH", default=None)
        api_key = config(f"PROVIDER{i}_API_KEY", default=None)
        validation_types = config(f"PROVIDER{i}_VALIDATION_TYPES", default=None)
        if not (name and logo_path and api_key and validation_types):
            break
        else:
            logo = ""
            with open(logo_path, "rb") as image_file:
                logo = f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
            validation_types = validation_types.replace(" ", "").split(",")
            provider = {
                "name": name,
                "logo": logo,
                "api_key": api_key,
                "validation_types": validation_types
            }
            providers.append(provider)
        i += 1
    return providers


# Retrieve provider details
PROVIDERS = get_providers()
