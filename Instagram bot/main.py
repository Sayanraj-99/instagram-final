import database
from scheduler import AutoScheduler
from bot import app
# Initialize database
database.init_db()

# Start scheduler
scheduler = AutoScheduler()
scheduler.start()

# Start bot
app.run_polling()
