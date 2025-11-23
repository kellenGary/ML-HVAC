import torch
import torch.nn as nn

class Temp_Predictor(nn.Module) :
    def __init__(self):
        super(Temp_Predictor, self).__init__()
        self.linear = nn.Linear(in_features=3, out_features=1)
        pass

    def forward(self, x):
        return self.linear(x)
    
model = Temp_Predictor()
optimizer = torch.optim.Adam(model.parameters, lr=0.01)
loss = nn.MSELoss