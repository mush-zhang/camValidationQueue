from retrieve_img_from_stream import *
from PIL import Image


def get_resolution(page_url):

    imageName = 'img'
    getImages_from_stream(page_url, '1', '1', imageName)
    imagePath = "Outputs/" + imageName + "%d.jpg"
    im = Image.open(imagePath)
    width, height = im.size  # width and height

    resolution = {'width': width, 'height': height}

    return resolution
