import time
import database
from instagram_uploader import InstagramUploader

class Scheduler:
    def __init__(self):
        self.uploader = InstagramUploader()
    
    def run(self):
        while True:
            conn = database.get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM queue WHERE status='pending' LIMIT 1")
            video = c.fetchone()
            
            if video:
                # Get account
                c.execute("SELECT * FROM accounts LIMIT 1")
                account = c.fetchone()
                
                if account:
                    success = self.uploader.upload_video(
                        account[1], account[2], video[1], video[2]
                    )
                    
                    if success:
                        c.execute("DELETE FROM queue WHERE id=?", (video[0],))
                        conn.commit()
            
            conn.close()
            time.sleep(60)
