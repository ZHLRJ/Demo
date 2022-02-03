# -*- coding: utf-8 -*-
'''
@Time    : 1/26/22 
@Author  : Zhang Haoliang
'''
import MoNet.utils as utils
number_edges=8
metric ='euclidean'
levels=4
def grid_graph(dimension=28):
    # dimension=28
    coordinatePairs = utils.grid(dimension)  # normalized nodes coordinates
    distance_matrix, sortedidx =utils.KNearestNodes(coordinatePairs, num_neighbors=number_edges, metric=metric)
    # dist contains the distance of the 8 nearest neighbors for each node indicated in z sorted in ascending order
    # idx contains the indexes of the 8 nearest for each node sorted in ascending order by distance

    weights = utils.generateAdjMatrix(distance_matrix,sortedidx)
    # graph.adjacency() builds a sparse matrix out of the identified edges computing similarities
    # as: A_{ij} = e^(-dist_{ij}^2/sigma^2)

    return weights, coordinatePairs
weights, coordinatePairs=grid_graph(dimension=28)
graphs, parents = utils.metis(weights,levels)