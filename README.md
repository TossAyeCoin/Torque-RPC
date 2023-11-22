# Torque RPC API

This is an API which queries a list of RPCs for top of block and low latency.

## HOW 2 RUN

To run this. Make sure you have Python +3.9 installed, web3 +6.0.0

```bash
  pip install fastapi aiohttp web3 uvicorn
  python .\main.py
```

In API.py - Change the latency filter to whatever time you want and update the RPC list to match your RPCs. This should work with any RPC list.

## API Reference

#### Get chain tip rpc block

```http
  GET /toprpc
```

### Return Value

```
{
    "rpc_url": "URL_ADDRESS",
    "blocknumber": INT_BLOCKNUMBER
}
```

## Optimizations

I would like to add multiple chains to this api in the future, but I am working mainly on Optimism for now.
