import os
import time
import random
import logging
from instagrapi import Client
from instagrapi.exceptions import VideoNotUploaded, LoginRequired, ClientError
from telegram import Bot
from telegram.error import TelegramError
import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstagramUploader:
    def __init__(self):
        self.bot = Bot(token=os.getenv('BOT_TOKEN'))
        self.download_dir = os.getenv('DOWNLOAD_DIR', 'downloads')
        os.makedirs(self.download_dir, exist_ok=True)
    
    def _load_proxies(self):
        """Load all active proxies from database"""
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("SELECT address FROM proxies WHERE status='active'")
        proxies = [row[0] for row in c.fetchall()]
        conn.close()
        return proxies
    
    def _download_telegram_file(self, file_id):
        """Download file from Telegram to local storage with retry logic"""
        file_path = os.path.join(self.download_dir, f"{file_id}.mp4")
        
        for attempt in range(3):
            try:
                file = self.bot.get_file(file_id)
                file.download(custom_path=file_path)
                logger.info(f"Downloaded file {file_id} successfully")
                return file_path
            except TelegramError as e:
                logger.warning(f"Download attempt {attempt+1} failed: {e}")
                time.sleep(2)
        
        logger.error(f"All download attempts failed for {file_id}")
        return None
    
    def _instagram_login(self, username, password, proxy=None):
        """Authenticate with Instagram using instagrapi"""
        client = Client()
        if proxy:
            try:
                client.set_proxy(proxy)
            except Exception as e:
                logger.error(f"Invalid proxy format {proxy}: {e}")
                return None
        
        try:
            client.login(username, password)
            return client
        except (LoginRequired, ClientError) as e:
            logger.error(f"Login failed for {username}: {e}")
            return None
    
    def _update_account_stats(self, username, views):
        """Increment post count and views for account"""
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("""
            UPDATE accounts 
            SET posts_count = posts_count + 1, 
                total_views = total_views + ? 
            WHERE username = ?
        """, (views, username))
        conn.commit()
        conn.close()
    
    def _record_analytics(self, username, post_id, views):
        """Save post performance data"""
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM accounts WHERE username = ?", (username,))
        row = c.fetchone()
        if not row:
            conn.close()
            return
        account_id = row[0]
        c.execute("""
            INSERT INTO analytics (account_id, post_id, views, timestamp)
            VALUES (?, ?, ?, ?)
        """, (account_id, post_id, views, int(time.time())))
        conn.commit()
        conn.close()
    
    def _mark_proxy_banned(self, proxy):
        """Flag proxy as banned"""
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("UPDATE proxies SET status='banned' WHERE address=?", (proxy,))
        conn.commit()
        conn.close()
    
    def _mark_account_suspended(self, username):
        """Flag account as suspended"""
        conn = database.get_connection()
        c = conn.cursor()
        c.execute("UPDATE accounts SET status='suspended' WHERE username=?", (username,))
        conn.commit()
        conn.close()
    
    def upload_video(self, username, password, file_id, caption):
        """Main upload method with proxy retry mechanism"""
        file_path = self._download_telegram_file(file_id)
        if not file_path:
            return False
        
       proxies = self._load_proxies()

# allow upload without proxy if none exist
if not proxies:
    proxies = [None]

random.shuffle(proxies)
            logger.info(f"Trying proxy: {proxy}")
            client = self._instagram_login(username, password, proxy)
            
            if not client:
                self._mark_proxy_banned(proxy)
                continue  # Try next proxy
            
            try:
                media = client.video_upload(file_path, caption=caption)
                views = getattr(media, 'view_count', 0)
                
                self._update_account_stats(username, views)
                self._record_analytics(username, media.id, views)
                
                logger.info(f"Uploaded {file_id} to {username}'s Instagram using proxy {proxy}")
                
                # Cleanup
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                client.logout()
                return True
                
            except VideoNotUploaded:
                logger.error(f"Upload failed for {username} with proxy {proxy}")
                self._mark_proxy_banned(proxy)
                continue  # Try next proxy
                
            except (ClientError, LoginRequired) as e:
                logger.error(f"Account error for {username} with proxy {proxy}: {e}")
                self._mark_proxy_banned(proxy)
                self._mark_account_suspended(username)
                break  # Stop trying proxies for this account
                
            except Exception as e:
                logger.error(f"Unexpected error with proxy {proxy}: {e}")
                self._mark_proxy_banned(proxy)
                continue  # Try next proxy
        
        # Cleanup if all proxies failed
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        return False
