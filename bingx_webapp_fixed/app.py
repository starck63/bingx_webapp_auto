import os, time, hmac, hashlib, requests
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

API_KEY = "2RIq4KBDyO3tqNyHsFxNy5cQOuYtXuykKWZEJ4XJbOoygr859uQEF4xoBCIln6T02U7D3VvmWnYQtbrEaBkw"
API_SECRET = "G1zpIw5djZb2BZcqHZup68iqY6Nu3D2do7qx1UknvMcsDTguMusvZy3Kxa6uJwMOpA9PdH6GVn1uh0LfOxQ"
BASE_URL = "https://open-api.bingx.com"

def create_signature(params):
    query_string = "&".join(f"{k}={params[k]}" for k in sorted(params))
    return hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def get_btc_price():
    try:
        endpoint = "/openApi/spot/v1/ticker/24hr"
        ts = int(time.time() * 1000)
        params = {"symbol": "BTC-USDT", "timestamp": ts}
        params["signature"] = create_signature(params)
        headers = {"X-BX-APIKEY": API_KEY}
        response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
        data = response.json()
        return float(data["data"][0]["lastPrice"]) if data.get("code") == 0 else 0.0
    except Exception as e:
        print("BTC 오류:", e)
        return 0.0

def get_futures_balance():
    try:
        endpoint = "/openApi/swap/v2/user/balance"
        ts = int(time.time() * 1000)
        params = {"timestamp": ts}
        params["signature"] = create_signature(params)
        headers = {"X-BX-APIKEY": API_KEY}
        response = requests.get(BASE_URL + endpoint, headers=headers, params=params)
        data = response.json()
        balance_data = data.get("data", {}).get("balance", {})
        return float(balance_data.get("balance", 0.0))
    except Exception as e:
        print("잔고 오류:", e)
        return 0.0

@app.route("/get_data")
def get_data():
    return jsonify({
        "btc_price": get_btc_price(),
        "usdt_balance": get_futures_balance()
    })

@app.route("/")
def index():
    return render_template_string("<h1>BingX GUI 앱</h1><p>가격/잔고 데이터 제공 중...</p>")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
