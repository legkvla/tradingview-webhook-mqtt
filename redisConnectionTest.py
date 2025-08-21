import requests
import json

url = "http://213.58.150.82:8080/webhook"

payload = json.dumps({
  "key": "GwY(JSh7S!",
  "data": {
    "strategy-order-action": "buy",
    "strategy-order-price": 1.1234,
    "ticker": "EUR/USD"
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
