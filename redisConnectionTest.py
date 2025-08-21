import requests
import json
import time

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
total_elapsed = 0
average_elapsed = 0
i = 1
while i > 0:
  start_time = time.perf_counter()
  response = requests.post(url, headers=headers, data=payload, timeout=15)
  elapsed_ms = (time.perf_counter() - start_time) * 1000.0
  total_elapsed += elapsed_ms
  average_elapsed = total_elapsed / i

  print(f"HTTP {response.status_code} in {elapsed_ms:.2f} ms")
  print(response.text)
  print(f"Average HTTP success in : {average_elapsed:.2f}")
  i = i + 1
  if response.status_code != 200:
    break