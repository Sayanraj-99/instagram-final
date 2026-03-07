import database
from scheduler import AutoScheduler
from bot import app

if __name__ == "__main__":
    
    # Initialize database
    database.init_db()

    # Start scheduler
    scheduler = AutoScheduler()
    scheduler.start()

    print("Scheduler started")

    # Start bot
    print("Bot started")
    app.run_polling()
