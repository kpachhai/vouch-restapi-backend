from decouple import config

BRAND_NAME = "Vouch REST API"

LOG_LEVEL = "DEBUG"

DEBUG = True

SECRET_KEY = config('SECRET_KEY')

MONGO = {
    "DATABASE": config('MONGO_DATABASE'),
    "HOST": config('MONGO_HOST'),
    "PORT": config('MONGO_PORT'),
    "USERNAME": config('MONGO_USERNAME'),
    "PASSWORD": config('MONGO_PASSWORD')
}

REDIS = {
    "HOST": config('REDIS_HOST'),
    "PORT": config('REDIS_PORT')
}
