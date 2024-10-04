 # -*- coding: utf-8 -*-

from random import randint
import numpy as np

from numpy import floor
import operator

import pandas as pd
import time

from Vehicle import Vehicle
from Message import message

vehicle_number = 10; #1~103, 10
vehicle_power_number = 13;
vehicle_data_number = 103;
max_comm_range= 4
relay_power_loss = 1
power_weight = []

    
def ideal_2PC_compare(v1, v2):
    #score1 = v1.get_score();
    #score2 = v2.get_score();
    return v1.get_score() < v2.get_score();

def real_2PC_compare(v1, v2):
    result0 = 0;
    result1 = 0;
    for t in range(vehicle_power_number):
        #print(v1.vid, v2.vid, t)
        result0 += (v1.share0_of_power[t] - v1.share_of_neighbors[v2.vid][t]) * power_weight[t];  #模拟计算v1的score
        result1 += (v2.share0_of_power[t] - v2.share_of_neighbors[v1.vid][t]) * power_weight[t];  #v2的score   #其实应该是v1.sop-v1.son  v2.  - v2.  
    #result0 += v1.random_int
    result1 += v2.random_share  #Just to confirm again: Since each comparison value includes the destination's randomint, when propagating, the previous random_int should be eliminated first. If it is the first node, it should not be eliminated?, If it is the last node, then it should be eliminated during the final recording
    return result1 - result0; #which equals to (score1 - score2) + r

def real_compare_my_2neighbors(vid, v1, v2): #Node vid, compare the sizes of its two neighboring nodes v1 and v2.
    result0 = 0;
    result1 = 0;
    for t in range(vehicle_power_number):
        #print(v1.vid, v2.vid, t)
        result0 +=  v1.share1_of_power[t] - v1.share_of_nn[vid][v2.vid][t] 
        result1 +=  v2.share1_of_power[t] - v2.share_of_nn[vid][v1.vid][t] 
    return result0 < result1;   

def select_max(leader_candidate, v_list):
    power_list = [];
    for i in range(len(leader_candidate)):
        power_list.append(v_list[leader_candidate[i]].get_score());
    arr1 = np.array(power_list)
    return np.argmax(arr1)
    
def sort_neighbors(vid):#, leader_candidate, scores
    #vlist[i].neighbor_list, vlist[i].neighbor_scores, 
    #if len(leader_candidate) == 1:
    #    return 0
    can_list = []
    maxn = 0; 
    for i in vlist[vid].neighbor_list:
        vlist[vid].neighbor_scores[i] = 0
    for i in vlist[vid].neighbor_list:
        for j in vlist[vid].neighbor_list:
            if i!= j:
                b = real_compare_my_2neighbors(vid, vlist[i], vlist[j])
                x = (1 + vlist[vid].neighbor_power_compare[i])
                y = (1 + vlist[vid].neighbor_power_compare[j])
                if b:
                    vlist[vid].neighbor_scores[i] -= x
                    vlist[vid].neighbor_scores[j] += y
                else:
                    vlist[vid].neighbor_scores[i] += x
                    vlist[vid].neighbor_scores[j] -= y
                #print(leader_candidate[maxn], leader_candidate[i], b)
    return 0



def get_distance(vi, vj):
    distance = -1;
    if vi == vj:
        return -1;
    if abs(vi - vj) < 2:
        distance = 1;
    else:
        return floor(abs(vi - vj)/2);
    return distance


def sort_candidates(candidate_find):
    return candidate_find[1]

def vehicle_data_load():
    EVs_url = 'ElectricCarData_Clean_sortBrand_num.csv'
    df = pd.read_csv(EVs_url, header=0)
    #print('Dimensions of the Training set:',df.shape)
    #print('Label distribution Training set:')
    #print(df['BodyStyle'].value_counts())

    '''
    print('Training set:')
    for col_name in df.columns:
        if df[col_name].dtypes == 'object' :
            unique_cat = len(df[col_name].unique())
            print("Feature '{col_name}' has {unique_cat} categories".format(col_name=col_name, unique_cat=unique_cat))

    print()
    '''
    #print('Distribution of categories in service:')
    #print(df['service'].value_counts().sort_values(ascending=False).head())

    from sklearn.preprocessing import LabelEncoder,OneHotEncoder
    categorical_columns=['Brand', 'Model', 'RapidCharge', 'PowerTrain', 'PlugType', 'BodyStyle', 'Segment']

    df_categorical_values = df[categorical_columns]

    #print(df_categorical_values.head())
    df_categorical_values_enc=df_categorical_values.apply(LabelEncoder().fit_transform)

    #print(df_categorical_values.head())
    #print('--------------------')
    #print(df_categorical_values_enc.head())

    newdf = df.copy()
    for col in categorical_columns:
        newdf.drop(col, axis=1, inplace=True)

    newdf = newdf.join(df_categorical_values_enc)

    X = newdf.iloc[:, :-1]
    Y = newdf.iloc[:, -1]
    
    w = [0.210 ,0.007 ,0.001 ,0.019 ,0.002 ,0.554 ,0.000 ,-0.008 ,-0.001 ,1.342 ,0.102 ,-0.596 ,0.007 , -9.038]
    
    return np.array(X), np.array(Y), w


# Initialize the vehicle list
vlist = []
v_data, v_label, power_weight = vehicle_data_load()
for i in range(vehicle_number):
    vn = Vehicle(i, v_data[i], vehicle_number, vehicle_power_number, power_weight); #内存上是否是同一个v
    vlist.append(vn);

# Generate vehicle network topology
# Let's assume a simple network where i nodes are connected to i+1,i+2, and so on from 0 to 10
for i in range(vehicle_number):
    if i == 0:
        vlist[i].set_neighbors([i+1, i+2]);
    elif i == 1:
        vlist[i].set_neighbors([i-1, i+1, i+2]);
    elif i == vehicle_number-2:
        vlist[i].set_neighbors([i-1, i-2, i+1]);
    elif i == vehicle_number-1:
        vlist[i].set_neighbors([i-1, i-2]);    
    else:
        vlist[i].set_neighbors([i-1, i-2, i+1, i+2]);
    print("The neighbors of node ", i, " is ", vlist[i].neighbor_list);
print()

# Deploy secret sharing scheme for each node
# Generate shares for each node first, then generate its neighbors list
# For brevity, assume secure channels between nodes and everyone knows each other in the cluster
for i in range(vehicle_number):
    vlist[i].generate_share(randint(0, 65535));
    #print("share 0 of node ", i, " is ")
    #for t in range(vehicle_power_number):
    #    print(" ", vlist[i].share0_of_power[t], end="");
    #print("share 1 of node ", i, " is ")
    #for t in range(vehicle_power_number):
    #    print(" ", vlist[i].share1_of_power[t], end="");

    # Deliver the share to neightbors, and initialize the nei_list for each neighbors
    for j in vlist[i].neighbor_list:
        vlist[j].share_of_neighbors[i] = vlist[i].share1_of_power;
        vlist[i].share_of_nn[j] = {};
        
for i in range(vehicle_number):
    for j in vlist[i].neighbor_list:    
        for s in vlist[j].neighbor_list:  #not j
            # Redeliver another shares to the two-step neighbors
            vlist[s].share_of_nn[j][i] = vlist[i].share0_of_power #vlist[s].share_of_nn[j].append({i : vlist[i].share0_of_power})

ideal_power_sort_list = []
for i in range(vehicle_number):
    print("The power of node ", i, " is ")
    for t in range(vehicle_power_number):
        print(" ", vlist[i].power[t], end="")
    print(" = ", vlist[i].get_score())
    ideal_power_sort_list.append((i, vlist[i].get_score()))
     
# A secure comparision using ideal functionality
print("#######################")
print("In ideal world: ")
print("Local comparison in first round is: ")
leader_candidate = {}
leader = {}
for i in range(vehicle_number): 
    leader_candidate[i] = []
    for j in vlist[i].neighbor_list: 
        if ideal_2PC_compare(vlist[i], vlist[j]):
            leader_candidate[i].append(j);
    if len(leader_candidate[i]) == 0:
        leader[i] = -1;
        print("Node ", i, " is local leader.")
    else:
        tmp = select_max(leader_candidate[i], vlist);
        print("leader of node ", i, " is ", leader_candidate[i][tmp])
        leader[i] = leader_candidate[i][tmp];
        
#print(leader)
ideal_power_sort_list = sorted(ideal_power_sort_list, key = lambda node:node[1])
ideal_max_node_id = ideal_power_sort_list[-1][0]
print("Global leader selection is: Node", ideal_max_node_id)

# Design secure comparison protocol for real-world participants
print("#######################")
print("In real world: ")
T1 = time.time()

for i in range(vehicle_number): 
    #leader_candidate[i] = []
    for j in vlist[i].neighbor_list: 
        delta = real_2PC_compare(vlist[i], vlist[j])
        vlist[i].neighbor_power_compare[j] = delta
        

#Initialize the messages
power_sumup = 0
candidate_find = []
for i in range(vehicle_number):
    vlist[i].message_list_recv.append(message(i, max_comm_range, vlist[i].random_int + vlist[i].random_share)) #vlist[i].random_share 只是为了代码方便，因为第一轮发消息代码重用会导致多减一次
    power_sumup += vlist[i].get_score()
cluster_average_power = power_sumup / vehicle_number

# N-round propagation
# The current problem is that only the largest point can be found correctly, and subsequent points are prone to disorder in order. The simplest way is to repeat the above process twice. At the end of each session, all candidates broadcast their scores, with the highest being the CH selected for that session
# Another method, more direct, is to record the difference between each comparison and propagate it, then finally recover the sum of the differences, and sort the CHS based on this final value. However, this will inevitably leak information about power and require each node to attach a random number.
# But in the end, there is a need for comparison, so either all values are added with the same random number, or the random number can be eliminated in the end, which requires a third party to distribute the random number, or all nodes will eventually make the random number public.

for t in range(max_comm_range+1):
    if len(candidate_find) == 2:
        break
    for i in range(vehicle_number):
        #for j in vlist[i].message_list_recv:
        score, flag = vlist[i].update_list()
        if flag != False:
            candidate_find.append((vlist[i], score, t))
            #vlist[i].message_list_send = vlist[i].message_list_recv
        #else:
        #    vlist[i].message_list.append(i)
        #if len(vlist[i].message_list_recv) == vehicle_number:
        #    candidate_find += 1
    for i in range(vehicle_number): #每个节点i在当轮执行下列操作
        for j in vlist[i].message_list_send: #对于手中每个待发送的消息j
            if j.ttl == 0:
                continue
            else:
                j.ttl -= 1
                for y in vlist[i].neighbor_list: #For each neighbor y of node i
                    if y != j.vid:
                        vlist[y].message_list_recv.append(message(j.vid, j.ttl, j.power_sum + vlist[i].neighbor_power_compare[y] - vlist[i].random_share)) #Weight update rule: The weight of the message itself+the weight of the edge connected to the neighbor - the random number of this node
                    continue;
        vlist[i].message_list_send.clear()
#check the result
candidate_find.sort(key=sort_candidates,reverse=True)
bigger_ind = candidate_find[0][1]

if len(candidate_find) != 0:
    for i in range(len(candidate_find)):
        print("CH candidates found:", candidate_find[i][0].vid, " with score ", candidate_find[i][1],  " (origin is ", vlist[candidate_find[i][0].vid].get_score(), " in ", candidate_find[i][2],  " rounds. ") # " (origin is ", original_scores[candidate_find[i][0].vid], ") in "
        if candidate_find[i][1] > bigger_ind:
            print("Wrong!")
        bigger_ind = candidate_find[i][1] 
else:
    print("No candidate find!")
print()
if ideal_max_node_id == candidate_find[0][0].vid:
    print(":) Best match! Find the most powerful one: Node ", ideal_max_node_id)
else:
    print(":( Oops! We do not find the most powerful node in a secure way...")
print()

CHs_average_power = (candidate_find[0][0].get_score() + candidate_find[1][0].get_score() )/2
print("Clustre averange power: ", cluster_average_power, ", CHs averange power: ", CHs_average_power)

T2 = time.time()
print('Runtime:%s ms' % ((T2 - T1)*1000))
