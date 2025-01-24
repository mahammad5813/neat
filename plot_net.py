import matplotlib.pyplot as plt
from network import Network

def plot_net(net: Network, show_disabled=False):
    
    class NodeDisplay:

        def __init__(self, id):
            self.id = id

            self.pos = [0,0]

            self.in_nodes = []

            self.pos_known = False


    center_y = 0

    connections = [connection for connection in net.connections]

    nodes = [NodeDisplay(i) for i in range(len(net.nodes))]

    n_inputs = net.n_inputs
    n_outputs = net.n_outputs

    for i, node in enumerate(nodes):
        for connection in connections:
            if connection.out_node == i:
                node.in_nodes.append(connection.in_node)

    y = center_y - (n_inputs-1)/2
    for i in range(n_inputs):
        nodes[i].pos = [0,y]
        nodes[i].pos_known = True
        y += 1


    temp_nodes = [node for node in nodes[n_inputs+n_outputs:]]

    while len(temp_nodes)>0:

        for node in temp_nodes:
            ahead = True
            for input in node.in_nodes:
                if not nodes[input].pos_known:
                    ahead=False
                    break

            if ahead:
                nodes[node.id].pos[0] = max([nodes[input].pos[0] for input in node.in_nodes])+1
                nodes[node.id].pos[1] = sum([nodes[input].pos[1] for input in node.in_nodes])/len(node.in_nodes)
                nodes[node.id].pos_known = True
                temp_nodes.remove(node)




    y = center_y - (n_outputs-1)/2
    x_max = max([node.pos[0] for node in nodes])+1

    for i in range(n_inputs, n_inputs+n_outputs):
        nodes[i].pos = [x_max,y]
        nodes[i].pos_known = True
        y+=1


    plot_x = [node.pos[0] for node in nodes]
    plot_y = [node.pos[1] for node in nodes]

    plt.scatter(plot_x, plot_y, s=100)
    
    arrow_head_width = 0.04

    for connection in connections:

        in_node = connection.in_node
        out_node = connection.out_node

        in_node_pos = nodes[in_node].pos
        out_node_pos = nodes[out_node].pos

        dx = out_node_pos[0]-in_node_pos[0]
        dy = out_node_pos[1]-in_node_pos[1]

        plt.arrow(in_node_pos[0], in_node_pos[1], dx, dy, head_width = arrow_head_width, color='black')

    if show_disabled:
        for d_connection in net.disabled_connections:
            in_node = d_connection.in_node
            out_node = d_connection.out_node

            in_node_pos = nodes[in_node].pos
            out_node_pos = nodes[out_node].pos

            dx = out_node_pos[0]-in_node_pos[0]
            dy = out_node_pos[1]-in_node_pos[1]

            plt.arrow(in_node_pos[0], in_node_pos[1], dx, dy, head_width = arrow_head_width, color='red')
        
    plt.show()


if __name__=="__main__":
    pass
