
class Server:
    def __init__(self):
        self.server_data = []

    def get_data(self):
        return self.server_data

    def upload_data(self, payload):
        self.server_data = payload
