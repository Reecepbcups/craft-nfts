# craft-nft-poc

TODO: image compression?

MAIN.py has the main logic for how NFTs can be done including:
- get NFTs from stargaze
- PLUGIN: download each IPFS to memory (image byte array when placing w/ map)
- Save to mongoDB collection as {address, {name_of_nft, IPFSLink}}