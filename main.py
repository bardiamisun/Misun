from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# 🔍 DEBUG: Check if the API key is being read
api_key = os.environ.get("OPENAI_API_KEY")
print("LOADED API KEY (first 5 letters):", api_key[:5] if api_key else "None found")

# 🔑 Initialize OpenAI with the API key
client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return "🤖 DM Auto-Reply Bot is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    message = data.get("message", "")
    username = data.get("username", "")

    if not message:
        return jsonify({"error": "No message received"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"{username} says: {message}"}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)