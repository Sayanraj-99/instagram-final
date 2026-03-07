import database


def add_proxy(proxy):

    conn = database.get_connection()
    c = conn.cursor()

    c.execute(
        "INSERT INTO proxies(proxy) VALUES(?)",
        (proxy,)
    )

    conn.commit()
    conn.close()


def get_proxies():

    conn = database.get_connection()
    c = conn.cursor()

    c.execute("SELECT proxy FROM proxies")

    rows = c.fetchall()

    conn.close()

    return [r[0] for r in rows]
