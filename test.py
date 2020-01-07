import numpy as np
import torch
from torch.utils.data import DataLoader
from dataloader import notMNIST
import os
from parameters import MODEL_NAME
from matplotlib import pyplot as plt

path = os.path.join(os.path.dirname(__file__), 'Dataset/Test')
test_dataset = notMNIST(path)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=True)
classifier = torch.load('models/{}.pt'.format(MODEL_NAME)).eval()
correct = 0



for _, data in enumerate(test_loader, 0):
	test_x, test_y = data
	print(test_x)
	pred = classifier.forward(test_x)
	y_hat = np.argmax(pred.data)
	#print(y_hat)
	if y_hat == test_y:
		correct += 1
		#print(y_hat)

#print(test_dataset[0])
#image = test_dataset[0]
#image = np.array(image)
#pixels = image.reshape((28,28))
#plt.imshow(image, cmap='gray')
#plt.show()
print("Accuracy={}".format(correct / len(test_dataset)))

#y_hat = classifier(test_x[0])

#pred1 = classifier.forward(test_x[0])
#y_hat1 = np.argmax(pred1.data)
#print(y_hat1)

