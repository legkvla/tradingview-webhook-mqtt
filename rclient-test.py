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
REDIS_URL=os.getenv("REDIS_URL", '')

url = urlparse(REDIS_URL)
r = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_ca_certs='./ca.crt', ssl_cert_reqs=None)

def resolve_signal_kind(ev):
    if ev.get('heartbeat', False):
        return 'heartbeat'
    elif ev.get('strategy-prev_market_position') == 'flat':
        return 'open'
    else:
        return 'close'

def main():
    while True:
        e = r.brpop('signals', 0)
        if e is not None:
            # j = json.dumps(e[1].decode())
            msg = e[1].decode()
            print(f'Event: {msg}')
            # send_signal(json.loads(msg))

if __name__ == "__main__":
    main()
