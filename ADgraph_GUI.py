import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from AD20.ADnum import ADnum
from mpl_toolkits.mplot3d import Axes3D

def gen_graph(y):
    """ Function to create a directed graph from an ADnum.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A networkx digraph
    """
    G = nx.DiGraph()
    d = y.graph
    if len(d)== 0:
        G.add_node(y)
    for key in d:
        G.add_node(key)
        neighbors = d[key]
        for neighbor in neighbors:
            G.add_edge(key, neighbor[0], label = neighbor[1])
    return G

def reverse_graph(y):
    """ Function to create a dictionary containing edges of y reversed.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A dictionary
    """
    d = y.graph
    parents = {}
    for key in d:
        neighbors = d[key]
        for neighbor in neighbors:
            if neighbor[0] not in parents:
                parents[neighbor[0]] = []
            parents[neighbor[0]].append((key, neighbor[1]))
    return parents

def get_labels(y):
    """ Function to generate labels for plotting networkx graph.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A dictionary of ADnum objects mapped to string labels
    """
    parents = reverse_graph(y)
    total = len(y.graph) - sum([entry.constant for entry in y.graph.keys()])
    new_names = {}
    nodes = [y]
    while len(nodes)>0:
        node = nodes.pop()
        if node not in new_names:
            if node.constant:
                new_names[node] = str(np.round(node.val, decimals=1))
            else:
                new_names[node] = 'X' + str(total)
                total = total - 1
            if node in parents:
                neighbors = parents[node]
                for neighbor in neighbors:
                    nodes.append(neighbor[0])
    return new_names

def get_colors(G, y):
    """ Function to assign colors to nodes in the graph.

    INPUTS
    ======
    G : networkx digraph
    y : ADnum

    OUTPUTS
    =======
    A list of colors for the graph
    """
    colors = []
    parents = reverse_graph(y)
    for node in G:
        if node.constant:
            colors.append('blue')
        else:
            if node == y:
                colors.append('green')
            else:
                if node in parents:
                    colors.append('red')
                else:
                    colors.append('magenta')
    return colors

def get_sizes(G, y, labs):
    """ Function to assign sizes to nodes in the graph.

    INPUTS
    ======
    G : networkx digraph
    y : ADnum
    labs : dictionary of graph labels

    OUTPUTS
    =======
    A list of sizes for the graph
    """
    sizes = []
    for node in G:
        label = labs[node]
        sizes.append(len(label)*200)
    return sizes

def draw_graph(y):
    """ Function to draw the graph.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A plot of the graph
    """  
    fig = plt.figure()
    G = gen_graph(y)
    edge_labs = nx.get_edge_attributes(G, 'label')
    pos = nx.spring_layout(G)
    labs = get_labels(y)
    nx.draw_networkx(G, pos, labels = labs, node_color = get_colors(G, y), node_size = get_sizes(G, y, labs), font_color= 'white')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labs)
    limits = plt.axis('off')
    mag_patch = mpatches.Patch(color = 'magenta', label = 'input')
    red_patch = mpatches.Patch(color = 'red', label = 'intermediate')
    blue_patch = mpatches.Patch(color = 'blue', label = 'constant')
    green_patch = mpatches.Patch(color = 'green', label = 'output')
    plt.legend(handles = [mag_patch, red_patch, blue_patch, green_patch])
    return fig

def gen_table(y):
    """ Function to generate tables for the ADnum.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A pandas data frame of the computational traces
    """
    parents = reverse_graph(y)
    labs = get_labels(y)
    visited = []
    data = {}
    data['Trace'] = []
    data['Operation']=[]
    data['Value']= []
    data['Derivative']=[]
    nodes = [y]
    while len(nodes)>0:
        node = nodes.pop()
        if node not in visited:
            if node.constant:
                visited.append(node)
            else:
                visited.append(node)
                data['Trace'].append(labs[node])
                data['Value'].append(node.val)
                data['Derivative'].append(node.der)
                if node in parents:
                    if len(parents[node]) == 1:
                        link = parents[node][0][1]+'('+labs[parents[node][0][0]]+')'
                    else:
                        link = parents[node][0][1]+'(' +labs[parents[node][0][0]]+ ' , ' + labs[parents[node][1][0]] + ')'
                    neighbors = parents[node]
                    for neighbor in neighbors:
                        nodes.append(neighbor[0])
                else:
                    link = 'input'
                data['Operation'].append(link)
    result = pd.DataFrame.from_dict(data)
    result2 = result.sort_values('Trace')
    resultorder = result2[['Trace', 'Operation', 'Value', 'Derivative']]  
    return resultorder

def plot_ADnum(f, ins=1, xmin = -10, xmax = 10):
    '''Function to plot f and its derivative for single variable input

    INPUTS
    ======
    x : ADnum
    xmin : starting value of input
    xmax : ending value of input

    OUTPUTS
    =======
    A plot of x evaluated from xmin to xmax and its derivative
    '''
    if ins == 1:
        vals = np.linspace(xmin, xmax, 100)
        evals = [f(ADnum(value, der=1)).val for value in vals]
        ders = [f(ADnum(value, der=1)).der for value in vals]
        fig = plt.figure()
        plt.plot(vals, evals, label = 'f', linewidth = 2)
        plt.plot(vals, ders, label = 'df/dx', linewidth = 2)
        plt.legend(fontsize = 20)
        plt.xlabel('x', fontsize = 20)
        plt.ylabel('f', fontsize = 20)
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 12)
        return fig
    if ins == 2:
        fig = plt.figure()
        ax = fig.gca(projection = '3d')
        vals = np.linspace(xmin, xmax, 100)
        z = f(vals, vals)
        ax.plot_trisurf(vals, vals, z, antialiased = True)
        return fig
    if ins > 2:
        fig = plt.figure()
        return fig


