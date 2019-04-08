import random
import numpy as np

def mutate(matrix, capacity):
    """
    The function gets a child and the capacity of the trucks and performs
    the mutation step. Mutation is done by switching the cargo of two different
    trucks. To do so we need to look for two trucks of which the smaller one
    has enough space to carry all that was originally carried by the larger
    one.

    Args
        matrix: a child containing trucks and cities and what is carried
        capacity: how much the trucks can carry in total
    Return
        matrix: the mutated child
    """
    cargo = np.sum(matrix, axis=1)

    # so we enter the while loop
    mini, maxi = 0, 1

    while mini < maxi:
        truck1 = random.randint(0,len(capacity)-1)
        truck2 = random.randint(0,len(capacity)-1)

        mini = min(capacity[truck1],capacity[truck2])
        maxi = max(cargo[truck1], cargo[truck2])

    temp = matrix[truck1]
    matrix[truck1] = matrix[truck2]
    matrix[truck2] = temp

    return matrix
