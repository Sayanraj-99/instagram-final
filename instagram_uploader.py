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
        self.bot = Bot(token=os.getenv("BOT_TOKEN"))
        self.download_dir = os.getenv("DOWNLOAD_DIR", "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

    def _load_proxies(self):
        conn = database.get_connection()
        c = conn.cursor()

        c.execute("SELECT address FROM proxies WHERE status='active'")
        proxies = [row[0] for row in c.fetchall()]

        conn.close()
        return proxies

    def _download_telegram_file(self, file_id):

        file_path = os.path.join(self.download_dir, f"{file_id}.mp4")

        for attempt in range(3):
            try:
                file = self.bot.get_file(file_id)
                file.download(custom_path=file_path)
                logger.info(f"Downloaded {file_id}")
                return file_path

            except TelegramError as e:
                logger.warning(f"Download failed attempt {attempt+1}: {e}")
                time.sleep(2)

        return None

    def _instagram_login(self, username, password, proxy=None):

        client = Client()

        if proxy:
            try:
                client.set_proxy(proxy)
            except Exception:
                pass

        try:
            client.login(username, password)
            return client

        except (LoginRequired, ClientError) as e:
            logger.error(f"Login failed {username}: {e}")
            return None

    def upload_video(self, username, password, file_id, caption):

        file_path = self._download_telegram_file(file_id)

        if not file_path:
            return False

        proxies = self._load_proxies()

        if not proxies:
            proxies = [None]

        random.shuffle(proxies)

        for proxy in proxies:

            client = self._instagram_login(username, password, proxy)

            if not client:
                continue

            try:

                media = client.video_upload(file_path, caption=caption)
                views = getattr(media, "view_count", 0)

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

                logger.info(f"Uploaded {file_id} for {username}")

                if os.path.exists(file_path):
                    os.remove(file_path)

                client.logout()
                return True

            except VideoNotUploaded:
                logger.error("Upload failed")
                continue

            except (ClientError, LoginRequired):
                logger.error("Account issue")
                break

        if os.path.exists(file_path):
            os.remove(file_path)

        return False
