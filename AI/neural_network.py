import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from matplotlib.pyplot import imshow
import os
import PIL
import numpy as np
from matplotlib.pyplot import imshow

def to_negative(img):
    img = PIL.ImageOps.invert(img)
    return img

class Negative(object):
    def __init__(self):
        pass
    
    def __call__(self, img):
        return to_negative(img)
       
transform = transforms.Compose([Negative(), transforms.ToTensor()])
train_set = torchvision.datasets.ImageFolder(root='train', transform=transform)
classes = ("pepper", "potato", "strawberry", "tomato")

BATCH_SIZE = 4
train_loader = torch.utils.data.DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1), #3 channels to 32 channels
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # output: 64 channels x 50 x 50 image size - decrease

            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1), #increase power of model 
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # output: 128 x 25 x 25

            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(5, 5), # output: 256 x 5 x 5

            nn.Flatten(), #a single vector 256*5*5,
            nn.Linear(256*5*5, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 4))
        
    def forward(self, xb):
        return self.network(xb)
 
def training_network():
    net = Net()
    net = net.to(device)
 
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
 
    for epoch in range(10):
        running_loss = 0.0
        for i, data in enumerate(train_loader, 0):
            inputs, labels = data[0].to(device), data[1].to(device)
            optimizer.zero_grad()
            outputs = net(inputs.to(device))
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
 
            running_loss += loss.item()
            if i % 200 == 199:
                print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss))
                running_loss = 0.0
 
    print("Finished training")
    save_network_to_file(net)
 
 
def result_from_network(net, loaded_image):
    image = PIL.Image.open(loaded_image)
    pil_to_tensor = transforms.Compose([Negative(), transforms.ToTensor()])(image.convert("RGB")).unsqueeze_(0)
    outputs = net(pil_to_tensor)
 
    return classes[torch.max(outputs, 1)[1]]
 
 
def save_network_to_file(network):
    torch.save(network.state_dict(), 'network_model.pth')
    print("Network saved to file")
 
 
def load_network_from_structure(network):
    network.load_state_dict(torch.load('network_model.pth'))
 
 
if __name__ == "__main__":
    print(torch.cuda.is_available())
    training_network()