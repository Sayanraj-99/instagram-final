import time
import threading
import database
from instagram_uploader import InstagramUploader


class AutoScheduler:

    def __init__(self):
        self.uploader = InstagramUploader()
        self.running = False

    def start(self):
        """Start scheduler thread"""

        if self.running:
            return

        self.running = True

        thread = threading.Thread(target=self._run)
        thread.daemon = True
        thread.start()

        print("Scheduler started")

    def _run(self):
        """Main scheduling loop"""

        while self.running:

            conn = database.get_connection()
            c = conn.cursor()

            # Get next pending video
            c.execute("SELECT id, file_id, caption FROM queue WHERE status='pending' LIMIT 1")
            video = c.fetchone()

            if video:

                video_id, file_id, caption = video

                # Mark as processing
                c.execute("UPDATE queue SET status='processing' WHERE id=?", (video_id,))
                conn.commit()

                # Get account
                c.execute("SELECT username, password FROM accounts WHERE status='active' LIMIT 1")
                account = c.fetchone()

                if account:
                    username, password = account

                    success = self.uploader.upload_video(
                        username,
                        password,
                        file_id,
                        caption
                    )

                    if success:
                        print("Upload successful")

                        c.execute(
                            "UPDATE queue SET status='uploaded', uploaded_at=CURRENT_TIMESTAMP WHERE id=?",
                            (video_id,)
                        )
                        conn.commit()

            conn.close()

            time.sleep(60)

    def stop(self):
        self.running = False
        print("Scheduler stopped")
