from instagrapi import Client

class InstagramAuth:
    def login(self, username, password):
        client = Client()
        try:
            client.login(username, password)
            return client
        except:
            return None
