Is done when creating the collection, we dont need atm

# EXAMPLE: https://json-schema.org/learn/miscellaneous-examples.html
# https://www.liquid-technologies.com/online-json-to-schema-converter <<< Useful to copy paste our desired string -> a schema (make sure to run it through removeWebappAPIThings since some values are not required)>>>
# https://codebeautify.org/jsonminifier << Then remove all the whitespace >>
omniflixhubd tx onft create craftre3 --name craft_re_1 --description="The Craft Real Estate Test #2 Collection of XXXX properties" --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" --schema='{"$schema":"http://json-schema.org/draft-04/schema#","type":"object","properties":{"name":{"type":"string"},"type":{"type":"string"},"description":{"type":"string"},"floorArea":{"type":"integer"},"volume":{"type":"integer"},"location":{"type":"object","properties":{"city":{"type":"object","properties":{"uuid":{"type":"string"},"name":{"type":"string"}},"required":["uuid","name"]},"building":{"type":"object","properties":{"uuid":{"type":"string"},"name":{"type":"string"}},"required":["uuid","name"]},"coordinates":{"type":"object","properties":{"x":{"type":"integer"},"y":{"type":"integer"},"z":{"type":"integer"}},"required":["x","y","z"]}},"required":["city","building","coordinates"]}},"required":["name","type","description","floorArea","volume","location"]}' --chain-id flixnet-4  --fees 200uflix --from reece





# THis will be done via the mint.py script (Just template example here)
omniflixhubd tx onft mint onftdenome307136eed384681ab981e6aedbcad5c \
    --name="{PROPERTY_NAME}" \    
    --media-uri="{IPFS_IMAGE_LINK}" \
    --preview-uri="https://pbs.twimg.com/profile_images/1530715122770931712/79qwdB0R_400x400.jpg" \
    --data="{RETURNED_API_JSON_VALUES}" \
    --chain-id flixnet-4 --fees 200uflix --from reece
# omniflixhubd q tx AEE050057EAD3EF2D1CE92ABCED615E17C256EA8D505EFF63FD162ED31164FA9