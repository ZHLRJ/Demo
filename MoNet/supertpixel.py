# -*- coding: utf-8 -*-
'''
@Time    : 1/28/22 
@Author  : Zhang Haoliang
'''
from PIL import Image, ImageDraw
import numpy as np
from torchvision.datasets import MNIST
from skimage.color import gray2rgba
# import skimage.io as io
# from skimage.draw import draw
import torch
from torch_cluster import grid_cluster
import matplotlib.pyplot as plt
import sys
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
sys.path.insert(0, '.')
sys.path.insert(0, '..')
sys.path.insert(0, '../..')

from torch_geometric.datasets import MNISTSuperpixels  # noqa
from torch_geometric.graph.grid import grid_5x5 # noqa
from torch_geometric.nn import max_pool,graclus, perm_input  # noqa
from torch_geometric.sparse import SparseTensor  # noqa
def grid_pos(height, width, dtype=None, device=None):
    dtype = torch.float if dtype is None else dtype
    x = torch.arange(width, dtype=dtype, device=device)
    y = (height - 1) - torch.arange(height, dtype=dtype, device=device)

    x = x.repeat(height)
    y = y.unsqueeze(-1).repeat(1, width).view(-1)

    return torch.stack([x, y], dim=-1)


image_dataset = MNIST('/tmp/MNIST', train=True, download=True)
graph_dataset = MNISTSuperpixels('/MNISTSuperpixels', train=True)

scale = 32
rescale = 4
offset = torch.FloatTensor([1, 1])
example = 35

image, _ = image_dataset[example]
image = np.array(image)
data = graph_dataset[example]
input, adj, position = data['input'], data['adj'], data['position']
print(data['target'])
segments_slic = slic(image, n_segments=70, compactness=10, sigma=1,start_label=1)

def max_grid_pool(x, position, adj, size):
    x = x.view(-1, 1)
    grid_size = position.new(2).fill_(size)
    cluster = grid_cluster(position, grid_size)
    index = adj._indices().contiguous()
    x, index, position = max_pool(x, index, position, cluster)
    n = position.size(0)
    adj = torch.sparse_coo_tensor(index, torch.ones(index.size(1)), torch.Size([n, n]))
    return x, position, adj


input, position, adj = max_grid_pool(input, position, adj, 3)
input, position, adj = max_grid_pool(input, position, adj, 6)


image = np.ones((28, 28), np.uint8)
image = np.repeat(image, scale * rescale, axis=0)
image = np.repeat(image, scale * rescale, axis=1)
image = gray2rgba(image, alpha=True)
# image *= np.array([228, 246, 232], np.uint8)
image *= np.array([255, 255, 255, 1], np.uint8)
# image *= np.array([0, 0, 0, 0], np.uint8)
image = Image.fromarray(image)
draw = ImageDraw.Draw(image)
image=Image.fromarray(segments_slic/max(segments_slic),mode='L' )
image.show()
offset = torch.FloatTensor([(28 - position[:, 0].max()) / 2,
                            (28 - position[:, 1].max()) / 2])
plt.imshow(image)
plt.show()
# row, col = adj._indices()
# direction = position[row] - position[col]
# direction = (direction * direction).sum(dim=1)
# mask = direction < 30
# row = row[mask]
# col = col[mask]
# index = torch.stack([row, col], dim=0)
# weight = torch.FloatTensor(row.size(0)).fill_(1)
# n = adj.size(0)
# adj = torch.sparse.FloatTensor(index, weight, torch.Size([n, n]))

position *= scale * rescale
position += scale * offset * rescale



index = adj._indices().t()
for i in range(index.size(0)):
    start, end = index[i]
    start_x, start_y = position[start]
    end_x, end_y = position[end]
    start_x, start_y = int(start_x), int(start_y)
    end_x, end_y = int(end_x), int(end_y)

    draw.line(
        (start_x, start_y, end_x, end_y),
        fill=(0, 0, 0, 255),
        width=rescale * 2)

for i in range(position.size(0)):
    x, y = position[i]
    r = 16 * rescale
    draw.ellipse((x - r, y - r, x + r, y + r), fill=(0, 0, 0, 255))
    r = 14 * rescale
    draw.ellipse(
        (x - r, y - r, x + r, y + r), fill=(49, 130, 219, int(255 * input[i])))
scale=4
image = image.resize((28 * scale, 28 * scale), Image.ANTIALIAS)

image.show()
