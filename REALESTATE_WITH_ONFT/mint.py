from os.path import dirname as parentDir
import json
from PIL import Image
import time
import os
import requests
'''
Steps to mint
1) Ensure the flask api / normal API is running with the data we need from our MongoDB
2) call http://127.0.0.1:5000/getFirst & save this JSON schema (LATER, FOR BETA NOT NOW)

3) Ensure top variables are correct to our liking. 



'''

OUR_NFT_DENOM = "onftdenom612ffc6aac614402b3d45a6b6a5caff7"
prefixName = "CRE2 #"
TX_SUFFIX = "--chain-id flixnet-4 --fees 200uflix --from reece --yes"
# ourPreviewImage = "https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" # I assume we use the property as the preview image??

# Keys we block from going in the ONFT (Since they are in game, and not NFT attrributes)
KEYS_WE_DONT_NEED_IN_THE_NFT = ["block_restrictions", "current_renter", "current_owner", "state"]


# ----------------------------------------------------------------------------------------------------------------------

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

        jsonObj = requests.get(f"http://127.0.0.1:5000/info?uuid={reUUID}").json()
        jsonObj = removeWebappUneededKeys(jsonObj)
        # print(jsonObj)
        mintNFT(nftID, jsonObj)

def mintNFT(nftNumber: int = 0000, JSONData: dict = {}):
    # WHAT IF WE BASE64 ENCODE THE JSON DATA? json.loads(base64.b64decode(myStr).decode('UTF-8'))
    IPFS_IMAGE_LINK = links[nftNumber]
    # Example value this returns:  (( omniflixhubd q tx AEE050057EAD3EF2D1CE92ABCED615E17C256EA8D505EFF63FD162ED31164FA9  ))
    # omniflixhubd tx onft mint {OUR_NFT_DENOM} --name="TestRE #0001" --media-uri="https://ipfs.io/ipfs/QmXozTQYxsR5gz18gdhwtCNV37jiQgtuR9n9nMTpSRM1jq" --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" --data="{'name': 'Property 1', 'type': 'House', 'description': 'This is a house', 'floorArea': 25, 'volume': 100, 'location': {'city': {'uuid': 'a71f5e33-5fa9-4de9-852a-dbed20b0be3a', 'name': 'craftcity'}, 'building': {'uuid': 'ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2', 'name': 'Building1'}, 'coordinates': {'x': 0, 'y': 0, 'z': 0}}, 'property_owner': {'uuid': '805a4070-2d4f-442e-9c7b-9194d1252325', 'username': 'Tesla_Stock'}}" --chain-id flixnet-4 --fees 200uflix --from reece

    JSONData = json.dumps(JSONData) # makes things double quoted
    # print(JSONData)

    # For now preview-uri is the same as media uri
    output = f"""omniflixhubd tx onft mint {OUR_NFT_DENOM} --name="{prefixName}{nftNumber}" --description="Craft Economy Real Estate Testing" --media-uri="{IPFS_IMAGE_LINK}" --preview-uri="{IPFS_IMAGE_LINK}" --data='{JSONData}' {TX_SUFFIX}"""
    print(output + "\n")

def removeWebappUneededKeys(JSONObject: dict) -> dict:
    # remove keys from the JSONObject that are not needed for the webapp.
    # These keys are just for the marketplace
    for s in KEYS_WE_DONT_NEED_IN_THE_NFT:
        JSONObject.pop(s, None)    
    return JSONObject




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