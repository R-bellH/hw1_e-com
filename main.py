# -*- coding: utf-8 -*-
"""hw1_e-com.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K43sbYvZ5IJCXXTE3qm6_gCM0vR__npQ
"""

import networkx as nx
import pandas as pd
from scipy.stats import gamma


class User:
    id = 0
    listen = {}

    def __init__(self, userID, artists):
        self.id = userID
        for artist in artists:
            self.listen[artist] = 0

    def update_plays(self, artist, plays):
        self.listen[artist] = plays


def increment_times(G0):
    G1 = increment_connection(G0)
    G2 = increment_connection(G1)
    G3 = increment_connection(G2)
    G4 = increment_connection(G3)
    G5 = increment_connection(G4)
    G6 = increment_connection(G5)
    return [G0, G1, G2, G3, G4, G5, G6]


def infect(times, artist, influncers):
    G0 = patient_zero(times[0], influncers)
    G1 = increment_people(times[1], G0, artist)
    G2 = increment_people(times[2], G1, artist)
    G3 = increment_people(times[3], G2, artist)
    G4 = increment_people(times[4], G3, artist)
    G5 = increment_people(times[5], G4, artist)
    G6 = increment_people(times[6], G5, artist)
    infected = 0
    for i in G6.nodes:
        infected += G6.nodes[i]['weight']
    return infected


def patient_zero(G0, influncers):
    Gt = G0.copy()
    for node in influncers:
        Gt.nodes[node]['weight'] = 1
    return Gt


def increment_connection(G):
    Gt = G.copy()
    precision = 4
    for node1 in G.nodes:
        for node2 in G.nodes:
            if len(list(nx.common_neighbors(G, node1, node2))) > 0:
                if G.has_edge(node1, node2):
                    if Gt[node1][node2]['weight'] < 1:
                        Gt[node1][node2]['weight'] = Gt[node1][node2]['weight'] + (
                            1 - round(G[node1][node2]['weight']) * p_gamma(node1, node2, G, precision), 5)
                    if Gt[node1][node2]['weight'] > 1:
                        print(f"bad news!! {(node1, node2)} weight = {Gt[node1][node2]['weight']}")
                        Gt[node1][node2]['weight'] = 1
                else:
                    weighted = p_gamma(node1, node2, G, precision)
                    if weighted >= 10 ** -precision:
                        Gt.add_edge(node1, node2, weight=weighted)
    # remove self_loops
    Gt.remove_edges_from(nx.selfloop_edges(Gt))

    return Gt


def p_gamma(node1, node2, G, precision):
    overlap = 0
    neig1 = sum(map(lambda i: G[node1][i]['weight'], dict(G[node1])))
    neig2 = sum(map(lambda i: G[node1][i]['weight'], dict(G[node2])))
    for node in nx.common_neighbors(G, node1, node2):
        overlap = overlap + ((G[node][node2]['weight']) * (G[node1][node]['weight']))
    n_overlap = overlap / (neig2 + neig1 - overlap)
    return round(gamma.pdf(n_overlap * 30, a=3.8, loc=0.5) / 12, precision)


def increment_people(G, Gi, artist):
    Gt = G.copy()
    nodes = [(node, Gi.nodes[node]) for node in Gi.nodes]
    Gt.add_nodes_from(nodes)
    for node in Gt.nodes:
        buy(node, Gi, Gt, artist)
    return Gt


def buy(node1, G, Gt, artist):
    bt = 0
    nt = sum(map(lambda i: G[node1][i]['weight'], dict(G[node1])))
    for node2 in nx.neighbors(G, node1):
        if node1 != node2:
            bt = bt + G.edges[(node1, node2)]['weight'] * G.nodes[node2]['weight']
    if G.nodes[node1]['user'].listen[artist] == 0:
        Gt.nodes[node1]['weight'] = G.nodes[node1]['weight'] + (1 - G.nodes[node1]['weight']) * (bt / nt)
    else:
        Gt.nodes[node1]['weight'] = G.nodes[node1]['weight'] + (1 - G.nodes[node1]['weight']) * (
                (bt * G.nodes[node1]['user'].listen[artist]) / (nt * 1000))


def harmonic(G):
    """
  harmonic centrality
  """
    dists = dict(nx.all_pairs_shortest_path_length(G0, 6))
    HC_score = {}
    for node in G.nodes:
        HC_score[node] = harmonic_inner(G, node, dists)
    return HC_score


def harmonic_inner(G, node1, dists):
    sum_d = 0.0
    for node2 in G.nodes:
        if node2 != node1:
            if node2 in dists[node1].keys():
                sum_d = sum_d + (1 / dists[node1][node2] ** 2)
    sum_d /= nx.number_of_nodes(G)
    return sum_d


def hill_climb(times, users, artist):
    team = []
    for i in range(5):
        team.append(hill_climb_step(times, users, artist, team))
    return team


def hill_climb_step(times, users, artist, team):
    kim = (None, 0)
    for user in users:
        if user not in team:
            team_build = team.copy()
            team_build.append(user)
            anna_zack = (user, infect(times, artist, team_build))
            kim = max(kim, anna_zack, key=lambda x: x[1])
    return kim[0]


def better_than_kim(times, annas, artist):
    possible_teams = []
    for anna in annas:
        possible_teams.append((anna, infect(times, artist, [anna])))
    possible_teams = sorted(possible_teams, key=lambda x: x[1])[:20]
    possible_teams = [anna[0] for anna in possible_teams]
    possible_teams = choose_sets(possible_teams, 5)
    for team in possible_teams:
        kim_possible = max((team, infect(times, artist, team)), key=lambda x: x[1])
    kim_possible=[kim[0] for kim in kim_possible]
    return kim_possible


def choose_sets(lst, k):
    ''' Input: lst,
        Output: a list of all k-length sub-lists '''
    if len(lst) == k:
        return [lst]
    if k == 0:
        return [[]]
    if k == 1:
        return [[i] for i in lst]
    sub_lst1 = choose_sets(lst[1:], k - 1)
    for i in sub_lst1:
        i.append(lst[0])
    sub_lst2 = choose_sets(lst[1:], k)
    final_lst = []
    final_lst.extend(sub_lst1)
    final_lst.extend(sub_lst2)
    return final_lst


def read_Graphs(G0):
    times = [G0]
    for i in range(1, 7):
        df = pd.read_csv(f'prob_instaglam {i}.csv')
        G = nx.from_pandas_edgelist(df, 'source', 'target', 'weight')
        times.append(G)
    nodes = [(node, G0.nodes[node]) for node in G0.nodes]
    for G in times:
        G.add_nodes_from(nodes)
    return times


"""
Enter your ids below (if you are submitting alone DO NOT CHANGE ID2) and execute the code.
The list of ids you get is the list of artists you need to promote.
"""

####################
ID1 = '315694281'
ID2 = '315775585'
####################

x = (int(ID1[-1]) + int(ID2[-1])) % 5
y = (int(ID1[-2]) + int(ID2[-2])) % 5
options = [(70, 150), (989, 16326), (144882, 194647), (389445, 390392), (511147, 532992)]
y = (y + 1) % 5 if x == y else y
print("your artists are:")
print(*options[x], *options[y])
artists = [*options[x], *options[y]]
print(artists)

# init cell
G0 = nx.Graph()
spotifly = pd.read_csv('spotifly.csv')
users = {}
for userid in spotifly['userID']:
    users[userid] = (User(userid, artists))
    # G0.add_node(userid, user=users[userid], weight=0)
pref = {}
for user in users.values():
    for cuser, artist, plays in zip(spotifly['userID'], spotifly[' artistID'], spotifly['#plays']):
        if artist in artists:
            if user.id == cuser:
                user.update_plays(artist, plays)

G0 = nx.Graph()
glam0 = pd.read_csv('instaglam0.csv')

# add actual edges
for node, friend in zip(glam0['userID'], glam0['friendID']):
    G0.add_node(node, user=users[node], weight=0)  # attach the class User to the node in the graph
    G0.add_node(friend, user=users[friend], weight=0)  # attach the class User to the node in the graph
    G0.add_edge(node, friend, weight=1)
    G0.add_edge(node, friend, weight=1)
# remove self_loops
G0.remove_edges_from(nx.selfloop_edges(G0))

"""evaluate best influences """

HC_scores = harmonic(G0)
# keep the top 100 central nodes
top100 = list(sorted(HC_scores.items(), key=lambda item: item[1], reverse=True))[:100]
top100 = [user[0] for user in top100]
print(f'top10 = {top100[:10]}')
times = read_Graphs(G0)
# times=increment_times(G0)
data = []
for artist in artists:
    print(f'for artist = {artist}')
    hill_climb_team = hill_climb(times, top100, artist)
    print(f'hill_climb_team = {hill_climb_team}')
    kim_possible_team = better_than_kim(times, top100, artist)
    print(f'kim_possible_team = {kim_possible_team}')
    MIB = max(infect(times, artist, hill_climb_team), infect(times, artist, kim_possible_team),
              key=lambda item: item[1])
    data.append([artist, MIB[0]])
df = pd.DataFrame(data, columns=['Artists', [f'influences {i}' for i in range(5)]])
df.to_csv('./influences.csv')

"""just to evaluate the data"""
#
# G_1 = nx.Graph()
# good_art = [989, 16326, 144882, 194647]
# spotifly = pd.read_csv('spotifly.csv')
# users = {}
# for userid in spotifly['userID']:
#     users[userid] = (User(userid, good_art))
# pref = {}
#
# G_1 = nx.Graph()
# glam_1 = pd.read_csv('instaglam_1.csv')
# for node, friend in zip(glam_1['userID'], glam_1['friendID']):
#     G_1.add_node(node, user=users[node], weight=0)  # attach the class User to the node in the graph
#     G_1.add_node(friend, user=users[friend], weight=0)  # attach the class User to the node in the graph
#     G_1.add_edge(node, friend, weight=1)
#     G_1.add_edge(node, friend, weight=1)
#
# G0 = nx.Graph()
# glam0 = pd.read_csv('instaglam0.csv')
# for node, friend in zip(glam0['userID'], glam0['friendID']):
#     G0.add_node(node, user=users[node], weight=0)  # attach the class User to the node in the graph
#     G0.add_node(friend, user=users[friend], weight=0)  # attach the class User to the node in the graph
#     G0.add_edge(node, friend, weight=1)
#     G0.add_edge(node, friend, weight=1)
# hemol = []
# G0.remove_edges_from(nx.selfloop_edges(G0))
# # neighborhood overlap
# for user1 in G_1.nodes:
#     for user2 in nx.neighbors(G0, user1):
#         if not G_1.has_edge(user1, user2):
#             neig1 = [i for i in nx.neighbors(G_1, user1)]
#             neig2 = [i for i in nx.neighbors(G_1, user2)]
#             neig12 = 0
#             for i in neig1:
#                 if i in neig2:
#                     neig12 += 1
#             hemol.append(neig12 / (len(neig2) + len(neig1) - neig12))
# dist = np.arange(0.0, 1.0, 0.02)
# n = 50
# prec = np.zeros(n)
# for i in hemol:
#     for j in range(n):
#         if i <= dist[j]:
#             prec[j] = prec[j] + 1
#             break
# print(prec)
#
# hemol_all = []
# for user1 in G_1.nodes:
#     for user2 in G_1.nodes:
#         if not G_1.has_edge(user1, user2):
#             neig1 = [i for i in nx.neighbors(G_1, user1)]
#             neig2 = [i for i in nx.neighbors(G_1, user2)]
#             neig12 = 0
#             for i in neig1:
#                 if i in neig2:
#                     neig12 += 1
#             hemol_all.append(neig12 / (len(neig2) + len(neig1) - neig12))
# prec_all = np.zeros(n)
# for i in hemol_all:
#     for j in range(n):
#         if i <= dist[j]:
#             prec_all[j] = prec_all[j] + 1
#             break
# print(prec_all)
#
# # print plots for evaluation
# from scipy.stats import beta, gamma
# import matplotlib.pyplot as plt
#
# prec_all_clean = prec_all
# for i in range(len(prec)):
#     if prec_all_clean[i] < 20:
#         prec_all_clean[i] = 0
#
# p = np.true_divide(prec, prec_all_clean)
# p[np.isnan(p)] = 0.4
# p[np.isinf(p)] = 0.4
# print(p)
# p1 = p * 12
# y = dist * 30
# fig, axes = plt.subplots(figsize=(10, 10))
# x = np.linspace(0, 30, 1000)
#
# # Varying positional arguments
# a_b = 3.8
# b_b = 0.5
# gamma1 = gamma.pdf(x, a_b, b_b)
# plt.plot(x, gamma1, c='b')
#
# a_g = 3.9
# b_g = 0.5
# gamma2 = gamma.pdf(x, a_g, b_g)
# plt.plot(x, gamma2, c='r')
#
# plt.scatter(y, p1, s=20, c='g')
# plt.show()

# # make new graph list with 0.01 precision
# G1 = increment_connection(G0)
# print(f'done with G1')
# df = nx.to_pandas_edgelist(G1)
# df.to_csv(f'prob_instaglam_0.01 1.csv', index=False)
# G2 = increment_connection(G1)
# print(f'done with G2')
# df = nx.to_pandas_edgelist(G2)
# df.to_csv(f'prob_instaglam_0.01 2.csv', index=False)
# G3 = increment_connection(G2)
# print(f'done with G3')
# df = nx.to_pandas_edgelist(G3)
# df.to_csv(f'prob_instaglam_0.01 3.csv', index=False)
# G4 = increment_connection(G3)
# print(f'done with G4')
# df = nx.to_pandas_edgelist(G4)
# df.to_csv(f'prob_instaglam_0.01 4.csv', index=False)
# G5 = increment_connection(G4)
# print(f'done with G5')
# df = nx.to_pandas_edgelist(G5)
# df.to_csv(f'prob_instaglam_0.01 5.csv', index=False)
# G6 = increment_connection(G5)
# print(f'done with G6')
# df = nx.to_pandas_edgelist(G6)
# df.to_csv(f'prob_instaglam_0.01 6.csv', index=False)
