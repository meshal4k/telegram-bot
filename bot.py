from keep_alive import keep_alive
keep_alive() 
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import imaplib
import email
import re

# إعدادات الإيميلات وأسرارها (ضع بياناتك هنا)
ROCKSTAR_EMAIL_GTA = "tofergrand@gmail.com"
ROCKSTAR_PASS_GTA = "vwtt glii ovdi jizs"
ROCKSTAR_IMAP_GTA = "imap.gmail.com"

ROCKSTAR_EMAIL_RDR2 = "toferredd@gmail.com"
ROCKSTAR_PASS_RDR2 = "zvbq bbsx szfa snbq"
ROCKSTAR_IMAP_RDR2 = "imap.gmail.com"

BOT_TOKEN = "7511900709:AAGAbfXsQpx3E9wPZC2UDMcjjvPmAN6_tdo"

def get_code_from_email(email_user, email_pass, imap_server, sender_email, regex_pattern):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        mail.select("inbox")
        result, data = mail.search(None, f'(FROM "{sender_email}")')
        if result != "OK" or not data[0]:
            return f"❌ لا توجد رسائل من {sender_email}."
        ids = data[0].split()
        latest_email_id = ids[-1]
        result, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        match = re.search(regex_pattern, body, re.IGNORECASE)
        if match:
            return f"✅ رمز التحقق هو: {match.group(1)}"
        else:
            return "❌ لا يوجد رمز تحقق بعد."
    except Exception as e:
        return f"⚠️ خطأ: {str(e)}"

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🎮 GTA 5", "🎮 RDR2"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("📋 الرجاء اختيار اللعبة من القائمة التالية:", reply_markup=reply_markup)

async def handle_game_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "🎮 GTA 5":
        await update.message.reply_text("🔍 جاري إرسال رمز التحقق من Rockstar (GTA 5)...")
        code = get_code_from_email(
            ROCKSTAR_EMAIL_GTA, ROCKSTAR_PASS_GTA, ROCKSTAR_IMAP_GTA,
            "noreply@rockstargames.com",
            r"Enter this code on the identity verification screen[:\s]+(\d{6})"
        )
        await update.message.reply_text(code)
    elif text == "🎮 RDR2":
        await update.message.reply_text("🔍 جاري إرسال رمز التحقق من Rockstar (RDR2)...")
        code = get_code_from_email(
            ROCKSTAR_EMAIL_RDR2, ROCKSTAR_PASS_RDR2, ROCKSTAR_IMAP_RDR2,
            "noreply@rockstargames.com",
            r"Enter this code on the identity verification screen[:\s]+(\d{6})"
        )
        await update.message.reply_text(code)
    else:
        await update.message.reply_text("❗ ارسل /start لتظهر لك قائمة الألعاب")

    if __name__ == "__main__":
        import asyncio
        async def main():
            app = Application.builder().token(BOT_TOKEN).build()
            app.add_handler(...)
            await app.run_polling()
        asyncio.run(main())
