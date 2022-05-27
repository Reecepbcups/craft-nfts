# https://app.stargaze.zone/marketplace
# https://github.com/ipfs-shipyard/py-ipfs-http-client < Future?
'''
GOALS:
- find people who own NFts on stargaze OR omniflix
- with that wallet, make a rest query to get their NFT tokens
- Get those tokens IPFS link
- download that IPFS link as a filename
- store this in mongodb 

Future:
- Webapp to link what NFTs you own by connecting to wallet
'''
# https://app.stargaze.zone/profile/stars1j42087twdvkmkdqfedg0gq2c6wnp7ycdayllx4/all


WALLET = "stars1j42087twdvkmkdqfedg0gq2c6wnp7ycdayllx4"

import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

import requests # httpx in future so async

def downloadImage(name, link):
    if '.' not in name:
        name += ".jpg"
    r = requests.get(link)
    with open(f"{CURRENT_DIR}/{name}", "wb") as f:
        f.write(r.content)


def getImageLinkFromIPFS(imageURL: str) -> dict:
    r = requests.get(imageURL.replace("ipfs://", "https://ipfs.io/ipfs/")).json()
    output = {}

    if "name" in r:
        output["name"] = r["name"].replace(" ", "_")

    if 'image' in r:
        imgLink = r['image'].replace("ipfs://", "") 
        imgLink = f"https://ipfs.io/ipfs/{imgLink}"        
        output["link"] = imgLink
        print(imgLink)

    return output

def getNFTs(WALLET: str):
    API = "https://nft-api.stargaze-apis.com/api/v1beta/profile/{WALLET}/nfts".format(WALLET=WALLET)
    r = requests.get(API).json()
    for nft in r:
        # print(nft)
        print(nft['tokenUri'])

    
    # ipfs://QmUoHk4hY6mNoHgNEJDcy94APUky6o8xVmyD3YzddJtUWe/5885
    

# getNFTs(WALLET)
obj = getImageLinkFromIPFS("ipfs://QmUoHk4hY6mNoHgNEJDcy94APUky6o8xVmyD3YzddJtUWe/5885")
link = obj["link"]
name = obj["name"]

downloadImage(f"{WALLET}_{name}", link)


# omniflix https://github.com/OmniFlix/mainnet/tree/main/omniflixhub-1
# https://rest.omniflix.network:443

# id: onftdenom039541ba04dd4c0f94c1f1d177b97b74
# "symbol": "COSPK",

# Someones address
# omniflix1mltkk0ktaljxqmvuh7n703qcsjez6g22apq8ne
# curl -X GET "https://rest.omniflix.network/cosmos/bank/v1beta1/balances/omniflix1mltkk0ktaljxqmvuh7n703qcsjez6g22apq8ne" -H  "accept: application/json"

# info on a denom
# curl -X GET "https://rest.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenom039541ba04dd4c0f94c1f1d177b97b74" -H  "accept: application/json"

# get supply of a denom
# curl -X GET "https://rest.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenom039541ba04dd4c0f94c1f1d177b97b74/supply" -H  "accept: application/json"

