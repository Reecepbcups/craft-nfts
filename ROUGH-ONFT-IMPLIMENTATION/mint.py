from os.path import dirname as parentDir
import json
from PIL import Image
import time
import os

OUR_NFT_DENOM = "onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b"
prefixName = "TestRE #"
ourPreviewImage = "https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg"

# We may need block_restrictions for the onft
KEYS_WE_DONT_NEED_IN_THE_NFT = ["block_restrictions", "current_renter", "current_owner", "state"]

thisFolder = parentDir(__file__)
jsonFile = f"{thisFolder}/info.json"
ipfsLinkFile = f"{thisFolder}/ipfs_links.json"

def main():

    for nftID, reUUID in data.items():
        '''
        nftID: The number which specifies this NFT (ex. 0001)
        reUUID: The UUID of the in game asset (is given when creating the property)
        '''    
        if nftID.startswith("IGNORE"):
            continue
        
        ipfsImageLink = links[nftID]
        # print(nftID, reUUID, ipfsImageLink)

        jsonObj = getAPI(reUUID)
        jsonObj = removeWebappAPIThings(jsonObj)
        # print(jsonObj)
        mintNFT(nftID, jsonObj)

def mintNFT(nftNumber: int = 0000, JSONData: dict = {}):
    # WHAT IF WE BASE64 ENCODE THE JSON DATA? json.loads(base64.b64decode(myStr).decode('UTF-8'))
    IPFS_IMAGE_LINK = links[nftNumber]
    # Example value this returns:  (( omniflixhubd q tx AEE050057EAD3EF2D1CE92ABCED615E17C256EA8D505EFF63FD162ED31164FA9  ))
    # omniflixhubd tx onft mint onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b --name="TestRE #0001" --media-uri="https://ipfs.io/ipfs/QmXozTQYxsR5gz18gdhwtCNV37jiQgtuR9n9nMTpSRM1jq" --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" --data="{'name': 'Property 1', 'type': 'House', 'description': 'This is a house', 'floorArea': 25, 'volume': 100, 'location': {'city': {'uuid': 'a71f5e33-5fa9-4de9-852a-dbed20b0be3a', 'name': 'craftcity'}, 'building': {'uuid': 'ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2', 'name': 'Building1'}, 'coordinates': {'x': 0, 'y': 0, 'z': 0}}, 'property_owner': {'uuid': '805a4070-2d4f-442e-9c7b-9194d1252325', 'username': 'Tesla_Stock'}}" --chain-id flixnet-4 --fees 200uflix --from reece

    JSONData = json.dumps(JSONData) # makes things double quoted
    # print(JSONData)
    

    # Do we need to strinfify data & escape?
    output = f"""omniflixhubd tx onft mint {OUR_NFT_DENOM} --name="{prefixName}{nftNumber}" --description="Craft Economy Real Estate Testing" --media-uri="{IPFS_IMAGE_LINK}" --preview-uri="{ourPreviewImage}" --data="{JSONData}" --chain-id flixnet-4 --fees 200uflix --from reece --yes"""
    print(output)

def removeWebappAPIThings(JSONObject: dict) -> dict:
    # remove keys from the JSONObject that are not needed for the webapp.
    # These keys are just for the marketplace
    for s in KEYS_WE_DONT_NEED_IN_THE_NFT:
        JSONObject.pop(s, None)    
    return JSONObject

def getAPI(uuid: str) -> dict:
    '''
    Here is an example of what the get request to f"crafteconomy.io/api/realestate/{uuid}"
    will return.
    Some values will not be used for the IPFS generation, but only for the webapp marketplace.
    '''
    EXAMPLE_API = {
        "ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2": {
            "name": "Property 1",
            "type": "House",
            "description": "This is a house",
            "floorArea": 25,
            "volume": 100,        
            "block_restrictions": {
                # Is this final for a property? maybe we just save the NAME of the restriction if so to IPFS.
                "CHEST": 5,
                "FURNACE": 5
            }, 
            "location": {
                "city": {
                    "uuid": "a71f5e33-5fa9-4de9-852a-dbed20b0be3a",
                    "name": "craftcity"
                },
                "building": {
                    "uuid": "ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2",
                    "name": "Building1"
                },
                "coordinates": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                },
            },
            "state": "OWNED", # WEBAPP ONLY
            "current_renter": { # WEBAPP ONLY
                "uuid": "79da3753-1b9e-4340-8a0f-9ea975c17fe4",
                "username": "Reecepbcups",
            },
            "property_owner": { # WEBAPP ONLY
                "uuid": "805a4070-2d4f-442e-9c7b-9194d1252325",
                "username": "Tesla_Stock",
            }
        },
        "f6ebbe2d-f5ca-4756-8d0c-b5973c0d0006": {
            "name": "Property 2",
            "type": "Business",
            "description": "This is a business",
            "floorArea": 50,
            "volume": 500,        
            "block_restrictions": {
                # Is this final for a property? maybe we just save the NAME of the restriction if so to IPFS
                # none for the business
            }, 
            "location": {
                "city": {
                    "uuid": "a71f5e33-5fa9-4de9-852a-dbed20b0be3a",
                    "name": "craftcity"
                },
                "building": {
                    "uuid": "892f8bb6-df50-49dd-b06a-93b9de72e27e",
                    "name": "Building2"
                },
                "coordinates": {
                    "x": 100,
                    "y": 100,
                    "z": 100
                },
            },
            "state": "RENTED", # WEBAPP ONLY
            "current_renter": { # WEBAPP ONLY
                "uuid": "79da3753-1b9e-4340-8a0f-9ea975c17fe4",
                "username": "Reecepbcups",
            },
            "property_owner": { # WEBAPP ONLY
                "uuid": "805a4070-2d4f-442e-9c7b-9194d1252325",
                "username": "Tesla_Stock",
            }
        },
    }
    
    return EXAMPLE_API.get(uuid, None)



    
    

    # image = f"{thisFolder}/screenshots/{nftID}.png" # path/0001.png
    # reType = data[nftID]['type']    
    # uuid = data[nftID]['id']
    # location = getThisFromRESTAPI based on the property uuid
    # size = data[nftID]['size'] #>> can we easily get this from the restAPI when made? or do we have to manually find this for each property


    
    # print(f"CRAFT RealEstate #{nftID}: {reType=}, {uuid=}, {image=}")

    # We can only view 1 image at a time, would have to save these t
    #im = Image.open(myImg); im.show()



    # print(f"{key}: {value}")


if __name__ == '__main__':
    # Read the properties -> their in game UUID (so we can query our API for their data)
    with open(jsonFile, 'r') as jf:
        data = dict(json.load(jf))

    # ensure ipfsLinks exist
    if not os.path.isfile(ipfsLinkFile):
        print("Follow the readme.md steps! You need to upload the images first")
        exit(1)
    with open(ipfsLinkFile, 'r') as jf:
        links = dict(json.load(jf)) # 0001 = ipfs.io/ipfs/HASH

    main()