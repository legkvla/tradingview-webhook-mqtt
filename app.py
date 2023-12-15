import json
import os
import time
from fastapi import FastAPI, Request
import redis

SEC_KEY=os.getenv("SEC_KEY", 'DEFAULT_KEY')

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, db=0)

def try_redis():
    r.set('foo', 'bar')
    return r.get('foo')

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
        raise ValueError('Alert Message must be of type application/json')
    elif 'application/json' in headers['content-type']:
        data = await request.json()
        if 'key' not in data:
            raise ValueError('Missing key!')
        key = data['key']
        if key == SEC_KEY:
            if 'data' not in data:
                raise ValueError('Wrong Alert message format, "data" field not found!')
                return 400
            data = data['data']
            print(f'Publishing TradingView Alert {data}')
            r.lpush('signals', json.dumps(data))
            return {"success": True}
        else:
            return 400

@app.post("/pop-event")
async def pop_event():
    event = r.rpop('signals')
    if event is not None:
        return json.loads(event)
    else:
        return {"empty": True}
