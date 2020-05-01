import falcon
from .startValidation import StartValidation
from .brokerService   import BrokerService
from .getTransactions import GetTransactions
from .callback        import Callback

api = application = falcon.API()
brokerService = BrokerService()

api.add_route('/start', StartValidation(brokerService))
api.add_route('/callback', Callback())
api.add_route('/get', GetTransactions())

#brokerService.start_monitors()