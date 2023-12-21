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
    "key": "SECURITY_KEY",
    "data":
    {
      "heartbeat" : "false",
      "signal-id" : "signal1",
      "ticker" : "ETH/USD",
      "strategy-order-action": "buy",
      "strategy-order-price": 1.1234,
      "strategy-prev_market_position": "flat"
    }
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
