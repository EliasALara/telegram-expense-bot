# Telegram version of the bot

import os
import urllib.parse
import logging
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# OpenAI client
client = OpenAI(api_key=openai_api_key)

# Allowed subcategories (for filtering)
allowed_subcategories = [
    "Snacks", "Fiction", "Non-fiction", "Side Hustle", "Parents", "Private", "Public"
]

# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print("Incoming message:", user_msg)

    prompt = f"""
You are a helpful assistant that converts text messages into structured data for an expense tracker.
Use only the following categories and subcategories:

- Dining
  - Snacks
- Groceries
- Shopping
- Books
  - Fiction
  - Non-fiction
- Income
  - Side Hustle
  - Parents
- Transit
  - Private
  - Public
- Gifts
- Entertainment
- Personal
- Travel

Accounts must be one of: Cash, Credit Card, Bank.

If the message describes an expense, make the amount negative.
If it describes income or receiving money, make the amount positive.

Respond only in JSON format with keys: amount, title, category, subcategory, account.
Only include subcategory when appropriate. If it's unclear or unnecessary, set it to "Uncategorized".

Input: "{user_msg}"
Output:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content.strip()
        print("Raw OpenAI output:", raw_output)

        # Clean up code block formatting
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`").strip()
            if raw_output.startswith("json"):
                raw_output = raw_output[4:].strip()

        data = eval(raw_output)  # Use json.loads() in production

        query_data = {
            "amount": data["amount"],
            "title": data["title"],
            "category": data["category"],
            "account": data["account"]
        }

        subcat = data.get("subcategory", "").strip()
        if subcat in allowed_subcategories:
            query_data["subcategory"] = subcat

        query_string = urllib.parse.urlencode(query_data)
        link = f"https://cashewapp.web.app/addTransaction?{query_string}"

        await update.message.reply_text(link)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("Sorry, I couldn't understand that expense message.")

# Set up and run the bot
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Telegram bot is running...")
    app.run_polling()