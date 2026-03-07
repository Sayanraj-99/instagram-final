import database
import random


def add_proxy(proxy):

    conn = database.get_connection()
    c = conn.cursor()

    try:

        c.execute(
            "INSERT INTO proxies(proxy) VALUES(?)",
            (proxy,)
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


def get_proxies():

    conn = database.get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT proxy FROM proxies WHERE status='active'"
    )

    rows = c.fetchall()

    conn.close()

    return [r["proxy"] for r in rows]


def get_random_proxy():

    proxies = get_proxies()

    if not proxies:
        return None

    return random.choice(proxies)
