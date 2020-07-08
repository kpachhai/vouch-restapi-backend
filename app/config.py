from decouple import config

BRAND_NAME = "Vouch REST API"

PRODUCTION = config('PRODUCTION', default=False, cast=bool)

LOG_LEVEL = "DEBUG"

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