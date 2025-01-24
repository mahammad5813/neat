import random
from connection import Connection
from node import Node
from activations import activation_name_map
g_innov = 0



class Network:
    def __init__(self, n_inputs, n_outputs):
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs

        self.nodes = [Node(i) for i in range(n_inputs+n_outputs)]
        for node in self.nodes[n_inputs:n_inputs+n_outputs]:
            node.activation = activation_name_map["linear"]

        # self.connections = [Connection(i, random.randint(n_inputs, n_inputs+n_outputs-1), random.uniform(0,1), enabled=True, innov=i) for i in range(n_inputs)]
        self.connections = []
        self.disabled_connections = []


    def update_inputs(self, inputs: list[float]):
        for i in range(self.n_inputs):
            self.nodes[i].value = inputs[i]
            self.nodes[i].determined = True

    def add_connection(self, in_node, out_node, value, innov):
        if out_node<self.n_inputs:
            print("Input nodes can't be output node for a connection")
            return
        
        if self.n_inputs <= in_node < self.n_inputs+self.n_outputs:
            print("Output nodes can't be input node for a connection")
            return
        
        if in_node > len(self.nodes)-1 or out_node > len(self.nodes)-1:
            print("Node doesn't exist")
            return
        
        for connection in self.connections:
            if connection.in_node == in_node and connection.out_node==out_node:
                print("Connection exists")
                return
            
        new_connection = Connection(in_node, out_node, value, True, innov)
        
        self.connections.append(new_connection)

        if not self.order_and_check(order=True):
            self.connections.remove(new_connection)
            print("The new connection created a circular dependency and got removed")
            return False
        return True

    
    def add_node(self, connection: Connection, value, innov):
        node_id = len(self.nodes)
        self.nodes.append(Node(node_id))

        self.add_connection(connection.in_node, node_id, value, innov)
        self.add_connection(node_id, connection.out_node, connection.weight, innov+1)

        connection.enabled = False
        self.connections.remove(connection)
        self.disabled_connections.append(connection)

        self.order_and_check(order=True)

    def mutate(self, innov, mut_rate):
        if random.uniform(0,1)>mut_rate:
            return
        
        mut_type = random.randint(0,2)
        
        if mut_type == 0:

            while True:
                if self.add_connection(random.choice(self.nodes[:self.n_inputs]+self.nodes[self.n_inputs+self.n_outputs:]).id, random.choice(self.nodes[self.n_inputs:]).id, random.uniform(-1,1), innov):
                    innov += 1
                    break
        
        elif mut_type == 1:
            self.add_node(random.choice(self.connections), random.uniform(-1,1), innov)
            innov += 2
        
        else:
            con_i = random.randint(0,len(self.connections)-1)
            self.connections[con_i].weight += self.connections[con_i].weight*random.uniform(-0.2,0.2)

        return innov

    def order_and_check(self, order=False):
        connections = [connection for connection in self.connections]
        nodes = [Node(i) for i in range(len(self.nodes))]
        op_order = []

        for node in nodes[:self.n_inputs]:
            node.determined = True



        while len(connections)>0:

            prev_len = len(connections)

            for connection in connections:
                in_node = nodes[connection.in_node]
                out_node = nodes[connection.out_node]

                if in_node.determined:
                    connections.remove(connection)
                    op_order.append(connection)
                    out_node.determined = True
                    for connection_check in connections:
                        if connection_check.out_node == connection.out_node:
                            out_node.determined = False
                            break

                    if out_node.determined:
                        self.nodes[out_node.id].deter_i = len(op_order)-1
                    
            
            if len(connections) == prev_len:
                return False
            
        if order:
            self.connections = op_order
        
        return True
    
    def run(self, inputs):
        self.update_inputs(inputs)
        connections = [connection for connection in self.connections]
        nodes = [Node(i, value=node.value, bias=node.bias) for i, node in enumerate(self.nodes)]
        for i, node in enumerate(self.nodes):
            nodes.append(Node(i, value=node.value, bias=node.bias))
            nodes[-1].activation = node.activation

        for node in nodes[:self.n_inputs]:
            node.determined = True

        for i, connection in enumerate(connections):
            in_node = nodes[connection.in_node]
            out_node = nodes[connection.out_node]

            out_node.value += in_node.value*connection.weight
            if out_node.deter_i == i:
                out_node.value += out_node.bias
                out_node.value = out_node.activation(out_node.value)

        return nodes[self.n_inputs:self.n_inputs+self.n_outputs]

    def get_connection(self, in_node, out_node):
        for connection in self.connections:
            if connection.in_node == in_node and connection.out_node == out_node:
                return connection
            
        print("Connection doesn't exist")

    def print_nodes(self):
        for node in self.nodes:
            print(node)

    def print_cons(self, show_disabled=False):
        print("Enabled connections:")
        for con in self.connections:
            print(con)
        if show_disabled:
            print("Disabled connections")
            for con in self.disabled_connections:
                print(con)


if __name__ == "__main__":
    pass
