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

# ====== ENV VARIABLES ======
TELEGRAM_TOKEN = os.environ.get("8648455166:AAEYGHn7DshRjK8YMeJUDf1Z2UtbGgrcbCQ")
OPENAI_API_KEY = os.environ.get("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")

# ====== GROQ CLIENT ======
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ====== DEFAULT MODE ======
user_modes = {}  # user_id: "soft" / "demon"


# ====== START COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "মুরুব্বি 🧔‍♂️ হাজির।\n"
        "Mode change করতে লিখো:\n"
        "/soft অথবা /demon"
    )


# ====== MODE COMMANDS ======
async def soft_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_modes[update.effective_user.id] = "soft"
    await update.message.reply_text("Soft roast mode চালু 😌")


async def demon_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_modes[update.effective_user.id] = "demon"
    await update.message.reply_text("Demon roast mode চালু 😈")


# ====== MESSAGE HANDLER ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id

    level = user_modes.get(user_id, "soft")

    if level == "demon":
        system_prompt = """
        You are 'মুরুব্বি', a cold ruthless Bengali roast master.
        Speak only Bengali.
        Short brutal lines.
        No kindness.
        No vulgar abuse.
        Make it psychologically sharp.
        """
    else:
        system_prompt = """
        You are 'মুরুব্বি', a witty sarcastic Bengali guru.
        Speak only Bengali.
        Short sharp roast.
        No vulgar abuse.
        """

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.9,
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("আজ মুরুব্বির মুড অফ 😑")


# ====== MAIN FUNCTION ======
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
