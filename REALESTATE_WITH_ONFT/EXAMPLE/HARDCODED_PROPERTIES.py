# This here is a hardcoded return value of some properties.
# This would be from the crafteconomy.reProperties mongo collection in the future

PROPERTY_MONGODB_EXAMPLE = {
    "ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2": {
        "name": "Property 1",
        "uuid": "ee53f5d3-63fc-4ea3-ab9b-6981ad14f6a2", # The properties ID, we need this in the request to save NFTs
        "type": "House",
        "description": "This is a house",
        "floorArea": 25,
        "volume": 100,
        "block_restrictions": { # Is this final for a property? maybe we just save the NAME of the restriction if so to IPFS.
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
        "state": "OWNED",  # WEBAPP USE ONLY
        "current_renter": {   # WEBAPP USE ONLY
            "uuid": "79da3753-1b9e-4340-8a0f-9ea975c17fe4",
            "username": "Reecepbcups",
        },
        "property_owner": {   # WEBAPP USE ONLY
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
    "dbcd78cb-326e-4842-982b-9252f9ca25a7": {
        "name": "Mansion",
        "uuid": "dbcd78cb-326e-4842-982b-9252f9ca25a7", 
        "type": "Home",
        "description": "This is a pretty mansion",
        "floorArea": 1800,
        "volume": 26000,
        "block_restrictions": {},
        "location": {
            "city": {
                "uuid": "a71f5e33-5fa9-4de9-852a-dbed20b0be3a",
                "name": "craftcity",
            },
            "building": {
                "uuid": "4730b411-c94c-467a-8792-6f4696b180be",
                "name": "Mansion",
            },
            "coordinates": {"x": 500, "y": 60, "z": 500},
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
