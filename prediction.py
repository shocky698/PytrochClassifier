import torch
import numpy as np
from torchvision.transforms import transforms
from PIL import Image, ImageFont, ImageDraw
#from cnn_main import CNNet
from pathlib import Path
#from imageio import imread
import imageio as im
import matplotlib.pyplot as plt
from parameters import MODEL_NAME

classifier = torch.load('models/{}.pt'.format(MODEL_NAME)).eval()

# getting the input of the letter

trans = transforms.Compose([
    #transforms.RandomHorizontalFlip(),
    #transforms.Resize(32),
   # transforms.CenterCrop(32),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    #transforms.Normalize((0.5, 0.5, 0.5),(0.5, 0.5, 0.5))
    ])

image = Image.open(Path('/Users/user/Desktop/Classifier/PyTorchImageClassifier/Dataset/Target/Set/img034-01038.png'))

input = trans(image)


#output_pic = transforms.ToPILImage(input)

#plt.imshow(np.real(output_pic))
#plt.show()

input = input.view(1,1, 64, 64).float()
print(input)

output = classifier(input)



prediction = int(torch.max(output.data, 1)[1].numpy())
print("The predicted Class is  " + str(prediction))


