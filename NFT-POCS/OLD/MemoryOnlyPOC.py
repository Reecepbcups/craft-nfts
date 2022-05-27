'''
read to memory, not use any files
'''
import os, sys
import requests # httpx in future so async
from PIL import Image
import io
import matplotlib.pyplot as plt
from pymongo import MongoClient

# 'MultiScape Aztec Night L1 3427': 'https://ipfs.stargaze.zone/ipfs/QmSdiEvG4Xh7YxE7yQSH7UMHdGL8YRVMCZ3VyFxn4oYkcA/Aztec_Night_L1_3.png', 
# 'Stargaze Punks #1226': 'https://ipfs.stargaze.zone/ipfs/bafybeicvvfnlxuo3ineufnwqcjvwvo64dkazv5an4lclrymb77fmnga2ze/images/1226.png', 
# 'JunoNots #129': 'https://ipfs.stargaze.zone/ipfs/QmU7U2ULGMj1ZmzLTLUnpFYXonCnZnH2ZUNdeGKXmxAxTQ/89.png', 
# 'IBC Frens #637': 'https://ipfs.stargaze.zone/ipfs/bafybeiaip3vwwhhgerw6gcs66clj4onubkdadquqzzpzrftvuyhgnzojse/images/637.jpg'

def main():
    # nftImage = "https://ipfs.stargaze.zone/ipfs/bafybeiaip3vwwhhgerw6gcs66clj4onubkdadquqzzpzrftvuyhgnzojse/images/637.jpg"
    nftImage = "https://ipfs.stargaze.zone/ipfs/QmU7U2ULGMj1ZmzLTLUnpFYXonCnZnH2ZUNdeGKXmxAxTQ/89.png"
    imageObj = downloadImage(nftImage) # <class '_io.BytesIO'>
    # img.show()
    print(type(imageObj))

    stripEXIFDataFromImage(imageObj)

    # img_bytes = img.tobytes()
    # print(img_bytes)
    imageObject = bytesToImage(img_bytes)    
    print(type(imageObject))
    

def stripEXIFDataFromImage(image_data):
    from PIL import Image
    QUALITY = 33
    image = Image.open(imageToBytes(image_data))
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save("test.png", optimize=True,quality=QUALITY)

def viewImgFromBytes(img_bytes):
    pass

def downloadImage(link) -> Image:
    data = requests.get(link).content
    # with open(f"{CURRENT_DIR}/{output_name}", "wb") as f:
    #     f.write(data)
    image_bytes = io.BytesIO(data)
    return Image.open(image_bytes)

def imageToBytes(image) -> io.BytesIO:    
    return io.BytesIO(image)

def saveByteImageToFile(img_bytes, filename):
    image = Image.open(img_bytes)

def bytesToImage(img_bytes):
    import matplotlib.pyplot as plt # python3 -m pip install matplotlib
    # filter={'address': address, 'name': name}
    # image = images.find_one(filter=filter)
    pil_img = Image.open(img_bytes)
    pil_img.show()
    # plt.imshow(pil_img.tobytes())
    # plt.show()
    return pil_img

if __name__ == "__main__":
    main()