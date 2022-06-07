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








### How to make an ONFT
```bash
# https://github.com/OmniFlix/onft
# https://rpc.flixnet-4.omniflix.network/  ,  https://rest.flixnet-4.omniflix.network/

export NODE="https://rpc.flixnet-4.omniflix.network:443"

# fresh mnemonic only for testing. Tokens given from omniflix discord bot testnets
# sugar matrix make enough anxiety crazy birth forget adjust market few abuse spider town neither dice history bamboo prize fruit sell pupil online scare
# omniflixhubd keys add reece --recover     ===>   omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh

# creates denom craftre1 with a collection name of craft_re_1 (Schema example in LATER/Schema.md)
omniflixhubd tx onft create craftre5 --name craft_re_1 --description="The Craft Real Estate Test #5 Collection of XXXX properties" --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" --chain-id flixnet-4  --fees 200uflix --from reece
# omniflixhubd q tx 00E85E35A7834701CF9CA762BFC1B648E8F5BF4008D84AD6BFDE3580CCD2309F   
# ^^ Then get the onftdenom: onftdenom612ffc6aac614402b3d45a6b6a5caff7

# THis will be done via the mint.py script
omniflixhubd tx onft mint onftdenom612ffc6aac614402b3d45a6b6a5caff7 \
    --name="{PROPERTY_NAME}" \    
    --media-uri="{IPFS_IMAGE_LINK}" \
    --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" \
    --data="{RETURNED_API_JSON_VALUES}" \
    --chain-id flixnet-4 --fees 200uflix --from reece
# omniflixhubd q tx AEE050057EAD3EF2D1CE92ABCED615E17C256EA8D505EFF63FD162ED31164FA9

omniflixhubd query onft denom onftdenom612ffc6aac614402b3d45a6b6a5caff7 # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/collections/onftdenom612ffc6aac614402b3d45a6b6a5caff7" -H  "accept: application/json"

omniflixhubd q onft supply onftdenom612ffc6aac614402b3d45a6b6a5caff7 # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenom612ffc6aac614402b3d45a6b6a5caff7" -H  "accept: application/json"

omniflixhubd q onft collection onftdenom612ffc6aac614402b3d45a6b6a5caff7 # curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenom612ffc6aac614402b3d45a6b6a5caff7/onfts/onft12eef7f93436412080409b4c3ca73153" -H  "accept: application/json"
# The ID given after /onfts/:id is found with the collections endpoint '  curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/collections/onftdenom612ffc6aac614402b3d45a6b6a5caff7" -H  "accept: application/json"  '


# Get supply an owner owns
omniflixhubd q onft owner omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh --denom-id=onftdenom612ffc6aac614402b3d45a6b6a5caff7 # --denom-id is optional
curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/onfts/onftdenom612ffc6aac614402b3d45a6b6a5caff7/omniflix13na285c3llhnfenq6hl3fh255scljcue4td9nh" -H  "accept: application/json"

# Get specific onft values from denom
omniflixhubd q onft asset onftdenom612ffc6aac614402b3d45a6b6a5caff7 onft053ed17228c14d33b9f3bb7cd7b89622
curl -X GET "https://rest.flixnet-4.omniflix.network/omniflix/onft/v1beta1/denoms/onftdenom612ffc6aac614402b3d45a6b6a5caff7/onfts/onft053ed17228c14d33b9f3bb7cd7b89622" -H  "accept: application/json"
```





## New steps
1) Run the `python3 EXAMPLE/myFlaskAPI.py` in another terminal