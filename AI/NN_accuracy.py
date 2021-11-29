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
import neural_network
from matplotlib.pyplot import imshow


# wcześniej grader.py
# Get accuracy for neural_network model 'network_model.pth'
def NN_accuracy():
    # Create the model
    net = neural_network.Net()

    # Load state_dict
    neural_network.load_network_from_structure(net)

    # Set model to eval
    net.eval()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    folderlist = os.listdir(os.path.dirname(__file__) + "\\test")

    tested = 0
    correct = 0

    for folder in folderlist:
        for file in os.listdir(os.path.dirname(__file__) + "\\test\\" + folder):
            if neural_network.result_from_network(net, os.path.dirname(__file__) + "\\test\\" + folder + "\\" + file) == folder:
                correct += 1
                tested += 1
            else:
                tested += 1

    print(correct/tested)


if __name__ == "__main__":
    NN_accuracy()
