### Steps

### MAKE SURE WE COMPRESS IMAGES -> JPG & COMPRESS QUALITY BEFORE SENDING TO IPFS. + ALSO REMOVE META/EXISF DATA.
### Need to use py script

Setup:
- setup the real estate in game including all the keys.
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



## info.json
This is where we set the values of the NFTID -> In Game UUID.
We could probably just have a list of UUIDs instead and do it by enumeration?

# AUTO_GENERATED_ipfs_links.json
auto generated list matching the filename (without extension) -> ipfs link




### How to make an ONFT
```bash
# https://github.com/OmniFlix/onft
# https://rpc.flixnet-4.omniflix.network/  ,  https://rest.flixnet-4.omniflix.network/

export NODE="https://rpc.flixnet-4.omniflix.network:443"

# fresh mnemonic only for testing. Tokens given from omniflix discord bot testnets
# sugar matrix make enough anxiety crazy birth forget adjust market few abuse spider town neither dice history bamboo prize fruit sell pupil online scare
# omniflixhubd keys add reece --recover     ===>   omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh

# creates denom craftre1 with a collection name of craft_re_1 (Schema example in LATER/Schema.md)
omniflixhubd tx onft create craftre6 --name craft_re_1 --description="The Craft Real Estate Test Collection of XXXX properties" --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" --chain-id flixnet-4  --fees 200uflix --from reece
# omniflixhubd q tx 39F03DEC50EDDB3BD5694C775D8DAFDFDF40A3A7122B10A65561E75C944C503F   
# ^^ Then get the onftdenom: onftdenome307136eed384681ab981e6aedbcad5c
# ^^ Update this in mint.py, and myFlaskAPI.py
# ^ (Double click old onftdenom found below, cltr+h ->replace  the new one for the entire project)


omniflixhubd query onft denom onftdenome307136eed384681ab981e6aedbcad5c # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/collections/onftdenome307136eed384681ab981e6aedbcad5c" -H  "accept: application/json"

omniflixhubd q onft supply onftdenome307136eed384681ab981e6aedbcad5c # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenome307136eed384681ab981e6aedbcad5c" -H  "accept: application/json"

omniflixhubd q onft collection onftdenome307136eed384681ab981e6aedbcad5c # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenome307136eed384681ab981e6aedbcad5c/onfts/onft12eef7f93436412080409b4c3ca73153" -H  "accept: application/json"
# The ID given after /onfts/:id is found with the collections endpoint '  curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/collections/onftdenome307136eed384681ab981e6aedbcad5c" -H  "accept: application/json"  '


# Get supply an owner owns
omniflixhubd q onft owner omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh --denom-id=onftdenome307136eed384681ab981e6aedbcad5c # --denom-id is optional
curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/onfts/onftdenome307136eed384681ab981e6aedbcad5c/omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh" -H  "accept: application/json"

# Get specific onft values from denom
omniflixhubd q onft asset onftdenome307136eed384681ab981e6aedbcad5c onft053ed17228c14d33b9f3bb7cd7b89622
curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenome307136eed384681ab981e6aedbcad5c/onfts/onft053ed17228c14d33b9f3bb7cd7b89622" -H  "accept: application/json"
```





## New steps
1) Run the `python3 EXAMPLE/myFlaskAPI.py` in another terminal