import database
from scheduler import AutoScheduler

# Initialize database
database.init_db()

# Start scheduler
scheduler = AutoScheduler()
scheduler.start()

# Start bot
from bot import app
app.run_polling()
