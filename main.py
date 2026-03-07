import database
from scheduler import AutoScheduler
from instagram_bot.bot import app
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


# initialize database
database.init_db()


# start scheduler
scheduler = AutoScheduler()
scheduler.start()

print("Scheduler started")


# start telegram bot
def run_bot():
    print("Bot started")
    app.run_polling()


bot_thread = threading.Thread(target=run_bot)
bot_thread.start()


# small web server so Render doesn't kill the process
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")


def run_server():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()


server_thread = threading.Thread(target=run_server)
server_thread.start()
