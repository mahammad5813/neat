from network import Network
from connection import Connection
from node import Node
import random
from plot_net import plot_net

net = Network(5,2)

# net.print_cons()

for _ in range(50):
    net.add_node(random.choice(net.connections), random.uniform(-1,1))
    net.add_connection(random.choice(net.nodes).id, random.choice(net.nodes).id, random.uniform(-1,1))
    net.add_connection(random.choice(net.nodes).id, random.choice(net.nodes).id, random.uniform(-1,1))
    net.add_connection(random.choice(net.nodes).id, random.choice(net.nodes).id, random.uniform(-1,1))


net.print_cons()
print("\n")
net.print_nodes()


inputs = [0.54, 0.23, 0.75, 0.01, 0.89]
for n in net.run(inputs):
    print(n)

net.print_nodes()

print(len(net.connections))
print(len(net.nodes))
plot_net(net, show_disabled=False)
