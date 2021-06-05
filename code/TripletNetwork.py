# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 13:59:49 2021

@author: danie
"""

# %% Imports

import torch
import torch.nn as nn
import torch.nn.functional as F

# %% General sub net architecture

class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
            self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
            self.conv2_drop = nn.Dropout2d()
            self.fc1 = nn.Linear(320, 50)
            self.fc2 = nn.Linear(50, 10)

        def forward(self, x):
            x = F.relu(F.max_pool2d(self.conv1(x), 2))
            x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
            x = x.view(-1, 320)
            x = F.relu(self.fc1(x))
            x = F.dropout(x, training=self.training)
            return self.fc2(x)
        
# %% Triplet net embedding and distances

class TripletNetClass(nn.Module):
    def __init__(self, embeddingnet):
        super(TripletNetClass, self).__init__()
        self.embeddingnet = embeddingnet

    def forward(self, x, y, z):
        embedded_x = self.embeddingnet(x)
        embedded_y = self.embeddingnet(y)
        embedded_z = self.embeddingnet(z)
        dist_a = F.pairwise_distance(embedded_x, embedded_y, 2)
        dist_b = F.pairwise_distance(embedded_x, embedded_z, 2)
        return dist_a, dist_b, embedded_x, embedded_y, embedded_z

# %% Triplet net model  

def TripletNetModel(device):
    model = Net()
    Tnet = TripletNetClass(model).to(device)
    return Tnet

# %% Main
    
if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    Tnet = TripletNetModel(device)
    print('Triplet network defined succefully !')