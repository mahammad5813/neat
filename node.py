import random
from activations import activation_name_map
class Node:
    def __init__(self, id, value=0, bias=0, activation='relu'):
        self.id = id
        self.value = value
        if bias:
            self.bias = bias
        else:
            self.bias = random.uniform(-1,1)
        self.activation = activation_name_map[activation]
        self.deter_i = 0
        self.determined = False
        

    def __str__(self):
        return "Node "+ str(self.__dict__)