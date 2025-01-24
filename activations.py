
def relu(x):
    return max(0,x)

def linear(x):
    return x

activation_name_map = {
    "relu": relu,
    "linear": linear
}