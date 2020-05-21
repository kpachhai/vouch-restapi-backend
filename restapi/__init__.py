import falcon
from .startValidation import StartValidation
from .brokerService   import BrokerService
from .getTransactions import GetTransactions
from .callback        import Callback

from falcon_cors import CORS

cors = CORS(
    allow_all_origins=True,
    allow_all_headers=True,
    allow_all_methods=True,
)

api = application = falcon.API(middleware=[cors.middleware])
# api = application = falcon.API()
brokerService = BrokerService()

api.add_route('/start', StartValidation(brokerService))
api.add_route('/callback', Callback())
api.add_route('/get', GetTransactions())

#brokerService.start_monitors()