from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client with your API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
        # Make request to OpenAI API
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