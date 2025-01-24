import random
from network import Network
from plot_net import plot_net
import time

def get_innov(node_in, node_out, innovs, g_innov):
    for innov in innovs:
        if innov[0] == node_in and innov[1] == node_out:
            return innov[2]
        
    return g_innov+1

n_in = 4
n_out = 2
con_gid = 0
node_gid = n_in+n_out-1

node_innovs = []
con_innovs = []

print(node_gid)

net1 = Network(n_in, n_out)
net2 = Network(n_in, n_out)

node_in = random.choice(list(range(n_in))+list(range(n_in+n_out, len(net1.nodes)-1)))
node_out = random.choice(range(n_in,len(net1.nodes)-1))

innov = get_innov(node_in, node_out, con_innovs, con_gid)

if innov > con_gid:
    con_gid = innov
    con_innovs.append((node_in, node_out, innov))

net1.add_connection(node_in, node_out, random.uniform(-1,1), innov)

net1.print_cons()
print(con_gid)

innov = get_innov(node_in, node_out, con_innovs, con_gid)
con_gid = max(innov, con_gid)
net2.add_connection(node_in, node_out, random.uniform(-1,1), innov)
net2.print_cons()
print(con_gid)
