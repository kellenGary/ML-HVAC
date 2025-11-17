import torch
from torch.utils.data import Dataset
import numpy as np

class HvacDataset(Dataset) :
    def __init__(self, timestamp, temp, humidity):
        #create all tensors based on the packet
        self.timestamp = np.array(timestamp, dtype=np.float32)
        self.temp = np.array(temp, dtype=np.float32)
        self.humidity = np.array(humidity, dtype=np.float32)

        self.inputs = np.column_stack(self.timestamp, self.temp, self.humidity)

    def __len__(self):
        return len(self.inputs)
        

    def __getitem__(self, idx):
        x = torch.tensor(self.inputs[idx], dtype=torch.float32)
        return x

        

