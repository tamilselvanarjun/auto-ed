import networkx as nx
import matplotlib
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure
import io
#matplotlib.use('agg')
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from ADnum_rev_timed_vis import ADnum
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
    ins = total-len(parents)
    new_names = {}
    nodes = [y]
    while len(nodes)>0:
        node = nodes.pop(0)
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
                #new_names[node] = 'X' + str(total)
                #total = total -1
            #else:
             #   if len(nodes)>ins-2:
              #      nodes.append(node)
               # else:
                #    new_names[node] = 'X'+str(total)
                 #   total = total -1

            #else:
             #   if len(nodes) > ins-1:
              #      nodes.insert(0, node)
               # else:
                #    new_names[node] = 'X' + str(total)
                 #   total = total -1
    return new_names

def get_labels_rev(y):
    """ Function to generate labels for plotting networkx graph.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A dictionary of ADnum objects mapped to string labels
    """
    parents = reverse_graph(y)
    #total = len(y.graph) - sum([entry.constant for entry in y.graph.keys()])
    total = 0
    new_names = {}
    nodes = [y]
    while len(nodes)>0:
        
        node = nodes.pop()
        if node not in new_names:
            if node.constant:
                new_names[node] = str(np.round(node.val, decimals=1))
            else:
                new_names[node] = 'X' + str(total)
                total = total + 1
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

def draw_graph2(y, G, edge_labs, pos, labs, ax=None):
    """ Function to draw the graph.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A plot of the graph
    """  
    fig = Figure() #plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.axis('off')
    #G = gen_graph(y)
    #edge_labs = nx.get_edge_attributes(G, 'label')
    #pos = nx.spring_layout(G)
    #labs = get_labels(y)
    nx.draw_networkx(G, pos, labels = labs, node_color = get_colors(G, y), node_size = get_sizes(G, y, labs), font_color= 'white', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labs, ax=ax)
    #limits = plt.axis('off')
    mag_patch = mpatches.Patch(color = 'magenta', label = 'input')
    red_patch = mpatches.Patch(color = 'red', label = 'intermediate')
    blue_patch = mpatches.Patch(color = 'blue', label = 'constant')
    green_patch = mpatches.Patch(color = 'green', label = 'output')
    ax.legend(handles = [mag_patch, red_patch, blue_patch, green_patch])
    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    #plt.show()
    return output


def draw_graph_rev(y):
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
    G = G.reverse()
    edge_labs = nx.get_edge_attributes(G, 'label')
    pos = nx.spring_layout(G)
    labs = get_labels(y)
    #labs = get_labels_rev(y)
    nx.draw_networkx(G, pos, labels = labs, node_color = get_colors(G, y), node_size = get_sizes(G, y, labs), font_color= 'white')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labs)
    limits = plt.axis('off')
    mag_patch = mpatches.Patch(color = 'magenta', label = 'input')
    red_patch = mpatches.Patch(color = 'red', label = 'intermediate')
    blue_patch = mpatches.Patch(color = 'blue', label = 'constant')
    green_patch = mpatches.Patch(color = 'green', label = 'output')
    plt.legend(handles = [mag_patch, red_patch, blue_patch, green_patch])
    return fig 


def draw_graph_rev2(y, G, edge_labs, pos, labs, ax=None):
    """ Function to draw the graph.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A plot of the graph
    """  
    fig = plt.figure()
    #G = gen_graph(y)
    G = G.reverse()
    #edge_labs = nx.get_edge_attributes(G, 'label')
    #pos = nx.spring_layout(G)
    #labs = get_labels(y)
    #labs = get_labels_rev(y)
    nx.draw_networkx(G, pos, labels = labs, node_color = get_colors(G, y), node_size = get_sizes(G, y, labs), font_color= 'white', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labs)
    limits = plt.axis('off')
    mag_patch = mpatches.Patch(color = 'magenta', label = 'input')
    red_patch = mpatches.Patch(color = 'red', label = 'intermediate')
    blue_patch = mpatches.Patch(color = 'blue', label = 'constant')
    green_patch = mpatches.Patch(color = 'green', label = 'output')
    plt.legend(handles = [mag_patch, red_patch, blue_patch, green_patch])
    plt.show()
    #return fig

def get_graph_setup(y):
    G = gen_graph(y)
    #G = G.reverse()
    edge_labs = nx.get_edge_attributes(G, 'label')
    pos = nx.spring_layout(G, k=.15, iterations=20)
    labs = get_labels(y) #changed from get labels rev
    return G, edge_labs, pos, labs

def axis_reverse_edge(y, G, edge_labs, pos, labs, ax, edgelist, idx):
    edge = edgelist[idx]
    nx.draw_networkx(G, pos, ax = ax, labels = labs, node_color = get_colors(G, y), node_size = get_sizes(G, y, labs), font_color= 'white')
    nx.draw_networkx_edges(G, pos=pos, ax=ax, edgelist = edge, width = 4, edge_color = 'y', style = 'dashed')
    nx.draw_networkx_edge_labels(G, pos=pos, ax=ax, edge_labels = edge_labs)
    limits = plt.axis('off')

def draw_graph_rev_dynamic(y, edgelist, G, edge_labs, pos, labs, val):
    edgelist.reverse()
    fig = plt.figure()
    #G, edge_labs, pos, labs = get_graph_setup(y)
    G = G.reverse()
    ax = fig.add_subplot(111)
    ax.set_title('Press enter to start. \n Then use the left and right arrow keys to step through the calculation.')
    #plt.title('Press enter to start.  \n Then use the left and right arrow keys to step through the calculation.')
    ax.axis("off")
    #plt.axis("off")
    global curr_pos
    curr_pos = 0
    #axis_reverse_edge(y, G, edge_labs, pos, labs, ax, edgelist, curr_pos)
    #plt.show()
    def key_event(e):
        global curr_pos
        ax.cla()
        if e.key == 'enter':
            curr_pos = curr_pos
        elif e.key == 'right':
            curr_pos = curr_pos +1
            if curr_pos >= len(edgelist):
                curr_pos = len(edgelist)-1
        elif e.key == 'left':
            curr_pos = curr_pos -1
            if curr_pos<0:
                curr_pos = 0
        else:
            return
        #curr_pos = curr_pos%len(edgelist)
        axis_reverse_edge(y, G, edge_labs, pos, labs, ax, edgelist, curr_pos)
        if curr_pos == len(edgelist)-1:
            ax.set_title('Step ' + str(curr_pos+1)+': Caclulation Complete')
            #print('hello')
            #plt.title('Step ' + str(curr_pos+1) +': Calculation Complete')
        else:
            ax.set_title('Step ' + str(curr_pos+1))
            #print('hello')
            #plt.title('Step ' + str(curr_pos+1))

        plt.show()
    if len(edgelist)>0:
        fig.canvas.mpl_connect('key_press_event', key_event)
    elif val == 1:
        #plt.close()
        draw_graph_rev2(y, G, edge_labs, pos, labs, ax=ax)
    else:
        print('hello')
        #return
        #draw_graph_rev2(y, G, edge_labs, pos, labs)
        #plt.title('No dependence on input variable.')
    plt.show()


def draw_graph_rev_dynamic_old(y, edgelist):
    """ Function to draw the graph.

    INPUTS
    ======
    y : ADnum

    OUTPUTS
    =======
    A plot of the graph
    """  
    edgelist.reverse()
    fig = plt.figure()
    G = gen_graph(y)
    G = G.reverse()
    edge_labs = nx.get_edge_attributes(G, 'label')
    pos = nx.spring_layout(G)
    labs = get_labels_rev(y)
    nx.draw_networkx(G, pos, labels = labs, node_color = get_colors(G, y), node_size = get_sizes(G, y, labs), font_color= 'white')
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labs)
    limits = plt.axis('off')
    mag_patch = mpatches.Patch(color = 'magenta', label = 'input')
    red_patch = mpatches.Patch(color = 'red', label = 'intermediate')
    blue_patch = mpatches.Patch(color = 'blue', label = 'constant')
    green_patch = mpatches.Patch(color = 'green', label = 'output')
    plt.legend(handles = [mag_patch, red_patch, blue_patch, green_patch])
    figset = []
    for edge in edgelist:
        fignew = plt.figure()
        nx.draw_networkx(G, pos, labels = labs, node_color = get_colors(G, y), node_size = get_sizes(G, y, labs), font_color= 'white')
        nx.draw_networkx_edges(G, pos=pos, edgelist = edge, width = 4, edge_color = 'y', style = 'dashed')
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = edge_labs)
        figset.append(fignew)
    return fig, figset
 
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
    result['Number'] = [int(name[1:]) for name in result['Trace']]
    result2 = result.sort_values('Number')
    resultorder = result2[['Trace', 'Operation', 'Value', 'Derivative']]  
    return resultorder

def gen_table_rev(y):
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
    #labs = get_labels_rev(y)
    visited = []
    data = {}
    data['Trace'] = []
    data['Operation']=[]
    #data['Value']= []
    data['Derivative']=[]
    data['Weight'] = []
    nodes = [y]
    while len(nodes)>0:
        node = nodes.pop()
        if node not in visited:
            if node.constant:
                visited.append(node)
            else:
                visited.append(node)
                data['Trace'].append(labs[node])
                #data['Value'].append(node.val)
                data['Derivative'].append(node.der)
                data['Weight'].append(node.rder)
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
    result['Number'] = [int(name[1:]) for name in result['Trace']]
    result2 = result.sort_values('Number')
    resultorder = result2[['Trace', 'Operation', 'Weight']]  
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


