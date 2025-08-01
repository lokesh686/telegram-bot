from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from database import add_expense, get_summary, reset_expenses

# bot.py
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *Expense Tracker Bot*!\n\n"
        "Use /add <amount> <category> to log an expense.\n"
        "Example: `/add 250 food`\n\n"
        "Other commands:\n"
        "/summary - View your expenses\n"
        "/clear - Reset all your expenses\n"
        "/help - Show help message",
        parse_mode="Markdown"
    )

# Help message
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *Expense Tracker Bot Help*\n\n"
        "📌 Commands:\n"
        "/add <amount> <category> – Add a new expense\n"
        "/summary – Show expenses grouped by category\n"
        "/clear – Clear all expenses\n"
        "/start – Restart the bot\n"
        "/help – Show this message",
        parse_mode="Markdown"
    )

# Add expense
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        category = context.args[1].lower()
        user_id = update.message.chat_id
        add_expense(user_id, amount, category)
        await update.message.reply_text(f"✅ Added ₹{amount} to *{category}*!", parse_mode="Markdown")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Invalid format.\nUsage: `/add <amount> <category>`", parse_mode="Markdown")

# Show summary
async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    summary_text = get_summary(user_id)
    await update.message.reply_text(f"📊 *Your Expenses:*\n\n{summary_text}", parse_mode="Markdown")

# Clear all expenses
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    reset_expenses(user_id)
    await update.message.reply_text("🗑️ All your expenses have been cleared!")

# Handle unknown messages/commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ I didn't understand that command.\nUse /help to see what I can do.")

# Logging (optional)
def log_user_activity(update: Update):
    user = update.effective_user
    print(f"User {user.first_name} ({user.id}) sent a message.")

# Run the bot
app = ApplicationBuilder().token("7619357753:AAE4UNTnQg1jB9M0rYlEn22tX3xcpshB4S4").build()

# Command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("summary", summary))
app.add_handler(CommandHandler("clear", clear))

# Fallback for unknown commands
app.add_handler(MessageHandler(filters.COMMAND, unknown))

print("✅ Bot is running...")
app.run_polling()
