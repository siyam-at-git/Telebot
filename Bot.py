import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)
from openai import OpenAI

# =========================
# 🔴 এখানে তোমার তথ্য বসাও
# =========================
TELEGRAM_TOKEN = "8648455166:AAEYGHn7DshRjK8YMeJUDf1Z2UtbGgrcbCQ"
OPENAI_API_KEY = "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"
# =========================

# ====== GROQ CLIENT ======
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ====== USER MODE STORAGE ======
user_modes = {}


# ====== START COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧔‍♂️ মুরুব্বি হাজির!\n\n"
        "/soft – হালকা ব্যঙ্গ\n"
        "/demon – নির্মম রোস্ট\n\n"
        "কিছু লিখে দেখ।"
    )


# ====== MODE COMMANDS ======
async def soft_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_modes[update.effective_user.id] = "soft"
    await update.message.reply_text("😌 Soft mode চালু হয়েছে।")


async def demon_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_modes[update.effective_user.id] = "demon"
    await update.message.reply_text("😈 Demon mode চালু হয়েছে।")


# ====== MESSAGE HANDLER ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id

    level = user_modes.get(user_id, "soft")

    if level == "demon":
        system_prompt = """
তুমি 'মুরুব্বি'।
ঠান্ডা, নির্মম, সংক্ষিপ্ত ব্যঙ্গ করবে।
১-২ লাইনে শেষ করবে।
কোনো অশ্লীল গালি ব্যবহার করবে।
"""
    else:
        system_prompt = """
তুমি 'মুরুব্বি'।
বুদ্ধিদীপ্ত, সংক্ষিপ্ত, মজাদার ব্যঙ্গ করবে।
১-২ লাইনে শেষ করবে।
গালি ব্যবহার করবে।
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.9,
            max_tokens=150,
        )

        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("আজ মুরুব্বির মুড ভালো না 😑")


# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("soft", soft_mode))
    app.add_handler(CommandHandler("demon", demon_mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
