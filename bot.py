import MetaTrader5 as mt5
import time

# Connect to MT5
mt5.initialize()

# Trading pairs
pairs = ["XAUUSD", "BTCUSDC"]

# Settings
lot = 0.01
grid_distance = 300   # points
take_profit = 200
magic = 123456


def open_trade(symbol, order_type):
    
    price = mt5.symbol_info_tick(symbol).ask if order_type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "tp": price + take_profit * mt5.symbol_info(symbol).point if order_type == mt5.ORDER_TYPE_BUY else price - take_profit * mt5.symbol_info(symbol).point,
        "deviation": 20,
        "magic": magic,
        "comment": "LowRiskBot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    mt5.order_send(request)


def check_positions(symbol):
    positions = mt5.positions_get(symbol=symbol)
    return positions


while True:
    
    for pair in pairs:

        positions = check_positions(pair)

        if positions is None or len(positions) == 0:
            open_trade(pair, mt5.ORDER_TYPE_BUY)

        else:
            last_price = mt5.symbol_info_tick(pair).bid

            for pos in positions:

                if pos.type == 0:
                    if last_price < pos.price_open - grid_distance * mt5.symbol_info(pair).point:
                        open_trade(pair, mt5.ORDER_TYPE_BUY)

                if pos.type == 1:
                    if last_price > pos.price_open + grid_distance * mt5.symbol_info(pair).point:
                        open_trade(pair, mt5.ORDER_TYPE_SELL)

    time.sleep(10)
