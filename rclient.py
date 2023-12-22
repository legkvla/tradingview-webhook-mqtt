import app

def send_signal(ev):
    #Filtering positions closing
    if ev.get('strategy-prev_market_position') != 'flat':
        return
    url = "http://localhost:3002/trading/signals"
    headers = {"Content-Type": "application/json"}
    try:
        data = {
            "heartbeat": ev.get('heartbeat', False),
            "ttl": ev['ttl'],
            "strategy-id": ev['strategy-id'],
            "symbol": ev['ticker'],
            "side": ev['strategy-order-action'],
            "price": ev['strategy-order-price'],
            "sl-offset": ev.get('sl-offset'),
            "tp-offset": ev.get('tp-offset')
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

def main():
    while True:
        e = app.a_pop()
        if e is not None:
            # j = json.dumps(e[1].decode())
            msg = e[1].decode()
            print(f'Event: {msg}')
            send_signal(json.loads(msg))

if __name__ == “__main__”:
    main()