"""
FILE DESCRIPTION:
-----------------

This file contains all methods related to graph clustering/community detection , here i used the data collected in
Collector.py , i have collected 300 followers of Ellon Musk and for each of those followers i have collected 300 more
who are following the main follower of Ellon Musk (Basically the direct followers and 1 hop away followers of ellon musk).
Then i am using girvan-newman's clustering technique to identify clusters in the main graph, also i am plotting the
graph before and after clustering occurs.

Here my main aim was to check and see if they were any different communities of users who followed Ellon musk and what
type of community each one of them were.

Module Requirements for this File:
1) Collections
2) Networkx
3) Json
4) matplotlib
5) itertools
6) OS
7) faker

Here faker can be installed through the pip installer using the command -- pip install faker

"""

from faker import Factory
from collections import defaultdict
from networkx import edge_betweenness_centrality as betweenness
import networkx as nx
import json
import matplotlib.pyplot as plt
import itertools
import os


def create_graph(filename):
    """
    This method creates a graph from my republican_friends_map.json where i have collected followers of the
    republican party and who each of them follow.

    :param         filename: The file to read and create a graph from

    :return:       A unidirectional networkx graph object
    """
    G = nx.Graph()
    with open(filename,'r') as fp:
        follower_dict = json.load(fp)
    fp.close()

    G.add_nodes_from(follower_dict.keys())

    for key in follower_dict:
        for x in follower_dict[key]:
            if x not in G:
                G.add_node(x)
                G.add_edge(key,x)
            elif x in G and G.has_edge(key,x) == False and G.has_edge(x,key) == False:
                G.add_edge(key,x)

    print("\nCreated graph from data in file --> " + filename+"\n")
    print("\nGraph Contains : ")
    print("----------------")
    print("\n " + str(len(G.nodes())) + " Nodes")
    print("\n " + str(len(G.edges())) + " Edges")
    return G

def save_graph(G):
    """
    This creates an image of our original graph that has not undergone clustering .

    :param      G: Our networkx graph object
    :return:    Nothing
    """
    pos = nx.spring_layout(G, scale=5)
    plt.axis("off")
    nx.draw_networkx_nodes(G, pos, alpha=0.5, node_size=20, node_color='red')
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.4)
    plt.savefig("Cluster_Folder"+os.path.sep+"Graph.png", dpi=300)
    print("\nSaved Graph before Clustering to --> Graph.png in the Cluster_Folder")
    # plt.show()

def save_clustered_graph(G,com_dict,color_list):
    """
    This method creates a graph image using the cluster details and a random list of colours in hexadecimal format that
    is equal to the no of clusters found by girvan-newman.

    :param              G               : The networkx graph object
    :param              com_dict        : The dict containing different communities/clusters
    :param              color_list      : The list containing random hexadecimal notations of colors based
                                          on the number of clusters found
    :return:            Nothing
    """

    node_color = []
    new_G = G.copy()

    for n in new_G.nodes():
        for key in com_dict:
            if n in com_dict[key]:
                node_color.append(color_list[key])

    plt.clf()
    pos = nx.spring_layout(new_G, scale=8)
    plt.axis("off")
    nx.draw_networkx_nodes(new_G, pos, alpha=0.5, node_size=20, node_color=node_color)
    nx.draw_networkx_edges(new_G, pos, alpha=0.3, width=0.4)
    plt.savefig("Cluster_Folder"+os.path.sep+"clusteredGraph.png", dpi=300)
    print("\nSaved Graph after Clustering to --> Clustered_Graph.png in the Cluster_Folder")
    # plt.show()


def color_creation(no_of_communities):
    """
    This method creates random colour for each community using the faker python library equal to no of
    clusters/communities found

    :param          no_of_communities: The

    :return:        List of colours equal to no of communities found.
    """
    color_list = []
    fake  = Factory.create()
    for i in range(no_of_communities):
        color_list.append(fake.hex_color())

    return color_list


def cluster_graph(G,k):
    """
    This method clusters our given networkx graph into k clusters / communities using girvan_newman algorithm.

    :param      G: Our networkx graph made from twitter friend data

    :return:    The clusters of our graph.
    """
    comp = girvan_newman(G)
    # print(tuple(sorted(c) for c in next(comp)))

    result = tuple
    for comp in itertools.islice(comp, k-1):

        result = tuple(sorted(c) for c in comp)

    return result

def girvan_newman(G, most_valuable_edge=None):
    """
    This is the code given on the NetworkX Documentation site to implement girvan_Newman.

    :param        G: Our networkx graph object
    :param        most_valuable_edge: The most valuable edge in our graph ( can be based on weight, centrality measure
                                      or betweeness score).
    :return:      A generator of communities.
    """

    if G.number_of_edges() == 0:
        yield tuple(nx.connected_components(G))
        return

    if most_valuable_edge is None:
        def most_valuable_edge(G):
            betweenness = nx.edge_betweenness_centrality(G)
            return max(betweenness, key=betweenness.get)
    g = G.copy().to_undirected()
    g.remove_edges_from(g.selfloop_edges())
    # print("\t\t********************* - Completed Clustering of Graph - *********************")
    while g.number_of_edges() > 0:
        yield _without_most_central_edges(g, most_valuable_edge)



def _without_most_central_edges(G, most_valuable_edge):
    """
    Built-in method used for Girvan Newman

    :param G:
    :param most_valuable_edge:
    :return:
    """
    original_num_components = nx.number_connected_components(G)
    num_new_components = original_num_components
    new_components = tuple()
    while num_new_components <= original_num_components:
        edge = most_valuable_edge(G)
        G.remove_edge(*edge)
        new_components = tuple(nx.connected_components(G))
        num_new_components = len(new_components)
    return new_components

def most_central_edge(G):
    """
    Built-in method used for Girvan Newman

    :param G:
    :return:
    """
    centrality = betweenness(G)
    return max(centrality, key=centrality.get)

def cluster_details(Communities_tuple):
    """
    This saves the details of the clusters found and saves it to the cluster_details.txt file in the Clusters_Folder

    :param      Communities_tuple: The tuple that contains the clusters of the networkx graph
    :return:    Nothing
    """
    com_dict = defaultdict(list)

    for i in range(len(Communities_tuple)):
        com_dict[i] = Communities_tuple[i]

    totalsum = 0.0
    n_com = len(com_dict)
    for key in com_dict:
        totalsum += len(com_dict[key])

    avg_users = totalsum/n_com

    with open("Cluster_Folder"+os.path.sep+"cluster_details.txt",'w') as fp:
        fp.write("Number of communities discovered : " + str(len(Communities_tuple))+ "\n")
        fp.write("Average Number of users per community : " + str(avg_users)+ "\n")

    fp.close()
    return com_dict

def save_cluster(cluster_tuple):
    """
    This method saves the clusters of the graph to clusters.txt
    :param          cluster_tuple : The tuple containing the different clusters
    :return:        Nothing
    """
    with open("Cluster_Folder"+os.path.sep+"cluster.txt",'w') as fp:
        for i in range(len(cluster_tuple)):
            fp.write("Cluster " + str(i) + str(cluster_tuple[i]) + "\n")

    fp.close()
    print("\nClusters are saved to --> " + "cluster.txt in Cluster_Folder folder\n")

def main():
    """
    This method runs the methods defined in this file and saves the details after identifying the clusters and generates
    a graph before clustering and after clustering.

    :return: Nothing
    """

    print("\t\t************************ - Starting cluster.py - ************************ ")

    G = create_graph(filename="Collect_Folder"+ os.path.sep +"elonmusk.json")
    save_graph(G=G)
    cluster_tuple = cluster_graph(G=G,k=7)
    save_cluster(cluster_tuple)
    com_dict = cluster_details(Communities_tuple=cluster_tuple)
    color_list = color_creation(no_of_communities=len(com_dict))
    save_clustered_graph(G=G,com_dict=com_dict,color_list=color_list)

    print("\n\t\t************************ - Finished Graph Clustering - ************************")



if __name__ == main():
    main()
