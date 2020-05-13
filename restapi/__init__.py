import falcon
from .startValidation  import StartValidation
from .brokerService    import BrokerService
from .getTransactions  import GetTransactions
from .getListProviders import GetListProviders
from .callback         import Callback
from .mongoDatabase    import MongoDatabase

api = application = falcon.API()
brokerService = BrokerService()

database = MongoDatabase()
database.db_init()

api.add_route('/start', StartValidation(brokerService))
api.add_route('/callback', Callback())
api.add_route('/get', GetTransactions())
api.add_route('/providers', GetListProviders())



#brokerService.start_monitors()