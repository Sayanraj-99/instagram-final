import os
import time
from instagrapi import Client
from instagrapi.exceptions import VideoNotUploaded
from telegram import Bot
from config import BOT_TOKEN
from instagram_auth import InstagramAuth
import database

class InstagramUploader:
    def __init__(self):
        self.auth = InstagramAuth()
        self.bot = Bot(token=BOT_TOKEN)
    
    def upload_video(self, username, password, file_id, caption):
        """Upload video to Instagram"""
        # Download from Telegram
        file_path = f"downloads/{file_id}"
        try:
            file = self.bot.get_file(file_id)
            file.download(file_path)
        except:
            return False
        
        # Authenticate and upload
        client = self.auth.login_account(username, password)
        if not client:
            return False
        
        try:
            media = client.video_upload(file_path, caption=caption)
            
            # Update account stats
            conn = database.get_connection()
            c = conn.cursor()
            c.execute("""
                UPDATE accounts 
                SET posts_count = posts_count + 1,
                    total_views = total_views + ?
                WHERE username = ?
            """, (media.view_count if hasattr(media, 'view_count') else 0, username))
            conn.commit()
            conn.close()
            
            # Save analytics
            self._save_analytics(username, media.id, media.view_count)
            
            # Cleanup
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return True
            
        except VideoNotUploaded:
            return False
        except Exception as e:
            print(f"Upload error: {e}")
            return False
    
    def _save_analytics(self, username, post_id, views):
        """Save post analytics"""
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM accounts WHERE username = ?", (username,))
        account_id = c.fetchone()[0]
        
        c.execute("""
            INSERT INTO analytics(account_id, post_id, views)
            VALUES(?, ?, ?)
        """, (account_id, post_id, views))
        conn.commit()
        conn.close()
