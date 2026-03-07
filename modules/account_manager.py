import database

def add_account(username):

    conn = database.get_connection()
    c = conn.cursor()

    c.execute(
        "INSERT INTO accounts(username) VALUES(?)",
        (username,)
    )

    conn.commit()
    conn.close()


def delete_account(username):

    conn = database.get_connection()
    c = conn.cursor()

    c.execute(
        "DELETE FROM accounts WHERE username=?",
        (username,)
    )

    conn.commit()
    conn.close()


def get_accounts():

    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT username FROM accounts")

    rows = c.fetchall()

    conn.close()

    return [r[0] for r in rows]
