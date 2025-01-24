class Connection:
    def __init__(self, in_node, out_node, weight, enabled, innov):

        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innov = innov

    def __str__(self):
        return "Connection "+ str(self.__dict__)