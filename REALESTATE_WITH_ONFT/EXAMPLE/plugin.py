# This is a really rough idea of how the PLUGIN will work with real estate & syncing to players
import requests
import json

from os.path import dirname as parentDir # gets parent directory of a file
from os.path import isfile


'''
For this to work, 
- it will require MongoDB. [wallet->uuid connection]
- API (see all properties owned, get info on a property)

Endpoints:
http://127.0.0.1:5000/owned?address=omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh
http://127.0.0.1:5000/info?uuid=ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2

'''

WALLETS_COLLECTION = { # This is a MongoDB collection, for now we use omniflix for ONFT
    "omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh": "ReecepbcupsUUIDHere",
    "omniflix111111111111111111111111111111111111111": "FakeAddressChecking",
}

def main():
    for wallet in WALLETS_COLLECTION.keys():
        onJoin(wallet)


def onJoin(PlayerWallet):
    # We can get PlayerWallet from playersUUID in plugin
    ownedProperties = getOwnedProperties(PlayerWallet)
    saveUsersPropertiesToDatabase(PlayerWallet, ownedProperties)


def saveUsersPropertiesToDatabase(PlayerWallet, ownedProperties: dict):
    dbName = parentDir(__file__) + "/usersOwnedPropertyDB.json"

    if not isfile(dbName):
        with open(dbName, "w") as f:
            f.write("{}")

    with open(dbName, 'r') as oP: 
        database = json.load(oP)

    # We would save this in the users NFT collection to NFTS DB, AssetHoldings ['realestate'] section
    userID = WALLETS_COLLECTION[PlayerWallet]
    database[userID] = ownedProperties

    with open(dbName, "w") as oP: 
        json.dump(database, oP)


def getOwnedProperties(ADDRESS: str):
    myProperties = requests.get(f"http://127.0.0.1:5000/owned?address={ADDRESS}").json()
    return myProperties


if __name__ == '__main__':
    main()