from os.path import dirname as parentDir
import json
from PIL import Image
import time

thisFolder = parentDir(__file__)
jsonFile = f"{thisFolder}/info.json"

with open(jsonFile, 'r') as jf:
    data = dict(json.load(jf))


for key, value in data.items():
    nftID = str(key)
    if nftID.startswith("IGNORE"):
        continue

    image = f"{thisFolder}/screenshots/{nftID}.png" # path/0001.png
    reType = data[nftID]['type']    
    uuid = data[nftID]['id']
    # location = getThisFromRESTAPI based on the property uuid
    # size = data[nftID]['size'] #>> can we easily get this from the restAPI when made? or do we have to manually find this for each property


    # TODO MAKE SURE WE COMPRESS IMAGES -> JPG & COMPRESS QUALITY BEFORE SENDING TO IPFS. + ALSO REMOVE META DATA
    print(f"CRAFT RealEstate #{nftID}: {reType=}, {uuid=}, {image=}")

    # We can only view 1 image at a time, would have to save these t
    #im = Image.open(myImg); im.show()



    # print(f"{key}: {value}")