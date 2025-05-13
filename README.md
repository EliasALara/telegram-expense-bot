# 📊 Telegram Expense Bot

A smart Telegram bot that uses GPT-4o to convert natural language messages into structured expense or income entries for [Cashew](https://cashewapp.web.app/), a personal finance tracking app.

Runs 24/7 as a Render Background Worker using Python, OpenAI, and the Telegram Bot API.

## 💡 Example

You send a message like:

```
I spent $80 on groceries with my credit card
```

The bot replies with a structured App Link:

```
https://cashewapp.web.app/addTransaction?amount=-80&title=Groceries&category=Groceries&account=Credit%20Card
```

## ⚙️ Features

- Natural language input via Telegram
- Categorizes your expense or income
- Infers account (Cash, Credit Card, Bank)
- Selects from predefined categories and subcategories
- Automatically signs expenses as negative and income as positive
- Hosted as a background worker — no web server needed

## 📁 Project Structure

```
telegram-expense-bot/
├── bot.py                # Main Telegram bot logic
├── .env                  # API keys (ignored by Git)
├── requirements.txt      # Python dependencies
```

## 🔐 .env File Format

> This file is not tracked in Git and must be added manually.

```
OPENAI_API_KEY=your-openai-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

## 🚀 Deploy on Render

1. Push this repo to GitHub
2. Go to [https://render.com](https://render.com)
3. Click **New → Background Worker**
4. Select your GitHub repo
5. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
6. Add environment variables:
   - `OPENAI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
7. Click **Create Background Worker**

Your bot is now running in the cloud 🎉

## 📄 License

MIT License  
Created by [Elias A. Lara](https://github.com/EliasALara)
