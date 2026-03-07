from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import database
from instagram_manager import InstagramManager

# Initialize
app = Application.builder().token("YOUR_BOT_TOKEN").build()
manager = InstagramManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Instagram Bot Ready")

async def add_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /add username password")
        return
    
    username = context.args[0]
    password = context.args[1]
    manager.add_account(username, password)
    await update.message.reply_text("Account added")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = manager.get_stats(1)  # Simple demo
    await update.message.reply_text(f"Total Views: {stats['total_views']}")

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_account))
app.add_handler(CommandHandler("stats", stats))

# Start bot
app.run_polling()
