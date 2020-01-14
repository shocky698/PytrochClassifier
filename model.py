import torch.nn as nn
import torch
import torch.nn.functional as F


# All torch models have to inherit from the Module class
class Model(torch.nn.Module):

	def __init__(self):
		super(Model, self).__init__()
		self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
		self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
		self.conv2_drop = nn.Dropout2d()
		self.conv3 = nn.Conv2d(20, 30, kernel_size=5)
		self.conv3_drop = nn.Dropout2d()
		# self.conv4 = nn.Conv2d(30, 40, kernel_size=4)
		# self.conv4_drop = nn.Dropout2d()
		self.fc1 = nn.Linear(30*4*4, 100)  # 20*13*13
		self.fc2 = nn.Linear(100, 80)
		self.fc3 = nn.Linear(80, 50)
		self.fc4 = nn.Linear(50, 26)

	def forward(self, x):
		x = F.relu(F.max_pool2d(self.conv1(x), 2))
		x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
		x = F.relu(F.max_pool2d(self.conv3_drop(self.conv3(x)), 2))
		# x = F.relu(F.max_pool2d(self.conv4_drop(self.conv4(x)), 2))

		# Reshaping the tensor to BATCH_SIZE x 320. Torch infers this from other dimensions when one of the parameter is -1.
		#print(x.shape)
		x = x.view(-1, 30*4*4)  # 20*13*13 #30*4*4
		#print(x.size())
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		x = F.dropout(x)
		x = F.relu(self.fc3(x))
		x = F.dropout(x)
		x = self.fc4(x)
		return x