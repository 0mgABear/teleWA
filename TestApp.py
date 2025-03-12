from flask import Flask, request
import os
import json

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") 
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json() 
    print(json.dumps(data, indent=4)) 
    return "Webhook received!", 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)