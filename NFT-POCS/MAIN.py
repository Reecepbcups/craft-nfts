'''
POC walling though stargaze NFT logic.

TODO: Reduce image size in memory? how to do that without saving it to disk?

We need to get "attributes" from the NFT for real estate..
https://app.stargaze.zone/_next/data/3Jb8ezi2ldFVhLZQYcnft/media/stars15pqspe0lcyeztwmk232vkwqgpklku5t74du00827l44p4vxnal7qvevcuw/2911.json

'''

import os, sys
import requests # httpx in future so async
from PIL import Image, UnidentifiedImageError
import io
from pymongo import MongoClient
import bech32

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# WALLET = "craft178n8r8wmkjy2e3ark3c2dhp4jma0r6zwce9z7k"
WALLET = "craft12wdcv2lm6uhyh5f6ytjvh2nlkukrmkdk4qt20v" # has omniflix nfts as well

client = MongoClient("mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin")
db = client["NFTs"]
OWNERS_COLLECTION = db["OWNERS"]

# TODO IDEA: Function to sort NFTs into their groups. EX: {"Genesis Rat ": ["#640", "#676"], "Sunnyside Reapers": ["1170"]}
# TODO IDEA: This way we could show them in game as the keys, select that & see all the sub groups you own

def main():

    NFT_QUERYS = { # Functions which query all NFTs held by an account address
        # ! I need to add a check to ensure only png, jpg, jpeg are allowed to be saved.
        "stars": getStargazeHeldNFTS,
        "omniflix": getOmniflixHeldNFTS,
        # Secret network, query_permit to allow name and get NFTs. Can it give us all NFTs we own?
        # CRAFT in the future
    }

    ALL_MY_NFTS = {} # myNFTs from all NFT platforms
    # for prefix in ["stars"]:
    for prefix in ["omniflix", "stars"]:    
        myNewAddr = convert_wallet_address(WALLET, prefix)
        print(f"Getting NFTs for: {myNewAddr} (from original: {WALLET})")

        myNFTs = NFT_QUERYS[prefix](myNewAddr)
        print(f"Len: {len(myNFTs)}")

        if len(myNFTs.keys()) > 0:
            ALL_MY_NFTS = {**myNFTs, **ALL_MY_NFTS}

    '''
    # -- STEP 1: Get all NFT's a wallet owns & save these to a cache on server {"name": "ipfs_link"}
    # updates the users NFTs based off the above query. Or blank if none
    '''
    updateUsersHoldings(WALLET, myNFTs, debug=False) 
    
    myDatabaseNFTS = getUsersDatabaseNFTS(WALLET) # {_id, address, nfts, realestate}
    print(f"\nAll {WALLET} NFT Names: ", dict(myDatabaseNFTS['nfts']).keys())

    '''
    # Step 3: Get an matching our request
    '''
    queryNFTName = "Starchoadz #6215"
    link = getLink(WALLET, queryNFTName)
    if len(link) > 0:
        print(f'Found link for {queryNFTName}: ', link)
        img = downloadImage(link, show=True)
        # saveImageToDrive(img, f"{searchNFT.replace(' ', '_')}.jpeg")
    else:
        print(f'It does not seem {WALLET} owns the {queryNFTName}')

    '''
    Step 3.1 - Simpler way w/out checks
    '''
    # ipfsLink = getLink(address="stars178n8r8wmkjy2e3ark3c2dhp4jma0r6zwdnpgsm", name="IBC Ninjas #780")
    # print('linkFoundForUser', ipfsLink)

def convert_wallet_address(address, prefix="craft") -> str:
    '''
    So we take their stars/omniflix address, and save as craft
    '''
    _, data = bech32.bech32_decode(address)
    return bech32.bech32_encode(prefix, data)

def downloadImage(link, show=False) -> Image:
    '''
    Remove exif data and compress in the future
    FIX THIS
    '''
    # ! if image link does not end with png, jpg, jpeg, its a video not image
    data = requests.get(link).content
    # with open(f"{CURRENT_DIR}/{output_name}", "wb") as f:
    #     f.write(r.content)    
    image = Image.open(io.BytesIO(data))
    if show: 
        print("Showing image...")
        image.show()
    return image

def saveImageToDrive(image: Image, outputFile: str, quality: int = 100):
    '''
    Not sure this would ever be needed to do?
    '''    
    img = image.convert('RGB')
    img.save(outputFile, optimize=True, format='JPEG', quality=quality)

def getImageLinkFromName(address, name, debug=True) -> str:
    import matplotlib.pyplot as plt # python3 -m pip install matplotlib
    # filter={'address': address, 'name': name}
    # if debug:
    #     print("Trying to find query matching:", name)

    doc = OWNERS_COLLECTION.find_one(filter={"address": address})
    if doc is None:
        if debug: print(f"No doc found for {address}")
        return ""

    value = ""
    if name in doc["nfts"]:
        value = doc["nfts"][name]
    
    if debug and len(value)==0: print(f"No NFT found for {name}")
    return value
    
    
def updateUsersHoldings(address, NFTNameLink: dict = {}, RealEstate: dict = {}, debug=True):
    query = {"address": address}
    q = OWNERS_COLLECTION.find_one(query)    

    if q is None:
        doc = {"address": address, "nfts": NFTNameLink, "realestate": RealEstate}
        OWNERS_COLLECTION.insert_one(doc).inserted_id
        if debug: print(f'New user {address} added {NFTNameLink=} {RealEstate}')
        return

    OWNERS_COLLECTION.update_one(query, {"$set": {"nfts": NFTNameLink, "realestate": RealEstate}}) 
    if debug: print(f'User {address} updated: {NFTNameLink=} {RealEstate}')   

def getUsersDatabaseNFTS(address: str):
    query = {"address": address}
    q = OWNERS_COLLECTION.find_one(query)
    if q is None:
        return {"address": address, "nfts": {}, "realestate": {}}
    return q


def getLink(address, name, debug=False):
    query = {"address": address}
    q = OWNERS_COLLECTION.find_one(query)
    if q is None:
        if debug: print(f"No doc found for {address}")
        return ""
    if name not in q['nfts']:
        if debug: print(f"No NFTs found for {name}")
        return ""
    return q["nfts"][name]

def stripEXIFDataFromImage(imageLoc):
    from PIL import Image
    QUALITY = 33
    image = Image.open(imageLoc)
    # next 3 lines strip exif
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(imageLoc,optimize=True,quality=QUALITY)

def getStargazeHeldNFTS(WALLET: str):
    API = "https://nft-api.stargaze-apis.com/api/v1beta/profile/{WALLET}/nfts".format(WALLET=WALLET)
    r = requests.get(API).json()
    nftData = {}
    for nft in r:
        # print(nft)
        nftName = nft['name']
        nftData[nftName] = nft['image']
    return nftData

def getOmniflixHeldNFTS(WALLET: str):    
    API = "https://data-api.omniflix.studio/nfts?owner={WALLET}".format(WALLET=WALLET)
    nftData = {}
    r = requests.get(API).json()["result"]['list']
    # print(r)
    for nft in r:        
        if 'owner' not in nft:
            continue # Skips NFTS they have listed or are are not NFTs

        nftName = nft['name']
        nftData[nftName] = nft['media_uri']
    return nftData


if __name__ == "__main__":
    main()