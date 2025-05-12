from flask import Flask, request
import os
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import urllib.parse

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Create Flask app
app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get('Body')
    print("Incoming message:", incoming_msg)

    # Prompt with allowed categories/subcategories
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
- Yield
- MISC

Accounts must be one of: Cash, Credit Card, Bank.

Respond **only** in JSON format with these keys: amount, title, category, subcategory, account.

Only include subcategory when appropriate. If it's unclear or unnecessary, set it to "Uncategorized".

Example input: "I spent $1.50 for cookies in cash"
Example output: {{
  "amount": -1.5,
  "title": "Cookies",
  "category": "Dining",
  "subcategory": "Snacks",
  "account": "Cash"
}}

Input: "{incoming_msg}"
Output:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content.strip()
        print("Raw OpenAI output:", raw_output)

        data = eval(raw_output)  # Replace with json.loads() in production

        # Build the URL query parameters dynamically
        query_data = {
            "amount": data["amount"],
            "title": data["title"],
            "category": data["category"],
            "account": data["account"]
        }

        # Only add subcategory if it’s not empty or "Uncategorized"
        subcat = data.get("subcategory", "").strip()
        if subcat and subcat.lower() != "uncategorized":
            query_data["subcategory"] = subcat

        query_string = urllib.parse.urlencode(query_data)
        link = f"https://cashewapp.web.app/addTransaction?{query_string}"

    except Exception as e:
        print("Error:", e)
        link = "Sorry, I couldn't understand that expense message."

    reply = MessagingResponse()
    reply.message(link)
    return str(reply)

if __name__ == "__main__":
    app.run(debug=True)