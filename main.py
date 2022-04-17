import numpy as np
import networkx as nx
import random
import pandas as pd

G = nx.Graph()

glam_1 = pd.read_csv('instaglam_1.csv')
for user, friend in zip(glam_1['userID'], glam_1['friendID']):
    G.add_edge(user, friend)
    G.add_edge(user, friend)


print(G)
new_edges={}
for edge_1 in G.edges:
    for edge_2 in G.edges:
        if edge_1 != edge_2:
            if edge_1[0] == edge_2[0]:
                new_edges[(edge_1[1],edge_2[1])] = 1 if not ((edge_1[1],edge_2[1]) in new_edges) else (new_edges[(edge_1[1],edge_2[1])]+1)
            elif edge_1[0] == edge_2[1]:
                new_edges[(edge_1[1],edge_2[0])] = 1 if not ((edge_1[1],edge_2[0]) in new_edges) else (new_edges[(edge_1[1],edge_2[0])]+1)
            elif edge_1[1] == edge_2[1]:
                new_edges[(edge_1[0],edge_2[0])] = 1 if not ((edge_1[0],edge_2[0]) in new_edges) else (new_edges[(edge_1[0],edge_2[0])]+1)
            elif edge_1[1] == edge_2[0]:
                new_edges[(edge_1[0],edge_2[1])] = 1 if not ((edge_1[0],edge_2[1]) in new_edges) else (new_edges[(edge_1[0],edge_2[1])]+1)


G0=nx.Graph()
glam0 = pd.read_csv('instaglam_1.csv')
for user, friend in zip(glam0['userID'], glam0['friendID']):
    G0.add_edge(user, friend)
    G0.add_edge(user, friend)


G11 = nx.Graph(G)
G12 = nx.Graph(G)
for edge_1, edge_2 in new_edges.keys():
    if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 11:
        G11.add_edge(edge_1, edge_2)
    if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 12:
        G12.add_edge(edge_1, edge_2)

print(G11)
print(G0)
i=0

for edge in G11.edges:
    if edge in G0:
        i=i+1
print(f'{i} for G11')
i=0
for edge in G12.edges:
    if edge in G0:
        i=i+1
print(f'{i} for G12')


#see how many freind needed to convert
# G2 = nx.Graph(G)
# G3 = nx.Graph(G)
# G4 = nx.Graph(G)
# G5 = nx.Graph(G)
# G6 = nx.Graph(G)
# G7 = nx.Graph(G)
# G8 = nx.Graph(G)
# G9 = nx.Graph(G)
# G10 = nx.Graph(G)
# G11 = nx.Graph(G)
# G12 = nx.Graph(G)
# G13 = nx.Graph(G)
# G14 = nx.Graph(G)
# G15 = nx.Graph(G)
# G16 = nx.Graph(G)
# G17 = nx.Graph(G)
# G18 = nx.Graph(G)
# G19 = nx.Graph(G)
# G20= nx.Graph(G)
# G21= nx.Graph(G)
# G22 = nx.Graph(G)
# G23 = nx.Graph(G)
# G24 = nx.Graph(G)
# G25 = nx.Graph(G)
# G26 = nx.Graph(G)
# G27 = nx.Graph(G)
#
#
# for edge_1, edge_2 in new_edges.keys():
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 2:
#         G2.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 3:
#         G3.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 4:
#         G4.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 5:
#         G5.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 6:
#         G6.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 7:
#         G7.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 8:
#         G8.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 9:
#         G9.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 10:
#         G10.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 11:
#         G11.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 12:
#         G12.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 13:
#         G13.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 14:
#         G14.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 15:
#         G15.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 16:
#         G16.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 17:
#         G17.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 18:
#         G18.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 19:
#         G19.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 20:
#         G20.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 21:
#         G21.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 22:
#         G22.add_edge(edge_1, edge_2)
#     if (new_edges[(edge_1, edge_2)] + new_edges[(edge_2, edge_1)])/2 > 23:
#         G23.add_edge(edge_1, edge_2)
#
# print(f'{G2},G2')
# print(f'{G3},G3')
# print(f'{G4},G4')
# print(f'{G5},G5')
# print(f'{G6},G6')
# print(f'{G7},G7')
# print(f'{G8},G8')
# print(f'{G9},G9')
# print(f'{G10},G10')
# print(f'{G11},G11')
# print(f'{G12},G12')
# print(f'{G13},G13')
# print(f'{G14},G14')
# print(f'{G15},G15')
# print(f'{G16},G16')
# print(f'{G17},G17')
# print(f'{G18},G18')
# print(f'{G19},G19')
# print(f'{G20},G20')
# print(f'{G21},G21')
# print(f'{G22},G22')
# print(f'{G23},G23')
