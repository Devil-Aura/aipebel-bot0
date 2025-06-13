import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN
from scraper import fetch_episode_links

async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a URL. Example:\n/get https://example.com")
        return

    url = context.args[0]
    await update.message.reply_text("🔍 Processing, please wait...")

    try:
        results = await fetch_episode_links(url)
        for ep_num, links in results.items():
            msg = f"📥 Episode {ep_num}\n"
            for quality, link in links.items():
                msg += f"🔹 {quality}: {link}\n"
            await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("get", get_handler))

if __name__ == "__main__":
    app.run_polling()
