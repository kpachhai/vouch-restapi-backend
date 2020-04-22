import falcon
from .displayTest   import DisplayTest

api = application = falcon.API()

api.add_route('/display', DisplayTest())
