from random import randint
import numpy as np
        
class Vehicle:
    
    #share1 = -1;
    
    def __init__(self, vid, vehicle_number, vehicle_power_number, vehicle_data_number, power_weight):
        self.vid = vid;
        self.neighbor_list = [];
        self.neighbor_power_compare = {};
        self.neighbor_scores = {};
        self.power = [];
        self.data = []; 
        self.share_of_neighbors = {}; #An array that records the shares sent by surrounding nodes.
        self.share_of_nn = {};
        
        self.vehicle_number = vehicle_number;
        self.vehicle_power_number = vehicle_power_number;
        self.vehicle_data_number = vehicle_data_number
        self.power_weight = power_weight
        
        self.share0_of_power = [];
        self.share1_of_power = [];
        for i in range(vehicle_power_number):
            self.power.append(randint(1, 100));
            #self.share_of_neighbors[i] = [];
        self.message_list_recv = []
        self.message_list_send = []
        
        self.CCH1_is_neighbor = False;
        self.CCH2_is_neighbor = False;
        self.near_relay_node = {}
        
        self.is_candidate_CCH = False
        self.reachable_list = {}
        
        self.node_weight = 0
        self.random_share = randint(1, 100)
        self.random_int = randint(1, 100)
        
        #self.reachable_list[self.vid] = 1
        
    def __init__(self, vid, data, vehicle_number, vehicle_power_number, power_weight):
        self.vid = vid;
        self.neighbor_list = [];
        self.neighbor_power_compare = {};
        self.neighbor_scores = {};
        self.power = [];
        self.data = []; 
        self.share_of_neighbors = {}; 
        self.share_of_nn = {};
        
        self.vehicle_number = vehicle_number;
        self.vehicle_power_number = vehicle_power_number;
        self.vehicle_data_number = len(data)
        self.power_weight = power_weight
        
        self.share0_of_power = [];
        self.share1_of_power = [];
        for i in range(self.vehicle_power_number):
            self.power.append(int(data[i]));
            #self.share_of_neighbors[i] = [];
        self.message_list_recv = []
        self.message_list_send = []
        
        self.CCH1_is_neighbor = False;
        self.CCH2_is_neighbor = False;
        self.near_relay_node = {}
        
        self.is_candidate_CCH = False
        self.reachable_list = {}
        
        self.node_weight = 0
        self.random_share = randint(1, 255)
        self.random_int = randint(1, 255)
        
    
    def set_neighbors(self, list):
        self.neighbor_list = list;
        
    def add_neighbor(self, nvid):
        self.neighbor_list.append(nvid);
        
    def generate_share(self, r):
        for t in range(self.vehicle_power_number):
            self.share0_of_power.append(r);
            self.share1_of_power.append(self.power[t] - r)

    def get_score(self):
        score = 0;
        #for data in self.power:
        #    score += data;
        for i in range(self.vehicle_power_number):
            score += self.power[i] * self.power_weight[i];
        return score
    '''
    def add_relay_node(self, vi):
        distance = get_distance(vi, self.id)
        if self.near_relay_node.has_key(vi):
            self.near_relay_node[vi] = max(distance, vj.near_relay_node[vi]);
        else:
            self.near_relay_node[vi] = distance;
        return;
    '''  
    def update_list(self):
        for j in self.message_list_recv:
            if j.vid not in self.reachable_list:
                self.reachable_list[j.vid] = j.power_sum - self.random_share # add a alpha coe? #j.ttl #这里的random_int是否重复了，好像不重复，因为这是自己记录的一个值，不会继续往下传，往后传的是消息本身的值
                self.message_list_send.append(j)
        self.message_list_recv.clear()
        if len(self.reachable_list) == self.vehicle_number:
            if self.is_candidate_CCH == True:
                return (0, False)
            else:
                power = 0 #self.random_int
                for j in self.reachable_list:
                    power += self.reachable_list[j]
                self.is_candidate_CCH = True
                self.com_power = power
                #calculate the power sum
                return (power, True)
        else:
            return (0, False)