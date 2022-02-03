# -*- coding: utf-8 -*-
'''
@Time    : 1/28/22 
@Author  : Zhang Haoliang
'''
from PIL import Image, ImageDraw
import numpy as np
from skimage import color
import torch
from torchvision.datasets import MNIST
from torch_geometric.datasets import MNISTSuperpixels
from skimage.color import gray2rgb
from skimage.segmentation import mark_boundaries,slic
from skimage.measure import regionprops
import matplotlib.pyplot as plt
from skimage.measure import regionprops
import pylab
image_dataset = MNIST('/tmp/MNIST', train=True, download=True)



example_idx=100
numSegments=75
scale=32
def _scale(image, scale=8):
    if scale == 1:
        return image
    else:
        image = np.repeat(image, scale, axis=0)
        image = np.repeat(image, scale, axis=1)
        return image
# def showimage(image, image_label,mode='gray'):
#     image = np.array(image)
#     plt.imshow(image,cmap=mode)
#     plt.title("The number "+str(image_label))
#
#
# def _segment_with_mean(image, segmentation):
#     mean_image = np.zeros_like(image)
#     props = regionprops(segmentation + 1)
#
#     for i, prop in enumerate(props):
#         min_row, min_col, max_row, max_col = prop['bbox']
#         sliced_image = image[min_row:max_row, min_col:max_col]
#         color = sliced_image[prop['image']].mean(axis=0)
#
#         for row, col in prop['coords']:
#             mean_image[row, col] = color
#
#     return mean_image
# example_idx=12
# raw_image, image_label = image_dataset[example_idx]
# # raw_image=np.array(raw_image)
# raw_image = color.gray2rgb(np.reshape(raw_image, (28, 28)))
# image_scale=_scale(raw_image,scale=scale)
#
# segmentation = slic(raw_image, n_segments=numSegments,compactness=5, max_num_iter=10, sigma=2)
# segmentation = _scale(segmentation, scale)
# plt.imshow(mark_boundaries(image_scale, segmentation, (1, 0, 0)))
#
# # # store center position
# # regions = regionprops(segmentation)
# # position=[]
# # for props in regions:
# #     cx, cy = props.centroid  # centroid coordinates
# #     position.append([cx,cy])
#
# #     SuperPixels dataset
scale=32
rescale=4
raw_image, image_label = image_dataset[example_idx]
image=np.array(raw_image)
# image = np.ones((28, 28), np.uint8)
image = np.repeat(image, scale * rescale, axis=0)
image = np.repeat(image, scale * rescale, axis=1)
image = gray2rgb(image)
# plt.imshow(image)
# image *= np.array([228, 246, 232], np.uint8)
# image *= np.array([255, 255, 255, 1], np.uint8)
# image *= np.array([0, 0, 0, 0], np.uint8)
image = Image.fromarray(image)
draw = ImageDraw.Draw(image)
# plt.imshow(image)
# plt.show()





graph_dataset = MNISTSuperpixels('data/MNIST', True)
data = graph_dataset[example_idx]
input, index, position = data['x'], data['edge_index'], data['pos']
offset = torch.FloatTensor([(28 - position[:, 0].max()) / 2,
                            (28 - position[:, 1].max()) / 2])

# index=np.array(index)
# searched=set()
# for i in range(index.size(1)):
#     start, end = int(index[0][i]), int(index[1][i])
#
#     if start not in searched and input[start]>0:
#         searched.add(start)
#         print(start,position[start])
position *= scale * rescale
position += scale * offset * rescale


for i in range(index.size(1)):
    start, end = index[0][i],index[1][i]
    start_x, start_y = position[start]
    end_x, end_y = position[end]
    start_x, start_y = int(start_x), int(start_y)
    end_x, end_y = int(end_x), int(end_y)

    draw.line(
        (start_x, start_y, end_x, end_y),
        fill=(255, 0, 0, 255),
        width=rescale * 2)

for i in range(position.size(0)):
    x, y = position[i]
    r = 16 * rescale
    draw.ellipse((x - r, y - r, x + r, y + r), fill=(0, 0, 0, 255))
    r = 14 * rescale
    draw.ellipse(
        (x - r, y - r, x + r, y + r), fill=(49, 130, 219, int(255*2 * input[i])))
    # if v > 0:
    #     print(v)
    # c1 = [49 * v, 130 * v, 219 * v]
    # c2 = [228 * (1 - v), 246 * (1 - v), 232 * (1 - v)]
    # c = (int(c1[0] + c2[0]), 130, 219)

    # draw.ellipse((x - r, y - r, x + r, y + r), fill=c)
    if input[i] > 0.0:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(49, 130, 219))
    else:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(228, 246, 232))
image = image.resize((28 * scale, 28 * scale), Image.ANTIALIAS)

# image.show()
plt.imshow(image)