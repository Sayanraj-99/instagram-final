import database


def add_to_queue(file_id, caption):

    conn = database.get_connection()
    c = conn.cursor()

    c.execute(
        "INSERT INTO queue(file_id,caption) VALUES(?,?)",
        (file_id, caption)
    )

    conn.commit()
    conn.close()


def get_queue_count():

    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM queue")

    count = c.fetchone()[0]

    conn.close()

    return count


def get_next_video():

    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT id,file_id,caption FROM queue LIMIT 1")

    row = c.fetchone()

    if not row:
        conn.close()
        return None

    video = {
        "id": row[0],
        "file_id": row[1],
        "caption": row[2]
    }

    c.execute("DELETE FROM queue WHERE id=?", (video["id"],))

    conn.commit()
    conn.close()

    return video
