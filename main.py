import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

openai.api_key = os.getenv("OPENAI_API_KEY")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    username = update.message.from_user.first_name

    # Only respond if this is a group and bot is mentioned, or private chat
    if update.message.chat.type != "private" and f"@{context.bot.username}" not in text:
        return

    prompt = text.replace(f"@{context.bot.username}", "").strip()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant in a Telegram chat."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(f"{username}, {reply}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Missing TELEGRAM_BOT_TOKEN")
    else:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.run_polling()
