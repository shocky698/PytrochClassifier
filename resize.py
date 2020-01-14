from PIL import Image, ImageDraw, ImageFont,ImageOps
from torchvision.transforms import transforms
from matplotlib.pyplot import plot as plt
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

from scipy import ndimage, misc
import numpy as np
import os
#import cv2

def main():
    outPath = "/Users/user/Desktop/Data/Z"
    path = "/Users/user/Desktop/Thesis_Mixed/Alphabets/English2/Fnt/Sample036"

    # iterate through the names of contents of the folder
    for image_path in os.listdir(path):

        # create the full input path and read the file
        input_path = os.path.join(path, image_path)
        image = Image.open(input_path)

        # rotate the image
        #rotated = ndimage.rotate(image_to_rotate, 45)

        trans = transforms.Compose([
            # transforms.RandomHorizontalFlip(),
             transforms.Resize(64),
            transforms.Grayscale(num_output_channels=1)
            # transforms.CenterCrop(32),
            #transforms.ToTensor(),
            # transforms.Normalize((0.5, 0.5, 0.5),(0.5, 0.5, 0.5))
        ])
        #image = Image.open(image_to_resize)

        transimage = trans(image)

        # create full output path, 'example.jpg'
        # becomes 'rotate_example.jpg', save the file to disk
        fullpath = os.path.join(outPath,"" +image_path)
        transimage.save(fullpath)

if __name__ == '__main__':
    main()
