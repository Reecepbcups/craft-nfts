import json
from os.path import dirname as parentDir

# Upload IPFS Images, then grab with https://ipfs.io/ipfs/HASH  (In the future use our own IPFS server)
# https://anarkrypto.github.io/upload-files-to-ipfs-from-browser-panel/public/
# this returns:
returnOutput = [{
    "path": "0002.png",
    "hash": "QmbzzUfyQ31rsDnPtg27FZGEcyHMGZyvwNsyd1VanAQdXz",
    "size": 2508511
  },
  {
    "path": "0001.png",
    "hash": "QmXozTQYxsR5gz18gdhwtCNV37jiQgtuR9n9nMTpSRM1jq",
    "size": 2719570
  }]


'''
0002.png: https://ipfs.io/ipfs/QmbzzUfyQ31rsDnPtg27FZGEcyHMGZyvwNsyd1VanAQdXz
0001.png: https://ipfs.io/ipfs/QmXozTQYxsR5gz18gdhwtCNV37jiQgtuR9n9nMTpSRM1jq
'''

myDict = {}
for obj in returnOutput:
  newPath = obj['path'].replace(".png", "")
  myImageLink = f"https://ipfs.io/ipfs/{obj['hash']}"
  myDict[newPath] = myImageLink


# Put this into the ipfs_links.json file
filePath = parentDir(__file__) + '/ipfs_links.json'
with open(filePath, 'w') as outfile:
  json.dump(myDict, outfile)
  
print(f"Written all files name -> ipfs links to ipfs_links.json")