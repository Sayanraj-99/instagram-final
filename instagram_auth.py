from instagrapi import Client

class InstagramAuth:
    def __init__(self):
        self.active_clients = {}
    
    def login_account(self, username, password):
        """Authenticate Instagram account"""
        try:
            client = Client()
            client.login(username, password)
            self.active_clients[username] = client
            return client
        except Exception as e:
            print(f"Login failed for {username}: {e}")
            return None
    
    def get_client(self, username):
        """Get active client session"""
        return self.active_clients.get(username)
