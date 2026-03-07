import time
import threading
import database
from instagram_uploader import InstagramUploader

class AutoScheduler:
    def __init__(self):
        self.uploader = InstagramUploader()
        self.running = False
    
    def start(self):
        """Start automatic scheduler"""
        self.running = True
        thread = threading.Thread(target=self._run)
        thread.start()
    
    def _run(self):
        """Main scheduling loop"""
        while self.running:
            conn = database.get_connection()
            c = conn.cursor()
            
            # Get next video from queue
            c.execute("SELECT * FROM queue WHERE status='pending' LIMIT 1")
            video = c.fetchone()
            
            if video:
                # Get first available account
                c.execute("SELECT * FROM accounts WHERE status='active' LIMIT 1")
                account = c.fetchone()
                
                if account:
                    success = self.uploader.upload_video(
                        account[1], account[2], video[1], video[2]
                    )
                    
                    if success:
                        c.execute("DELETE FROM queue WHERE id=?", (video[0],))
                        conn.commit()
            
            conn.close()
            time.sleep(60)  # Check every minute
    
    def stop(self):
        """Stop scheduler"""
        self.running = False
