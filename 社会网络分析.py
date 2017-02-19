#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HaiShenMing
# 2017/2/8 19:10
import _hread

import networkx as nx
import csv
import matplotlib.pyplot as plt

def extraction_data(file):
    with open(file, 'r', encoding='utf-8') as f:
        file = csv.reader(f)
        headers = next(file)
        user_id_list = []
        from_node_list = []
        congruent_relationship = {}
        for row in file:
            user_id_list.append(row[1])
            from_node_list.append(row[5])
            congruent_relationship[row[0]] = row[1]
    return user_id_list,from_node_list,congruent_relationship


def data_conversion(dic,lis):
    from_user_id = []
    for node in lis:
        if node == '-1':
            from_user_id.append('0')
        else:
            from_user_id.append(dic[node])
    return from_user_id


def get_relationship(file):
    user_id,from_node,congruent_relationship = extraction_data(file)
    from_user_id = data_conversion(congruent_relationship,from_node)
    # relationship = creat_relation(from_user_id,user_id)
    relationship = list(zip(from_user_id,user_id))
    return relationship

file1 = get_relationship('zhuanfa_user.csv')
file2 = get_relationship('zhuanfa_user1.csv')
file = file1 + file2
for i in file:
    print(i)
print(len(file))
graph = nx.DiGraph(name="test")
for row in file:
    graph.add_edge(*row)
    print(row)

test_G = [(1,2),(2,3),(3,1)]
G = nx.DiGraph(name="test")
for row in test_G:
    G.add_edge(*row)

nx.draw(G)
plt.show()
# plt.savefig("picture_networkx.png")