from pymongo import MongoClient
from PIL import Image
import io

client = MongoClient("mongodb://root:akashmongodb19pass@782sk60c31ell6dbee3ntqc9lo.ingress.provider-2.prod.ewr1.akash.pub:31543/?authSource=admin")
db = client.reece
images = db.images

QUALITY = 33


def save(wallet, name, imageLoc):
    im = Image.open(imageLoc)
    image_bytes = io.BytesIO()
    im.save(image_bytes, format='JPEG')
    image = {
        'address': wallet,
        "name": name,
        'data': image_bytes.getvalue()
    }
    image_id = images.insert_one(image).inserted_id
    print('image saved', image_id)

def read(**kwargs):
    import matplotlib.pyplot as plt # python3 -m pip install matplotlib
    # filter={'address': address, 'name': name}
    filter={**kwargs}
    image = images.find_one(filter=filter)
    pil_img = Image.open(io.BytesIO(image['data']))
    plt.imshow(pil_img)
    plt.show()

# save("stars1j42087twdvkmkdqfedg0gq2c6wnp7ycdayllx4", "Bad_Kid_#5885", "./stars1j42087twdvkmkdqfedg0gq2c6wnp7ycdayllx4_Bad_Kid_#5885.jpg")
# save("stars1j42087twdvkmkdqfedg0gq2c6wnp7ycdayllx4", "Bad_Kid_#5885", "./5885.jpg")

# fun to get all names you own?
read("stars1j42087twdvkmkdqfedg0gq2c6wnp7ycdayllx4", "Bad_Kid_#5885")



def stripEXIFDataFromImage(imageLoc):
    from PIL import Image
    image = Image.open(imageLoc)
    # next 3 lines strip exif
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(imageLoc,optimize=True,quality=QUALITY)

# stripEXIFDataFromImage("stars1j42087twdvkmkdqfedg0gq2c6wnp7ycdayllx4_Bad_Kid_#5885.jpg")
# stripEXIFDataFromImage("5885.jpg")