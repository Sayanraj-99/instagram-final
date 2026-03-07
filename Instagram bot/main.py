import database
from scheduler import Scheduler
import threading

# Initialize database
database.init_db()

# Start scheduler in background
scheduler = Scheduler()
thread = threading.Thread(target=scheduler.run)
thread.start()

# Start bot
from bot import app
app.run_polling()
