import sys
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, curr_dir+"/deps")

import json
import redis
import requests
import traceback

from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

SEC_KEY=os.getenv("SEC_KEY", 'DEFAULT_KEY')
REDIS_URL=os.getenv("REDIS_TLS_URL", '')

url = urlparse(REDIS_URL)
r = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)

auth_token = None

def get_auth_token():
    global auth_token
    if auth_token is None:
        url = "http://localhost:3002/auth/login-token"
        headers = {"Content-Type": "application/json"}
        data = {'token': SEC_KEY}
        response = requests.post(url, json=data, headers=headers)
        auth_token = response.json()['jwt-token']
    return auth_token

def send_signal(ev):
    #Filtering positions closing
    # if ev.get('strategy-prev_market_position') != 'flat':
    #     return
    
    url = "http://localhost:3002/trading/signals"
    try:
        headers = {"Content-Type": "application/json", "Authorization": "Token " + get_auth_token()}
        data = {
            "heartbeat": ev.get('heartbeat', False),
            "ttl": ev['ttl'],
            "strategy-id": ev['strategy-id'],
            "symbol": ev['ticker'],
            "side": ev['strategy-order-action'],
            "price": float(ev['strategy-order-price']),
            "sl-offset": ev.get('sl-offset'),
            "tp-offset": ev.get('tp-offset'),
            "signal-kind": ev.get('strategy-prev_market_position') == 'flat' ? 'open' : 'close'
        }
        response = requests.post(url, json=data, headers=headers)

        # Check if the request was successful (status code 2xx)
        if response.ok:
            print("Request successful")
            print("Response:", response.json())
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response:", response.text)

    except Exception as e:
        print(f"Request failed: {e}")
        traceback.print_exc()

def main():
    while True:
        e = r.brpop('signals', 0)
        if e is not None:
            # j = json.dumps(e[1].decode())
            msg = e[1].decode()
            print(f'Event: {msg}')
            send_signal(json.loads(msg))

if __name__ == "__main__":
    main()
