#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:10:48 2022

@author: albitcabanmurillo
"""

import pandas as pd
import numpy as np
import scipy.special as sc
import seaborn as sns
import matplotlib.pyplot as plt
#import markov_clustering as mc
from bokeh.io import output_file, show
from bokeh.models import (Circle, MultiLine, Plot, Range1d, BoxZoomTool, ResetTool)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx
from bokeh.models import ColumnDataSource, LabelSet
from IPython import get_ipython
import bokeh as bk 
import matplotlib.colors as colors

from bokeh.io import output_file, show
from bokeh.models.graphs import from_networkx
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool,)
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,)
from bokeh.palettes import Spectral4
#from bokeh.plotting import from_networkx
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc
from sklearn.decomposition import PCA
#import plotly.express as px
import scola
import pylab
import networkx.algorithms.community as nx_comm


#%%
ndf = pd.read_csv('/Users/albitcabanmurillo/Downloads/CFOS_networks/NwxFosM1Tcorrect.csv')
#%%
# THIS IS FOR TEST PURPOSES ONLY
file = 'TempChR2.csv'
file2 = 'TempControl.csv'
get_ipython().run_line_magic('matplotlib', 'qt')
#%%
# simple function for loading our csv file
def loadData(data):
    data = pd.read_csv(data)  # add col list if you already made entirety of analysis usecols=(col_list)
    # data.drop(columns=data.columns[data.nunique() <= 3], inplace=True)
    data = data.apply(lambda x: x.fillna(x.mean()), axis=0)
    node_names = data.columns.to_list()
    node_number = list(item for item in range(0, len(node_names)))
    nodes = {node_number[i]: node_names[i] for i in range(len(node_number))}
    return data, nodes
#%%
# correlate our c-Fos counts between brain regions, df for data
# type for correlation coefficient i.e. "pearson"
def corrMatrix(data):
    rVal = np.corrcoef(data, rowvar=False)  # calculate pearson coefficients
    rf = rVal[np.triu_indices(rVal.shape[0], 1)]  # upper triangular matrix of data to shuffle for p-value calc
    df = data.shape[1] - 2  # calculate degrees of freedom
    ts = rf * rf * (df / (1 - rf * rf))  # calculate t's
    pf = sc.betainc(0.5 * df, 0.5, df / (df + ts))  # calculate p's from beta incomplete function
    # generate p-value matrix
    p = np.zeros(shape=rVal.shape)
    p[np.triu_indices(p.shape[0], 1)] = pf
    p[np.tril_indices(p.shape[0], -1)] = p.T[np.tril_indices(p.shape[0], -1)]
    p[np.diag_indices(p.shape[0])] = np.ones(p.shape[0])
    return rVal, p
#%%