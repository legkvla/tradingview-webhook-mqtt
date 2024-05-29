# tradingview-webhook-mqtt

This fork forwards TradingView Alerts to Redis.
Messages can be read through Redis (app.a_pop_loop) or rest method pop-event.

Easily can be deployed to Heroku.

## Usage

Set up this env value on Heroku:

```yaml
environment:
  - SEC_KEY=123123
```

The current implementation requires TV Alert messages to be defined in `application/json` and must conform to the following model.

```json
{
    "data":
    {
      "strategy-order-action": "buy",
      "strategy-order-price": 1.1234,
      "sl-offset": 0.002,
      "tp-offset": 0.001,
      "heartbeat" : false,
      "strategy-id" : "s1",
      "ticker" : "EUR/USD",
      "strategy-prev_market_position": "flat"
    },
    "key": "SECURITY_KEY"
}
```

### Template for TV

```json
{
    "data":
    {
      "strategy-order-action": "{{strategy.order.action}}",
      "strategy-order-price": "{{strategy.order.price}}",
      "sl-offset": 0.003,
      "tp-offset": 0.001,
      "heartbeat" : false,
      "strategy-id" : "fibrsi-EURUSD",
      "ticker" : "{{ticker}}",
      "strategy-prev_market_position": "{{strategy.prev_market_position}}"
    },
    "key": "{{sec_key}}"
}
```

strategy-prev_market_position can be used to distinguish position opening from closing.

The `key` property of alert messages is mandatory in order to allow access to
the webhook server, as it implements a lightweight authorization layer. The
value of the `key` is defined on the server side via the `SEC_KEY` environmental
variable as earlier mentioned.

The `data` property can include custom schemes/models, though it must be of type
dictionary.

## Use in other deployments

Build the image using the following command:

```
docker build -t <MY_IMAGE_NAME> .
```
