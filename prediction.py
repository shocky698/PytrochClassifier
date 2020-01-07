import numpy as np
import torch
from torch.utils.data import DataLoader
from dataloader import notMNIST
import os
from parameters import MODEL_NAME
from torchvision import  datasets, transforms, models
from PIL import Image
from torch.autograd import Variable
from torchnet.logger import meterlogger
import matplotlib as plt

path = "/Users/user/Desktop/Classifier/PyTorchImageClassifier/Dataset/Target" #os.path.join(os.path.dirname(__file__), 'Dataset/Target')
#test_dataset = notMNIST(path)
#test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)
#classifier = torch.load('models/{}.pt'.format(MODEL_NAME)).eval()
#correct = 0

test_transforms = transforms.Compose([transforms.Resize(224,224),
                                      transforms.ToTensor(),
                                      #transforms.Normalize([0.485, 0.456, 0.406],
                                      #                     [0.229, 0.224, 0.225])
                                     ])

model = torch.load('models/{}.pt'.format(MODEL_NAME)).eval()

def predict_image(image):
    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input = Variable(image_tensor)
    output = model(input)
    index = output.data.cpu().numpy().argmax()
    return index

def get_random_images(num):
    data = datasets.ImageFolder(path, transform=test_transforms)
    #classes = data.classes
    indices = list(range(len(data)))
    np.random.shuffle(indices)
    idx = indices[:num]
    from torch.utils.data.sampler import SubsetRandomSampler
    sampler = SubsetRandomSampler(idx)
    loader = torch.utils.data.DataLoader(data, sampler=sampler, batch_size=num)
    dataiter = iter(loader)
    images, labels = dataiter.next()
    return images, labels

to_pil = transforms.ToPILImage()
images, labels = get_random_images(2)
fig=plt.figure(figsize=(10,10))
for ii in range(len(images)):
    image = to_pil(images[ii])
    index = predict_image(image)
    sub = fig.add_subplot(1, len(images), ii+1)
    res = int(labels[ii]) == index
    #sub.set_title(str(classes[index]) + ":" + str(res))
    plt.axis('off')
    plt.imshow(image)
plt.show()

#for _, data in enumerate(test_loader, 0):
#	test_x, test_y = data
#	pred = classifier.forward(test_x)
#	y_hat = np.argmax(pred.data)
##		print(y_hat)