from constants import *
import random
import networkx as nx
import copy
from math import ceil
import matplotlib.pyplot as plt



def deter(conn, connections):
    x,y = conn
    if (y,x) in connections:
        connections.remove((y,x))
    return True


def num_connections(num, perc, conn_num):
    delta = int(ceil(perc * num))
    conn = random.randint(int(conn_num/2 - delta), int(conn_num/2 + delta))  
    return conn


NUM = len(ADDRESSES)
temp_json = {"graph":[]}
connections = []
connections = [(x,y) for x in ADDRESSES for y in ADDRESSES if (x != y)]
conn = [x for x in connections if deter(x, connections)] # hack of resizing array!
# random.shuffle(connections) 
# conn = num_connections(NUM, 0.1, len(connections))
# connections = connections[:conn]
          
for i in range(NUM):
    temp_addresses = copy.deepcopy(ADDRESSES)
    temp_addresses.remove(ADDRESSES[i])
    temp_dict = {"id":ADDRESSES[i],'neighbor':[]}
    for j in range(len(temp_addresses)):
        if ((ADDRESSES[i],temp_addresses[j]) in connections) or ((temp_addresses[j],ADDRESSES[i]) in connections) :
            inside_json = {"id":temp_addresses[j], "rssi": random.randint(-80,-30)}
            temp_dict['neighbor'].append(inside_json)
    temp_json['graph'].append(temp_dict)

print(temp_json)

G = nx.Graph()
for graph in temp_json['graph']:
    G.add_node(graph['id'])
    for j in graph['neighbor']:
        weight = 0
        for t in temp_json['graph']:
            if t['id'] == j['id']:
                for w in t['neighbor']:
                    if w['id'] == graph['id']:
                        weight = w['rssi']
        if weight == 0 :
            print("error")
            continue
        weight = (j['rssi'] + weight)/2
        G.add_edge(graph['id'], j['id'], weight = j['rssi'])
        # G.add_edge(graph['id'], j['id'])
nx.draw(G, with_labels=True ,font_weight='bold')


main = nx.Graph()
main.add_nodes_from(sorted(G.nodes(data=True)))
main.add_edges_from(G.edges(data=True))
nx.draw(main, with_labels=True ,font_weight='bold')


_tree = nx.bfs_tree(main, list(main.nodes)[2]).to_undirected()
nx.draw(_tree, with_labels=True ,font_weight='bold')

tree = nx.Graph()
tree.add_nodes_from(sorted(_tree.nodes(data=True)))
tree.add_edges_from(_tree.edges(data=True))
plt.figure()
nx.draw(tree, with_labels=True ,font_weight='bold')

print(tree.nodes)
print(tree.edges)