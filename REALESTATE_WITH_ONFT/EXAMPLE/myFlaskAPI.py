"""
https://github.com/Reecepbcups/craft-nfts/blob/master/ROUGH-ONFT-IMPLIMENTATION/mint.py/

This file will contain a hardcoded real estate API
- We will port this over to the TS CRAFT root API.

Goal:
- GET dat about properties based on their name
- GET middleware to our NFT module query endpoints
"""
import flask
from flask import request, jsonify
from typing import TypeVar, Type

# curl --header "Content-Type: application/json" --request POST --data '{"username":"xyz","password":"xyz"}' http://localhost:5000/tx

PRODUCTION, HOST, PORT = False, "0.0.0.0", 5000
ONFT_COLLECTION = "onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b"
MY_WALLET = ""

app = flask.Flask(__name__)

# used for / endpoint
ROOT_ENDPOINTS = {
    "/": "Root endpoint",
    "/info?uuid=": "Get a properties info from our DB",
    "/onft?address=": "Get all owned properties from onft module query",
}


@app.route("/", methods=["GET"])
def home():
    return jsonify(ROOT_ENDPOINTS)


PROPERTY_MONGODB_EXAMPLE = {
    "ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2": {
        "name": "Property 1",
        "uuid": "ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2",
        "type": "House",
        "description": "This is a house",
        "floorArea": 25,
        "volume": 100,
        "block_restrictions": {
            # Is this final for a property? maybe we just save the NAME of the restriction if so to IPFS.
            "CHEST": 5,
            "FURNACE": 5,
        },
        "location": {
            "city": {
                "uuid": "a71f5e33-5fa9-4de9-852a-dbed20b0be3a",
                "name": "craftcity",
            },
            "building": {
                "uuid": "ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2",
                "name": "Building1",
            },
            "coordinates": {"x": 0, "y": 0, "z": 0},
        },
        "state": "OWNED",  # WEBAPP ONLY
        "current_renter": {  # WEBAPP ONLY
            "uuid": "79da3753-1b9e-4340-8a0f-9ea975c17fe4",
            "username": "Reecepbcups",
        },
        "property_owner": {  # WEBAPP ONLY
            "uuid": "805a4070-2d4f-442e-9c7b-9194d1252325",
            "username": "Tesla_Stock",
        },
    },
    "f6ebbe2d-f5ca-4756-8d0c-b5973c0d0006": {
        "name": "Property 2",
        "uuid": "f6ebbe2d-f5ca-4756-8d0c-b5973c0d0006",
        "type": "Business",
        "description": "This is a business",
        "floorArea": 50,
        "volume": 500,
        "block_restrictions": {
            # Is this final for a property? maybe we just save the NAME of the restriction if so to IPFS
            # none for the business
            "CHEST": 5,
            "FURNACE": 5,
        },
        "location": {
            "city": {
                "uuid": "a71f5e33-5fa9-4de9-852a-dbed20b0be3a",
                "name": "craftcity",
            },
            "building": {
                "uuid": "892f8bb6-df50-49dd-b06a-93b9de72e27e",
                "name": "Building2",
            },
            "coordinates": {"x": 100, "y": 100, "z": 100},
        },
        "state": "RENTED",  # WEBAPP ONLY
        "current_renter": {  # WEBAPP ONLY
            "uuid": "79da3753-1b9e-4340-8a0f-9ea975c17fe4",
            "username": "Reecepbcups",
        },
        "property_owner": {  # WEBAPP ONLY
            "uuid": "805a4070-2d4f-442e-9c7b-9194d1252325",
            "username": "Tesla_Stock",
        },
    },
}


@app.route("/info", methods=["GET"])
def getProperty():
    '''
    http://127.0.0.1:5000/info?uuid=ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2
    http://127.0.0.1:5000/info?uuid=f6ebbe2d-f5ca-4756-8d0c-b5973c0d0006
    '''
    # PINGs against our database
    if len(request.args) == 0:
        return jsonify("error", "No arguments provided", 400)

    # http://127.0.0.1:5000/users?uuid=9d891348-0f18-4683-a338-64113e224547
    id = _getRequestValue(str, "uuid", request.args)

    return jsonify(PROPERTY_MONGODB_EXAMPLE.get(id, {}))

import requests, json, ast

@app.route("/onft", methods=["GET"])
def getOwnedNFTs():
    '''
    http://127.0.0.1:5000/onft?address=omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh
    '''
    wallet = _getRequestValue(str, "address", request.args)
    api = f"https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/onfts/{ONFT_COLLECTION}/{wallet}"
    
    myNFTs = requests.get(api).json()
    if len(myNFTs) == 0:
        return jsonify("error", "No NFTs found", 404)

    myProperties = {}
    myNFTs = myNFTs['collections'][0]['onfts']
    for nft in myNFTs:
        name = nft['metadata']['name']
        data = json.dumps(ast.literal_eval(nft['data']))
        print(data)
        # myProperties[name] = data


    return jsonify(myProperties)

    

# @app.route("/tx", methods=["POST"]) -> input_json = request.get_json(force=True)





T = TypeVar("T", str, float, int, dict)
def _getRequestValue(t: Type[T], key, args) -> T:
    """
    Takes in a type, the key, and the args immutable dict.
    Returns the value of the key if it exists and is of the correct type.
    """
    value = args.get(key, None)
    return None if value is None else t(value)


if __name__ == "__main__":

    output = f"Running on http://{HOST}:{PORT}"

    if PRODUCTION:  # waitress
        from waitress import serve

        print("Production", output)
        serve(app, host=HOST, port=PORT)
    else:
        print("Development", output)
        app.run(debug=True, port=PORT)


# import requests
# res = requests.post('http://127.0.0.1:5000/api/add_message/1234', json={"mytext":"lalala"})
# if res.ok:
#     print(res.json())
