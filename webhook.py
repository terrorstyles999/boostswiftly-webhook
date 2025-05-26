from flask import Flask, request
import json
import os

app = Flask(__name__)
CREDIT_FILE = "user_credits.json"

# Load & Save credits
def load_credits():
    if not os.path.exists(CREDIT_FILE):
        return {}
    with open(CREDIT_FILE, "r") as f:
        return json.load(f)

def save_credits(data):
    with open(CREDIT_FILE, "w") as f:
        json.dump(data, f)

@app.route("/", methods=["GET"])
def home():
    return "NOWPayments Webhook is Live ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook received:", data)

    if data.get("payment_status") != "finished":
        return "ignored", 200

    order_id = data.get("order_id", "")
    if "_" not in order_id:
        return "invalid order ID", 400

    user_id, amount = order_id.split("_")
    amount = float(amount)

    credits_to_add = {
        1.5: 10,
        7.0: 50,
        15.0: 100,
        90.0: 1000
    }.get(amount, 0)

    if credits_to_add == 0:
        return "invalid amount", 400

    credit_data = load_credits()
    credit_data[user_id] = credit_data.get(user_id, 0) + credits_to_add
    save_credits(credit_data)

    return "success", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Render uses port from env, this is placeholder
