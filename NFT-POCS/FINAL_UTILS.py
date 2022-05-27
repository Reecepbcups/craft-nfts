import bech32
def convertBech32WalletToNew(address, prefix="craft") -> str:
    '''
    Converts a coin 118 address to any other bech32 coin 118 address.
    '''
    _, data = bech32.bech32_decode(address)
    return bech32.bech32_encode(prefix, data)


import requests
from PIL import Image
import io
def downloadImageToMemoryAndShow(link, show=False) -> Image:    
    data = requests.get(link).content

    image = Image.open(io.BytesIO(data))
    # ! check data is an instance of png, jpg, jpeg, try except

    # check if image is a video
    if show: 
        print("Showing image...")
        image.show()
    return image



# converts PNG -> JPEG (RGB) & saves it to disk.
# Likely not needed, only using for debugging
def saveImageToDrive(image: Image, outputFile: str, quality: int = 100):
    img = image.convert('RGB')
    img.save(outputFile, optimize=True, format='JPEG', quality=quality)