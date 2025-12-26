from flask import Flask, render_template, request, jsonify, session, redirect
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.secret_key = "simple-secret-key"
CORS(app)

# ---------------- GROQ CONFIG ----------------
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return render_template("login.html", error="Username required")

        session["user"] = username
        session["history"] = []
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html", user=session["user"])


# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"reply": "⚠️ Please login first"})

    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "⚠️ Empty message"})

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a friendly AI assistant. Always start with: How can I help you today?"},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload, timeout=20)
        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        bot_reply = f"❌ Server Error: {str(e)}"

    session["history"].append({"user": user_message, "bot": bot_reply})
    return jsonify({"reply": bot_reply})


# ---------------- RUN (RENDER READY) ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
