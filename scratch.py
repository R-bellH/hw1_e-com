import pandas as pd
import networkx as nx

class User:
  id=0
  listen={}
  bought={}
  def __init__(self, userID,artists):
    self.id=userID
    for artist in artists:
      self.bought[artist]=False
      self.listen[artist] = 0

  def update_plays(self, artist,plays):
    self.listen[artist]=plays

G_1 = nx.Graph()
good_art=[989, 16326, 144882, 194647]
spotifly=pd.read_csv('spotifly.csv')
users={}
for userid in spotifly['userID']:
  users[userid] = (User(userid,good_art))
pref={}
# for user in users.values():
#   for cuser, artist, plays in zip(spotifly['userID'], spotifly[' artistID'],spotifly['#plays']):
#     if artist in good_art:
#       if user.id==cuser:
#         user.update_plays(artist,plays)

G_1 = nx.Graph()
glam_1 = pd.read_csv('instaglam_1.csv')
for node, friend in zip(glam_1['userID'], glam_1['friendID']):
    G_1.add_node(node,user=users[node]) #attach the class User to the node in the graph
    G_1.add_node(friend,user=users[friend]) #attach the class User to the node in the graph
    G_1.add_edge(node, friend)
    G_1.add_edge(node, friend)

G0 = nx.Graph()
glam0 = pd.read_csv('instaglam_1.csv')
for node, friend in zip(glam0['userID'], glam0['friendID']):
    G0.add_node(node,user=users[node]) #attach the class User to the node in the graph
    G0.add_node(friend,user=users[friend]) #attach the class User to the node in the graph
    G0.add_edge(node, friend)
    G0.add_edge(node, friend)
for user1 in G0.nodes:
  for user2 in nx.neighbors(G0,user1):
    if G0.has_edge(user1, user2) and not G_1.has_edge(user1, user2):
        print("user1")
        print(f'in deg={len(nx.neighbors(G_1,user1))}')


