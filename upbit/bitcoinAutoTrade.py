import time
import pyupbit
import datetime
import requests
import yaml

access = "2bpxnn6gmgNH6Tw5jtNzlbQ5ykPgbh4OLSUeWs4e"
secret = "2cMIRaeVw8L5xRI1Q4WZgUkh63dMNbrfu5GyOcVr"
discord_url = "https://discord.com/api/webhooks/1236272079930920992/R-P5iEb9J6CHV5tRMmGlU-ISVSkSCWyTFOQzMFWf1iJhRnYcEGfrRxeWraZ1aQK7Ivzv"

def send_message(msg):
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    requests.post(discord_url, data=message)
    print(message)

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    send_message(ticker)
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
print(get_target_price("KRW-BTC", 0.3))
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.3)
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    print("=== 비트 구매 ===")
                    print(get_balance("BTC"))
                    print("===============")
                    print("=== 비트 구매 후 잔고 ===")
                    print(get_balance("KRW"))
                    print("===============")
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                print("=== 비트판매 후 잔고 ===")
                print(get_balance("KRW"))
        time.sleep(1)
    except Exception as e:
        print("에러!!!")
        print(e)
        time.sleep(1)