# -*- coding: utf-8 -*-

class message():
    def __init__(self, vid, max_comm_range, power_sum):
        self.vid = vid;
        self.ttl = max_comm_range;
        self.type = 0;  #0: out of range; 1: CH candidate;  2: CH's broadcast node;
        self.data = []; #or using tuple
        
        self.power_sum = power_sum