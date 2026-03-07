import os
from instagrapi import Client
from telegram import Bot
from config import BOT_TOKEN
from instagram_auth import InstagramAuth

class InstagramUploader:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.auth = InstagramAuth()
    
    def upload_video(self, username, password, file_id, caption):
        # Download from Telegram
        file_path = f"downloads/{file_id}"
        file = self.bot.get_file(file_id)
        file.download(file_path)
        
        # Upload to Instagram
        client = self.auth.login(username, password)
        if not client:
            return False
        
        try:
            media = client.video_upload(file_path, caption=caption)
            
            # Cleanup
            if os.path.exists(file_path):
                os.remove(file_path)
                
            return True
        except:
            return False
