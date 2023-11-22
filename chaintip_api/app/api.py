from fastapi import FastAPI, Query,File, UploadFile, status
from fastapi.responses import FileResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import random
import aiohttp
from web3 import Web3

# Connection timeout, in seconds
# Good for filtering RPCs with high latency
connection_timeout_limit = 0.3

#list of RPC endpoints which will be checked
rpc_list = [
"https://optimism.llamarpc.com",
"https://optimism-mainnet.public.blastapi.io",
"https://mainnet.optimism.io",
"https://optimism.blockpi.network/v1/rpc/public",
"https://endpoints.omniatech.io/v1/op/mainnet/public",
"https://op-pokt.nodies.app",
"https://rpc.ankr.com/optimism",
"https://api.zan.top/node/v1/opt/mainnet/public",
"https://optimism.publicnode.com",
"https://rpc.optimism.gateway.fm",
"https://gateway.tenderly.co/public/optimism",
"https://optimism.gateway.tenderly.co",
"https://optimism.meowrpc.com",
"https://1rpc.io/op",
"https://optimism.drpc.org",
"https://optimism.api.onfinality.io/public",
]

app = FastAPI(title="ChainTip API",
    version="1.0.0",
    contact={
        "name": "TossAyeCoin",
    }
)

origins = [
    "http://localhost:8000",
    "localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
async def get_block_number(session, rpc_url):
    timeout = aiohttp.ClientTimeout(total=connection_timeout_limit)
    try:
        async with session.post(rpc_url, json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}, timeout=timeout) as response:
            json_response = await response.json()
            blocknumber = int(json_response['result'], 16)
            return {"rpc_url": rpc_url, "blocknumber": blocknumber}
    except asyncio.exceptions.TimeoutError:
        # print(f"Timeout error occurred while fetching block number from {rpc_url}")
        return {"rpc_url": rpc_url, "blocknumber": 0}

async def fetch_all_block_numbers(rpc_list):
    async with aiohttp.ClientSession() as session:
        tasks = [get_block_number(session, rpc_url) for rpc_url in rpc_list]
        return await asyncio.gather(*tasks)

def rpc_hunter(rpc_list):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        blocklist = loop.run_until_complete(fetch_all_block_numbers(rpc_list))
        loop.close()
        highest_block_number = max(block['blocknumber'] for block in blocklist)
        top_rpc_urls = [block['rpc_url'] for block in blocklist if block['blocknumber'] == highest_block_number]
        print(f"block: {highest_block_number} | RPC: {random.choice(top_rpc_urls)}")
        return random.choice(top_rpc_urls), highest_block_number
    except Exception as e:
        print(f"Error: {e}")
        return random.choice(rpc_list), 0


#default Route
@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to the ChainTip RPC Searcher."}

#list all routes
@app.get("/endpoints")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list

@app.get("/toprpc")
def get_all_urls():
    url, blocknumber = rpc_hunter(rpc_list)
    return {"rpc_url": url, "blocknumber": blocknumber}
