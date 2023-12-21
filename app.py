import json
import os
from fastapi import FastAPI, Request, HTTPException
import redis
from urllib.parse import urlparse

SEC_KEY=os.getenv("SEC_KEY", 'DEFAULT_KEY')
REDIS_URL=os.getenv("REDIS_TLS_URL", '')

app = FastAPI()

url = urlparse(REDIS_URL)
r = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)

def a_pop():
    return r.brpop('signals', 0)

def a_pop_loop():
    while True:
        e = a_pop()
        if e is not None:
            # j = json.dumps(e[1].decode())
            print(f'Event: {e[1].decode()}')

@app.get("/")
async def root():
    return {"message": "TradingView-Webhook-Bridge"}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    headers = request.headers
    qparams = request.query_params
    pparams = request.path_params

    if 'text/plain' in headers['content-type']:
        raise HTTPException(status_code=400, detail='Alert Message must be of type application/json')
    elif 'application/json' in headers['content-type']:
        data = await request.json()
        if 'key' not in data:
            raise HTTPException(status_code=401, detail='Missing auth key')
        key = data['key']
        if key == SEC_KEY:
            if 'data' not in data:
                raise HTTPException(status_code=400, detail='Wrong Alert message format, "data" field not found!')
            data = data['data']
            print(f'Publishing TradingView Alert {data}')
            r.lpush('signals', json.dumps(data))
            return {"success": True}
        else:
            raise HTTPException(status_code=401, detail='Wrong auth key')

@app.post("/pop-event")
async def pop_event(request: Request):
    data = await request.json()
    if 'key' not in data:
        raise HTTPException(status_code=401, detail='Missing auth key')
    key = data['key']
    if key == SEC_KEY:
        event = r.rpop('signals')
        if event is not None:
            return json.loads(event)
        else:
            return {"empty": True}
    else:
        raise HTTPException(status_code=401, detail='Wrong auth key')
