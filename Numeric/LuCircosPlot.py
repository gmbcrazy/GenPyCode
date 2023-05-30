# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 17:08:34 2023

@author: lzhang481
"""
from pycirclize import Circos
import numpy as np
import matplotlib.cm as cm
import networkx as nx


def Map2ColorMap(CData,Clim,ColorMapC,ClimN):

    temp=cm.get_cmap(ColorMapC)
    cmap_mat=temp(np.linspace(0,1,ClimN+1))
    C1 = CData.flatten()
    C1[C1 > Clim[1]] = Clim[1]
    C1[C1 < Clim[0]] = Clim[0]
    C2 = C1

    #ClimN = len(ColorMapC)
    ColorID = np.arange(ClimN)
# # Clim=[-0.1 0.1];
# # ClimN=10;
    B1, E1 = np.histogram(Clim, bins=ClimN-1)
    ColorC1I = np.digitize(C1, E1)
    ColorData=cmap_mat[ColorC1I,]
    return ColorC1I,ColorData


def Node2Circos(NodeName,NodeSpace):
    #  NodeName=['A','B','C','D','E']
    NodeL=np.ones([len(NodeName),1])*360/len(NodeName)
    S1=dict(zip(NodeName,NodeL))
    circos=Circos(S1,space=NodeSpace)
    
    VarS1=np.ones([len(NodeName),1])*360/len(NodeName)
    NodeN=list(S1.keys())
    NodePos=([S1[key] for key in NodeN])
    NodeStep=np.mean(VarS1/50)
    NodePosS=list(VarS1/2)
    NodePosO=list(VarS1/2)
   # NodePosS=list(VarS1/2-NodeStep)
   # NodePosO=list(VarS1/2+NodeStep)
    #NodeS1=tuple(zip(NodeN,NodePosS))
    NodeS1=tuple(zip(NodeName,NodePosS,NodePosO))
    return circos,NodeS1


def Node2Track(NodeWeight,NodeName,colormap,Clim,TrackPos,ClimN,circos):
    #  NodeName=['A','B','C','D','E']
    NodeL=np.ones([len(NodeName),1])*360/len(NodeName)
    S1=dict(zip(NodeName,NodeL))
    C1I,ColorNode=Map2ColorMap(NodeWeight,Clim,colormap,ClimN)

    i=0
    for sector in circos.sectors:
        trackTemp1=sector.add_track((TrackPos[0],TrackPos[1]))
        trackTemp1.axis(fc=ColorNode[i],ec="none",alpha=1)
        i=i+1
    return circos



def Adj2Edge(Adj,NodeS1,colormap,Clim,ClimN,NodeRad,circos):
    #Notedthat NodeS1 is the output of function Node
    # Adj = np.array([[0, 0.5, 0.9, -0.1, 0],
    #          [0.4, 0, 0.3, 0, 0],
    #         [0.2, 0.4, 0, 0, 0],
    #        [0, 0, 0, 0, 0.8],
    #           [0, 0, 0, 0.4, 0]])
    np.fill_diagonal(Adj,0)
    G=nx.from_numpy_matrix(np.array(Adj))
    EdgeN1,EdgeN2,weights=zip(*G.edges.data('weight'))
    EdgeN1=np.array(EdgeN1)
    EdgeN2=np.array(EdgeN2)
    weights=np.array(weights)
    EdgeCI,ColorEdge=Map2ColorMap(weights,Clim,colormap,ClimN)
    for N1,N2,EdgeC in zip(EdgeN1,EdgeN2,ColorEdge):
        circos.link(NodeS1[N1], NodeS1[N2], r1=NodeRad,r2=NodeRad, color=EdgeC,alpha=1) 
    return
