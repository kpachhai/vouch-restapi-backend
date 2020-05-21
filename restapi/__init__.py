import falcon
from .startValidation  import StartValidation
from .brokerService    import BrokerService
from .getTransactions  import GetTransactions
from .getListProviders import GetListProviders
from .callback         import Callback
from .mongoDatabase    import MongoDatabase

from falcon_cors import CORS

cors = CORS(
    allow_all_origins=True,
    allow_all_headers=True,
    allow_all_methods=True,
)

api = application = falcon.API(middleware=[cors.middleware])
# api = application = falcon.API()
brokerService = BrokerService()

database = MongoDatabase()
database.db_init()

api.add_route('/start', StartValidation(brokerService))
api.add_route('/callback', Callback())
api.add_route('/get', GetTransactions())
api.add_route('/providers', GetListProviders())



#brokerService.start_monitors()