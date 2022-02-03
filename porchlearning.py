# -*- coding: utf-8 -*-
'''
@Time    : 1/15/22
@Author  : Zhang Haoliang
'''

import torch
import math

dtype = torch.float
device = torch.device("cpu")


# Create Tensors to hold input and outputs.
x = torch.linspace(1, 20, 20)
y = torch.sin(x)

# For this example, the output y is a linear function of (x, x^2, x^3), so
# we can consider it as a linear layer neural network. Let's prepare the
# tensor (x, x^2, x^3).
p = torch.tensor([1, 2, 3])
xx = x.unsqueeze(-1).pow(p)