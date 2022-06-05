### Steps

### MAKE SURE WE COMPRESS IMAGES -> JPG & COMPRESS QUALITY BEFORE SENDING TO IPFS. + ALSO REMOVE META/EXISF DATA.
### Need to use py script

Needed:
- When making a property, have a list of set broad types (Home, Business, Apartment, etc.)
- When creating a property and it is all setup, return the uuid in an easy to click format to copy paste (in game plugin)
(Maybe we could return the format which is in info.json ! just ensure there is a , at the end)

Setup:
- setup the real estate in game including all the keys, maybe we base64 encode this? but then again may not be a good idea.
- Take screenshots of the real estate, edit the filename = the token name. Ex: 0001.png.
- Set the string name with a key of the UUID of this property (Will will query the API for all our needs)


1) Upload files to the link (ipfs) in upload.py
- Get the return value from the right, and copy paste to the returnOutput variable exactly
- Run the script, it will dump the filename->ipfs link as file ipfs_links.json.
(This way we can add the correct image -> the correct NFT)

2) Next we need to mint the nft tokens from the onft collection.
- Open the mint.py file.
- Ensure we remove any keys from the API which is not used in the NFT data via removeWebappAPIThings
- edit the values at the top to our desired
- run it for all NFTs for that collection








### How to make an ONFT
```bash
# https://github.com/OmniFlix/onft
# https://rpc.flixnet-4.omniflix.network/  ,  https://rest.flixnet-4.omniflix.network/

export NODE="https://rpc.flixnet-4.omniflix.network:443"

# fresh mnemonic only for testing. Tokens given from omniflix discord bot testnets
# sugar matrix make enough anxiety crazy birth forget adjust market few abuse spider town neither dice history bamboo prize fruit sell pupil online scare
# omniflixhubd keys add reece --recover     ===>   omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh

# creates denom craftre1 with a collection name of craft_re_1
# https://json-schema.org/learn/miscellaneous-examples.html
# https://www.liquid-technologies.com/online-json-to-schema-converter <<< Useful to copy paste our desired string -> a schema (make sure to run it through removeWebappAPIThings since some values are not required)>>>
# https://codebeautify.org/jsonminifier << Then remove all the whitespace >>
omniflixhubd tx onft create craftre2 --name craft_re_1 --description="The Craft Real Estate Test #1 Collection of XXXX properties" --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" --schema='{"$schema":"http://json-schema.org/draft-04/schema#","type":"object","properties":{"name":{"type":"string"},"type":{"type":"string"},"description":{"type":"string"},"floorArea":{"type":"integer"},"volume":{"type":"integer"},"location":{"type":"object","properties":{"city":{"type":"object","properties":{"uuid":{"type":"string"},"name":{"type":"string"}},"required":["uuid","name"]},"building":{"type":"object","properties":{"uuid":{"type":"string"},"name":{"type":"string"}},"required":["uuid","name"]},"coordinates":{"type":"object","properties":{"x":{"type":"integer"},"y":{"type":"integer"},"z":{"type":"integer"}},"required":["x","y","z"]}},"required":["city","building","coordinates"]}},"required":["name","type","description","floorArea","volume","location"]}' --chain-id flixnet-4  --fees 200uflix --from reece
# omniflixhubd q tx 3E45CB1E0024A3D4EF7B55F551271F177A419720E7454E20FAACE8D78D3E53AA   
# ^^ Then get the onftdenom: onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b

# THis will be done via the mint.py script
omniflixhubd tx onft mint onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b \
    --name="{PROPERTY_NAME}" \    
    --media-uri="{IPFS_IMAGE_LINK}" \
    --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" \
    --data="{RETURNED_API_JSON_VALUES}" \
    --chain-id flixnet-4 --fees 200uflix --from reece

# omniflixhubd q tx AEE050057EAD3EF2D1CE92ABCED615E17C256EA8D505EFF63FD162ED31164FA9

omniflixhubd query onft denom onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/collections/onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b" -H  "accept: application/json"

omniflixhubd q onft supply onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b" -H  "accept: application/json"

omniflixhubd q onft collection onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b/onfts/onft12eef7f93436412080409b4c3ca73153" -H  "accept: application/json"
# The ID given after /onfts/:id is found with the collections endpoint '  curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/collections/onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b" -H  "accept: application/json"  '


# Get supply an owner owns
omniflixhubd q onft owner omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh --denom-id=onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b # --denom-id is optional
curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/onfts/onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b/omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh" -H  "accept: application/json"

# Get specific onft values from denom
omniflixhubd q onft asset onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b onft053ed17228c14d33b9f3bb7cd7b89622
curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenom23c8ecb9a9e2484ebfc7c4847e65f15b/onfts/onft053ed17228c14d33b9f3bb7cd7b89622" -H  "accept: application/json"
```
