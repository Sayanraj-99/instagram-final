import database
from instagrapi import Client

class InstagramManager:
    def add_account(self, username, password):
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO accounts(username, password) VALUES(?,?)", 
                 (username, password))
        conn.commit()
        conn.close()
    
    def delete_post(self, username, password, post_id):
        client = Client()
        client.login(username, password)
        client.media_delete(post_id)
    
    def get_stats(self, account_id):
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("SELECT SUM(views) FROM analytics WHERE account_id=?", (account_id,))
        total_views = c.fetchone()[0] or 0
        conn.close()
        return {'total_views': total_views}
