import requests
import time
import statistics

# Price API
pairs = {
    "BTCUSDC": "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDC",
    "XAUUSD": "https://api.binance.com/api/v3/ticker/price?symbol=XAUUSDT"
}

price_history = {
    "BTCUSDC": [],
    "XAUUSD": []
}

def get_price(url):
    data = requests.get(url).json()
    return float(data["price"])

while True:

    for pair, url in pairs.items():

        price = get_price(url)

        history = price_history[pair]
        history.append(price)

        if len(history) > 20:
            history.pop(0)

        if len(history) >= 10:

            ma_short = statistics.mean(history[-5:])
            ma_long = statistics.mean(history)

            print(f"\nPair: {pair}")
            print("Current Price:", price)
            print("MA Short:", ma_short)
            print("MA Long:", ma_long)

            if ma_short > ma_long:
                print("Signal: BUY")

            elif ma_short < ma_long:
                print("Signal: SELL")

            else:
                print("Signal: WAIT")

    time.sleep(15)
