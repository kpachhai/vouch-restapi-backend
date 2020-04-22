class DisplayTest:
    def on_get(self, req, resp):
        """Handles Get requests"""
        didId = req.get_param('didid', True)
        email = req.get_param('email', True)
        resp.media = "Getting {} and {}".format(didId, email)