import falcon
import threading
from falcon_cors import CORS
from app import log, config, redisBroker, seedDatabase
from app.middleware import AuthMiddleware
from app.api.common import base
from app.api.v1 import providers, validationtx
from app.model import provider
from app.errors import AppError
from mongoengine import connect

LOG = log.get_logger()


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info("API Server is starting")

        # Simple endpoint for base
        self.add_route("/", base.BaseResource())
        
        #Retrieves all providers
        self.add_route("/v1/providers", providers.ProvidersCollection())

        #Retrieves providers from validation type
        self.add_route("/v1/providers/validationType/{validationType}", providers.ProvidersFromValidationTypeCollection())

        #Retrieves all transactions according to did
        self.add_route("/v1/validationtx/did/{did}", validationtx.ValidationsFromDid())

        # Retrieves transaction according to confirmation ID
        self.add_route("/v1/validationtx/confirmation_id/{confirmation_id}", validationtx.ValidationFromId())
        
        # Creates a new transaction
        self.add_route("/v1/validationtx/create", validationtx.CreateValidation())

        self.add_error_handler(AppError, AppError.handle)


connect(
    config.MONGO['DATABASE'],
    host="mongodb://" + config.MONGO['USERNAME'] + ":" + config.MONGO['PASSWORD'] + "@" +
         config.MONGO['HOST'] + ":" + str(config.MONGO['PORT']) + "/?authSource=admin"
)



# cors = CORS(
#     allow_all_origins=True,
#     allow_all_headers=True,
#     allow_all_methods=True)
LOG.info("Initializing the Falcon REST API service...")
application = App(middleware=[
    #cors.middleware,
    AuthMiddleware(),
])

seedDatabase.seed_database()

th = threading.Thread(target=redisBroker.monitor_redis)
th.setDaemon(True)
th.start()