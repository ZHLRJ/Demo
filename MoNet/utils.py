# -*- coding: utf-8 -*-
'''
@Time    : 1/26/22 
@Author  : Zhang Haoliang
'''
import numpy as np
import sklearn.metrics
import sklearn.neighbors
import scipy.sparse
import matplotlib.pyplot as plt
def grid(dimension,dtype=np.float32):
    # generate grid
    # dtype = np.float32
    # dimension=28
    x_array = np.linspace(0, 1, dimension, dtype=dtype)
    y_array = np.linspace(0, 1, dimension, dtype=dtype)
    x_coordinates,y_coordinates=np.meshgrid(x_array,y_array)
    coordinatesPairs=np.vstack((x_coordinates.reshape(dimension**2),y_coordinates.reshape(dimension**2))).transpose()
    return coordinatesPairs
def KNearestNodes(coordinatesPairs,num_neighbors=4,metric='euclidean'):
    distance_matrix = sklearn.metrics.pairwise_distances(coordinatesPairs, metric=metric)
    # k-NN graph.
    sortedidx = np.argsort(distance_matrix)
    distance_matrix.sort()
    return distance_matrix[:,1:1+num_neighbors], sortedidx[:,1:1+num_neighbors]

def generateAdjMatrix(distance_matrix,sortedidx):
    # W_ij=exp(|Z_i - Z_j|*2 / \theta^2)
    variance=np.mean(distance_matrix[:,-1])**2
    distance_matrix=np.exp(-distance_matrix**2/variance)
    row,col=distance_matrix.shape
    # Weight matrix.
    I = np.arange(0, row).repeat(col)
    J = sortedidx.flatten()

    weights = scipy.sparse.coo_matrix((distance_matrix.flatten(), (I, J)), shape=(row, row))

    # No self-connections.
    weights.setdiag(0)

    # Non-directed graph.
    bigger = weights.T > weights
    weights = weights- weights.multiply(bigger) + weights.T.multiply(bigger)
    return weights
def metis(weights,levels=4,rid=None):
    # INPUT
    #Weights: symmetric sparse weight (adjacency) matrix
    #levels: the number of coarsened graphs
    x_dimension,y_dimension=weights.shape
    if rid is None:
        rid = np.random.permutation(range(x_dimension))
    parents = []  # contains in each position the id of the clusters where two nodes have been placed
    degree = weights.sum(axis=0) - weights.diagonal()
    graphs = []
    graphs.append(weights)
    for _ in range(levels):
        squeezeweights=np.array(degree).squeeze()
        # PAIR THE VERTICES AND CONSTRUCT THE ROOT VECTOR
        # idx_row, idx_col and val contain the row indices, column indices, and values of the nonzero matrix entries
        idx_row, idx_col, val = scipy.sparse.find(weights)
        perm=np.argsort(idx_row)
        orderedrow=idx_row[perm]
        orderedcol=idx_col[perm]
        orderedval=val[perm]
        cluster_id=merit_operation(orderedrow, orderedcol, orderedval, rid, squeezeweights)
        parents.append(cluster_id)
        # COMPUTE THE EDGES WEIGHTS FOR THE NEW GRAPH
        nrr = cluster_id[orderedrow]
        # nrr and ncc are the idx of edges after clustering, self-loops are produced for each node by these new edges
        ncc = cluster_id[orderedcol]
        nvv = orderedval
        Nnew = cluster_id.max() + 1

        # CSR is more appropriate: row,val pairs appear multiple times
        weights = scipy.sparse.csr_matrix((nvv, (nrr, ncc)), shape=(Nnew, Nnew))
        weights.eliminate_zeros()
        # Add new graph to the list of all coarsened graphs
        graphs.append(weights)
        N, N = weights.shape

        # COMPUTE THE DEGREE (OMIT OR NOT SELF LOOPS)
        degree = weights.sum(axis=0)

        # CHOOSE THE ORDER IN WHICH VERTICES WILL BE VISTED AT THE NEXT PASS
        # [~, rid]=sort(ss);     # arthur strategy
        # [~, rid]=sort(supernode_size);    #  thomas strategy
        # rid=randperm(N);                  #  metis/graclus strategy
        ss = np.array(weights.sum(axis=0)).squeeze()
        rid = np.argsort(ss)

    return graphs, parents

def merit_operation(orderedrow,orderedcol,orderedval,rid,squeezeweights):
    orderedrowLen=orderedrow.shape[0]
    N=orderedrow[-1]+1

    marked = np.zeros(N, bool)   # identifies already processed nodes
    rowstart = np.zeros(N, np.int32)  # contains the idx of the edges where a new row start
    rowlength = np.zeros(N, np.int32)  # contains in every entry the number of edges associated to the row
    cluster_id = np.zeros(N, np.int32)  # contains the idx of the clusters of nodes after pairing
    oldval = orderedrow[0]
    count = 0
    clustercount = 0
    for idx in range(orderedrowLen):
        rowlength[count]+=1
        if orderedrow[idx]>oldval:
            oldval=orderedrow[idx]
            rowstart[count+1]=idx
            count+=1
    for idx in range(N):
        targetidx=rid[idx]
        if not marked[targetidx]:
            maxweight=0.0
            rowstartposition=rowstart[targetidx]
            marked[targetidx]=True
            bestneighbor=-1
            for nbr_step in range(rowlength[targetidx]):
                neighbor_idx=orderedcol[rowstartposition+nbr_step]
                if marked[neighbor_idx]:
                    tval = 0.0
                else:
                    # w_ij * 1/(\sum_k w_ik) + w_ij * 1/(\sum_k w_kj)
                    tval = orderedval[rowstartposition+nbr_step] * (1.0/squeezeweights[targetidx] + 1.0/squeezeweights[neighbor_idx])
                if tval>maxweight:
                    maxweight=tval
                    bestneighbor=neighbor_idx
            cluster_id[targetidx]=clustercount
            if bestneighbor > -1:
                cluster_id[bestneighbor] = clustercount
                marked[bestneighbor] = True
            clustercount += 1
    return cluster_id
def plot_matrix(m):
    plt.figure(figsize=(5, 5))
    plt.imshow(m.toarray())
    plt.show()
# plot_matrix(weights)
A=[1,2]
A.insert(0,4)