import random
import numpy as np

def mutate(matrix, capacity):

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
