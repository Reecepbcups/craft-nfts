from pymongo import MongoClient
import requests
import os

# list of helper utility functions which handle unique logic
from FINAL_UTILS import convertBech32WalletToNew, downloadImageToMemoryAndShow, saveImageToDrive

'''
This POC goes over the logic needed for the NFT webapp.
I have async webapp endpoints in the WEBAPP-POC/nft/test.js folder.
(I am very bad at javascript, something I need to spend a lot more time in to learn)


FLow:
1. Get a users CRAFT wallet address (or cosmos ATOM)
2. Bech32 convert that address into other NFT platforms (stargaze, omniflix, juno[future])
3. Loop through these new addresses & query the correct function API to get their NFTs
   - Format: {"address": "craftaddress", "nfts": {"name", "ipfslink", ...}, "realestate": {"name", "ipfslink", ...}}
   - Real estate is not yet done, so the foramt is not final. May just be an IPFS link as well.
   - Real estate endpoint will be queried the CRAFT chain.

Note to self: Store "attributes" from the NFT for real estate?
https://app.stargaze.zone/_next/data/3Jb8ezi2ldFVhLZQYcnft/media/stars15pqspe0lcyeztwmk232vkwqgpklku5t74du00827l44p4vxnal7qvevcuw/2911.json
'''

# Sets current folder as NFT-POCS
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


# connection to mongodb, NFTs Database with collection as holdings 
# {"address": "craftaddress", "nfts": {"name": "ipfslink", ...}, "realestate": {"name": "ipfslink", ...}}
client = MongoClient("mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin")
db = client["NFTs"]
OWNERS_COLLECTION = db["AssetHoldings"] 
OWNERS_COLLECTION.create_index([("address", 1)]) # Does this speed up return times?


print("WEBAPP\ncraft12wdcv2lm6uhyh5f6ytjvh2nlkukrmkdk4qt20v (omniflix as well)\ncraft178n8r8wmkjy2e3ark3c2dhp4jma0r6zwce9z7k (stargaze only)") 
WALLET = input("\n(KEPLR) WHAT IS YOUR CRAFT ADDRESS? ") or "craft12wdcv2lm6uhyh5f6ytjvh2nlkukrmkdk4qt20v"


def main():

    # Map of wallet prefix & the function it uses to get NFTs held by the wallet
    NFT_QUERYS = {      
        "stars": getStargazeHeldNFTS,
        "omniflix": getOmniflixHeldNFTS,
        "secret": None, # webapp will need a query_permit to get NFTs
        "craft": None,
    }

    # Map of every NFT we hold in the format {"name": "ipfslink", }
    ALL_MY_NFTS = {} 
    
    for prefix in ["omniflix", "stars"]:  
        # converts their CRAFT address -> stars & omniflix so we can query  
        myNewAddr = convertBech32WalletToNew(WALLET, prefix)
        print(f"Getting NFTs for: {myNewAddr} (from original: {WALLET})")

        # Calls the correct function to query their wallet, returns Map of many NFts
        myNFTs = NFT_QUERYS[prefix](myNewAddr)
        print(f"Len: {len(myNFTs)}")

        # If more than 0 NFts are there, we append all NFTs to ALL_MY_NFTS Map.
        if len(myNFTs.keys()) > 0:
            ALL_MY_NFTS = {**myNFTs, **ALL_MY_NFTS}

    # We save all of these NFTs we just queried to the database with their address.
    # If there is no document it creates is, if there is it updates jusst the nft section.
    updateUsersHoldings(WALLET, myNFTs, debug=True) 
    
    # ! THIS CONCLUDES THE WEBAPP PORTION
    # ! THIS IS THE POC NOW FOR HOW THE MINECRAFT SERVER WILL HANDLE IT

    # On MC, we get a users documents based on their address. This will be linked in game via a DB => wallet
    # {address: "craftxxxx", nfts: {}, realestate: {}}

    myDatabaseNFTS = getUsersCollection(WALLET) 
    print(f"\nIN GAME MINECRAFT => All {WALLET}'s NFT Names:\n\n", dict(myDatabaseNFTS['nfts']).keys())

    while True: # just so we can confirm the names work, ctrl + c to exit
        queryNFTName = input("(GUI) WHICH NFT DO YOU WANT TO PLACE? (just shows the image here)") or "Starchoadz #6215"
        
        # Query database for address, if there get the nft section, and get queryNFTName
        # if there is no value for queryNFTName, it returns "" which means they dont own that NFT name.
        link = getLink(WALLET, queryNFTName) 
        if len(link) > 0:
            print(f'\nFound link for {queryNFTName}: ', link)
            img = downloadImageToMemoryAndShow(link, show=True)
            # saveImageToDrive(img, f"{searchNFT.replace(' ', '_')}.jpeg")
        else:
            print(f'It does not seem {WALLET} owns the {queryNFTName}')

    # DEBUGGING Same as above, just more manual
    # ipfsLink = getLink(address="stars178n8r8wmkjy2e3ark3c2dhp4jma0r6zwdnpgsm", name="IBC Ninjas #780")
    # print('linkFoundForUser', ipfsLink)

# WEBAPP & IN GAME
def getUsersCollection(address: str, debug=False):
    '''
    Gets their document and returns it.
    - If they dont have one, it returns a blank document schema
    '''
    query = {"address": address}
    q = OWNERS_COLLECTION.find_one(query)
    if q is None:
        if debug:
            print(__name__, f"No document found for {address}")
        return {"address": address, "nfts": {}, "realestate": {}}
    return q  

# IN GAME
def getLink(address: str, name: str, debug=False) -> str:
    '''
    Makes a request to the database collection to find an account matching their wallet.
    If it finds it, it tries to find the NFT name in their keys. 
    If it finds that, it returns the IPFS link so we can download/use in game
    else: it will return an empty string
    '''
    doc = getUsersCollection(address, debug=False)
    if len(doc['nfts']) == 0:
        return ""

    value = ""
    if name in dict(doc["nfts"]).keys():
        value = doc["nfts"][name]

    if debug and len(value)==0: 
        print(f"No NFT found for {name}")

    return value


# WEBAPP & IN GAME (real estate qwueries only)
def updateUsersHoldings(address, NFTNameLink: dict = {}, RealEstate: dict = {}, debug=True) -> None:
    '''
    Tries to get a users collection, if it is not there it creates it.
    If it is there, it just sets NFTs and RealEstate to new values. (This way the document is not duplicated)
    '''
    query = {"address": address}
    q = OWNERS_COLLECTION.find_one(query)    

    if q is None:
        doc = {"address": address, "nfts": NFTNameLink, "realestate": RealEstate}
        OWNERS_COLLECTION.insert_one(doc).inserted_id
        if debug: 
            print(f'New user {address} added {NFTNameLink=} {RealEstate}')
        return

    OWNERS_COLLECTION.update_one(query, {"$set": {"nfts": NFTNameLink, "realestate": RealEstate}}) 
    if debug: 
        print(f'User {address} updated: {NFTNameLink=} {RealEstate}')   


# ===== QUERIES =====
# WEBAPP
def getStargazeHeldNFTS(WALLET: str):
    API = "https://nft-api.stargaze-apis.com/api/v1beta/profile/{WALLET}/nfts".format(WALLET=WALLET)
    r = requests.get(API).json()
    # print(r)
    nftData = {}
    for nft in r:    
        nftName = nft['name']
        nftImage = nft['image']
        if not any(nftImage.endswith(s) for s in [".png", ".jpg", ".jpeg"]):
            continue # it is not an image, so we skip it. Only stargaze shows file extensions for NFTs        
        nftData[nftName] = nftImage

    return nftData

# WEBAPP
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
    main() # calls the main function to start logic

