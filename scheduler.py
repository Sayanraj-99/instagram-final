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

            # Get next video
          c.execute("SELECT id, file_id, caption FROM queue WHERE status='pending' LIMIT 1")
            video = c.fetchone()

           if video:
    c.execute(
        "UPDATE queue SET status='processing' WHERE id=?",
        (video[0],)
    )
    conn.commit()

                # Get account
                c.execute("SELECT username, password FROM accounts LIMIT 1")
                account = c.fetchone()

                if account:

                    success = self.uploader.upload_video(
                        account[0],      # username
                        account[1],      # password
                        video[1],        # file_id
                        video[2]         # caption
                    )

               if success:

    print("Upload successful")

    c.execute(
        "UPDATE queue SET status='uploaded' WHERE id=?",
        (video[0],)
    )

    conn.commit()

            conn.close()

          time.sleep(30)


    def stop(self):

        self.running = False
        print("Scheduler stopped")
