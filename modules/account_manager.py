import database
import sqlite3
from instagrapi import Client
from instagram_auth import InstagramAuth


class InstagramManager:

    def __init__(self):

        self.auth = InstagramAuth()


    def add_account(self, username, password):

        conn = database.get_connection()
        c = conn.cursor()

        try:

            c.execute(
                "INSERT INTO accounts(username, password) VALUES(?,?)",
                (username, password)
            )

            conn.commit()

            return True

        except sqlite3.IntegrityError:

            return False

        finally:

            conn.close()


    def delete_post(self, username, password, post_id):

        client = self.auth.login_account(username, password)

        if client:

            client.media_delete(post_id)
            return True

        return False


    def get_stats(self, username):

        conn = database.get_connection()
        c = conn.cursor()

        c.execute("""
            SELECT 
                posts_count,
                total_views,
                AVG(CASE WHEN posts_count > 0 
                    THEN total_views * 1.0 / posts_count 
                    ELSE 0 END) as avg_views,
                MAX(views)
            FROM accounts a
            LEFT JOIN analytics an 
            ON a.id = an.account_id
            WHERE username = ?
        """, (username,))

        stats = c.fetchone()

        conn.close()

        return {
            "total_posts": stats[0] or 0,
            "total_views": stats[1] or 0,
            "avg_views": round(stats[2] or 0, 2),
            "max_views": stats[3] or 0
        }
