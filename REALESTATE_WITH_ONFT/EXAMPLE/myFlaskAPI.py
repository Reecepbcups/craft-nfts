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

from HARDCODED_PROPERTIES import PROPERTY_MONGODB_EXAMPLE

# curl --header "Content-Type: application/json" --request POST --data '{"username":"xyz","password":"xyz"}' http://localhost:5000/tx

PRODUCTION, HOST, PORT = False, "0.0.0.0", 5000
ONFT_COLLECTION = "onftdenom612ffc6aac614402b3d45a6b6a5caff7"

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



# Gets a random property from our DB (used for making a schema)
@app.route("/getFirst", methods=["GET"])
def getRandomProperty():
    '''
    http://127.0.0.1:5000/getFirst
    '''

    random_key = list(PROPERTY_MONGODB_EXAMPLE.keys())[0]
    return jsonify(PROPERTY_MONGODB_EXAMPLE.get(random_key))

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

@app.route("/owned", methods=["GET"])
def getOwnedNFTs():
    '''
    This is a middleware API to make it easier to sift through the data on the server
    http://127.0.0.1:5000/owned?address=omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh

    {
        "ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2": "CRE #0001",
        "f6ebbe2d-f5ca-4756-8d0c-b5973c0d0006": "CRE #0002"
    }
    '''
    wallet = _getRequestValue(str, "address", request.args)
    api = f"https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/onfts/{ONFT_COLLECTION}/{wallet}"
    # https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/onfts/onftdenom612ffc6aac614402b3d45a6b6a5caff7/omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh
    
    myNFTs = requests.get(api).json()
    # if len(myNFTs) == 0:
    #     return jsonify("error", "No NFTs found", 404)

    
    if 'message' in myNFTs:
        # Means the request did not work right, so we return nothing (no update)
        # Added since I test with an invalid wallet
        return {}


    myProperties = {}
    myNFTs = myNFTs['collections'][0]['onfts']

    if len(myNFTs) == 0:
        return {}

    for nft in myNFTs:
        name = nft['metadata']['name']
        data = ast.literal_eval(nft['data'])
        # print(data.keys())

        uuid = data['uuid']
        desc = data['description']
        _type = data['type']
        myProperties[uuid] = {
            "name": name,
            "description": desc,
            "type": _type,
        }

    print(myProperties)
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
