# Secure_comparison_between_vehicles_in_VANETs

## Overview 
A simple privacy-preserving comparision protocol for VANETs based on additive secret sharing scheme. Our protocol is constructed by end-to-end 2PC comparison, that is, in an one-hop VANETs where nodes only communicate with its neighbors. 

We construct this protocol to enable an secure cluster head (CH) selection phase based on the private vehicle information of each vehicle, such as the vehicle type, communication power and location. Those with the highest scores (i.e. the most powerful vehicles that are reachable for others) would be selected as the CHs. 

## Environment
Python 3.8.19, using numpy and pandas to process the dataset.

## Output

```
The neighbors of node  0  is  [1, 2]
The neighbors of node  1  is  [0, 2, 3]
The neighbors of node  2  is  [1, 0, 3, 4]
The neighbors of node  3  is  [2, 1, 4, 5]
The neighbors of node  4  is  [3, 2, 5, 6]
The neighbors of node  5  is  [4, 3, 6, 7]
The neighbors of node  6  is  [5, 4, 7, 8]
The neighbors of node  7  is  [6, 5, 8, 9]
The neighbors of node  8  is  [7, 6, 9]
The neighbors of node  9  is  [8, 7]

The power of node  0  is 
  9  150  335  188  350  5  36057  0  70  1  1  2  6 =  10.541
The power of node  1  is 
  6  180  400  193  540  5  55000  1  61  1  0  2  6 =  10.560000000000002
The power of node  2  is 
  3  240  425  197  850  4  125000  1  92  1  0  2  7 =  10.492999999999999
The power of node  3  is 
  6  190  280  231  450  5  67358  1  90  1  0  2  6 =  11.023000000000003
The power of node  4  is 
  5  200  380  228  610  5  81639  1  96  1  0  2  6 =  11.240000000000002
The power of node  5  is 
  5  200  365  237  590  5  79445  1  91  1  0  2  6 =  11.361000000000002
The power of node  6  is 
  6  180  410  188  550  5  57500  1  60  1  0  2  6 =  10.496
The power of node  7  is 
  6  190  295  219  470  5  69551  1  95  1  0  2  6 =  10.845
The power of node  8  is 
  4  210  320  270  510  5  93800  1  93  1  0  2  6 =  11.641000000000002
The power of node  9  is 
  4  210  335  258  540  5  96050  1  94  1  0  2  6 =  11.487000000000004
#######################
In ideal world: 
Local comparison in first round is: 
leader of node  0  is  1
leader of node  1  is  3
leader of node  2  is  4
leader of node  3  is  5
leader of node  4  is  5
Node  5  is local leader.
leader of node  6  is  8
leader of node  7  is  8
Node  8  is local leader.
leader of node  9  is  8
Global leader selection is: Node 8
#######################
In real world: 
CH candidates found: 8  with score  970.723000000009  (origin is  11.641000000000002  in  4  rounds. 
CH candidates found: 5  with score  967.9230000000243  (origin is  11.361000000000002  in  3  rounds. 
CH candidates found: 4  with score  966.7130000000434  (origin is  11.240000000000002  in  3  rounds. 
CH candidates found: 3  with score  964.5429999999978  (origin is  11.023000000000003  in  3  rounds. 
CH candidates found: 7  with score  962.7629999999917  (origin is  10.845  in  4  rounds. 
CH candidates found: 1  with score  959.9129999999459  (origin is  10.560000000000002  in  4  rounds. 
CH candidates found: 6  with score  959.2730000001065  (origin is  10.496  in  3  rounds. 
CH candidates found: 2  with score  959.2429999999549  (origin is  10.492999999999999  in  4  rounds. 

:) Best match! Find the most powerful one: Node  8

Clustre averange power:  10.968700000000002 , CHs averange power:  11.501000000000001
Runtime:0.9992122650146484 ms
```

## Dataset
This project utilizes One Electric Vehicle Dataset  (https://www.kaggle.com/datasets/geoffnel/evs-one-electric-vehicle-dataset) as the sensitive vehicle dataset, where the weights of each attribute are the optimal weight parameters of a linear regression model trained with the price of vehicles as the target value. 

## Possible drawbacks
The current version requires multiple rounds of communication to find the true maximum node, and subsequent nodes may not appear in the score order. In addition, only linear combinations of privacy features are currently considered.

## What is the purpose of the code

This project will serve as the implementation of an extended application in paper "RUPT-FL: Robust Two-layered Privacy-preserving Federated Learning Framework with Unlinkability for IoV".


