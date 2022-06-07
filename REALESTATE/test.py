data = "{'name': 'Property 2', 'type': 'Business', 'description': 'This is a business', 'floorArea': 50, 'volume': 500, 'location': {'city': {'uuid': 'a71f5e33-5fa9-4de9-852a-dbed20b0be3a', 'name': 'craftcity'}, 'building': {'uuid': '892f8bb6-df50-49dd-b06a-93b9de72e27e', 'name': 'Building2'}, 'coordinates': {'x': 100, 'y': 100, 'z': 100}}, 'property_owner': {'uuid': '805a4070-2d4f-442e-9c7b-9194d1252325', 'username': 'Tesla_Stock'}}"

# print(data)

import json, ast

# data = 

# convert data string into JSON object
data = json.dumps(ast.literal_eval(data))

print(data)
