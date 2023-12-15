import os
import time
from fastapi import FastAPI, Request

SEC_KEY=os.getenv("SEC_KEY", 'DEFAULT_KEY')

app = FastAPI()

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
            return 200
        else:
            return 400
