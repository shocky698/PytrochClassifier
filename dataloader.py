import os
import numpy as np
import torch
from PIL import Image
from torch.utils.data.dataset import Dataset
from torchvision.transforms import transforms
from imageio import imread
from torch import Tensor

"""
Loads the train/test set. 
Every image in the dataset is 32x32 pixels and the labels are numbered from 0-25
for A-Z respectively.

Set root to point to the Train/Test folders.
"""

# Creating a sub class of torch.utils.data.dataset.Dataset
class notMNIST(Dataset):

	# The init method is called when this class will be instantiated.
	def __init__(self, root):
		Images, Y = [], []
		folders = os.listdir(root)

		for folder in folders:
			folder_path = os.path.join(root, folder)
			for ims in os.listdir(folder_path):
				try:
					img_path = os.path.join(folder_path, ims)
					Images.append(np.array(imread(img_path)))
					Y.append(ord(folder) - 65)  # Folders are A-Z so labels will be 0-25
					#print(max(Y))
				except:
					# Some images in the dataset are damaged
					print("File {}/{} is broken".format(folder, ims))
		data = [(x, y) for x, y in zip(Images, Y)]
		self.data = data

	# The number of items in the dataset
	def __len__(self):
		return len(self.data)

	# The Dataloader is a generator that repeatedly calls the getitem method.
	# getitem is supposed to return (X, Y) for the specified index.
	def __getitem__(self, index):
		img = self.data[index][0]

		# 8 bit images. Scale between [0,1]. This helps speed up our training
		#img = img.resize((28,28))
		#img = img.reshape(128, 128)
		#print(img.shape)

		img = img.reshape(64, 64) / 255.0

		#print(img.shape)

		# Input for Conv2D should be Channels x Height x Width
		img_tensor = Tensor(img).view(1, 64, 64).float()
		label = self.data[index][1]
		#print(img_tensor)
		return (img_tensor, label)
