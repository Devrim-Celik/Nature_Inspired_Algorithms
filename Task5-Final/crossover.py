import numpy as np
import random



def vrp_crossover(parents, cap, demands):
    """
    Crossover: From two parents, create two children. We build them by randomly
    taking rows from the two parents. This way, the
    truck capacity demand is not violated. The problem is,
    that this way, the city demand constraint may be violated. To correct this,
    we employ a correction funciton, which fixes this problem in a rather
    optimal fashion.
    """
    # create an empty child list
    children = [None]*len(parents)

    # for each parent pair
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i+1]

        ### create two (faulty) children
        child1, child2 = create_children(parent1, parent2)

        #### fix children
        # we create a list of net values, telling us for each child:
        #       how much does each city has delivered to it, in relation to
        #       what was expected [net_list_child1/net_list_child2]

        # first look how much they deliver each city
        child1_city_deliverd = np.sum(child1, axis=0)
        child2_city_deliverd = np.sum(child2, axis=0)

        # from this delivered material, subtract what was demanded to see the
        # net values
        net_list_child1 = [child1_city_deliverd[i]-demands[i] for i in range(len(demands))]
        net_list_child2 = [child2_city_deliverd[i]-demands[i] for i in range(len(demands))]

        # first fix all the "columns" (amounts to cities delivered) which
        # have positive values (too much supplied), then the ones which have
        # negative values (not enough)
        # we do not mix them, since it is easier first to offload the trucks
        # to make space

        # child1 positive values
        for idx, val in enumerate(net_list_child1):
            if val > 0:
                child1[:,idx] = too_much(child1[:,idx], val)
        # child1 negative values
        for idx, val in enumerate(net_list_child1):
            if val < 0:
                child1[:,idx] = too_few(child1[:,idx], val, cap, np.sum(child1, axis=1))


        # child2 positive values
        for idx, val in enumerate(net_list_child2):
            if val > 0:
                child2[:,idx] = too_much(child2[:,idx], val)
        # child2 negative values
        for idx, val in enumerate(net_list_child2):
            if val < 0:
                child2[:,idx] = too_few(child2[:,idx], val, cap, np.sum(child2, axis=1))


        children[i] = child1
        children[i+1] = child2

    return children

def create_children(parent1, parent2):
    """
    for even truck numbers, child1 copies parent1 & child2 copies parent2

    for odd truck nubmers, child1 copies parent2 & child2 copies parent1
    """
    # create two empty children array
    child1 = np.zeros(parent1.shape)
    child2 = np.zeros(parent1.shape)

    # for every truck with number i
    for i in range(child1.shape[0]):

        # for even truck numbers, child1 copies parent1 and child2 copies
        # parent2
        if random.uniform(0,1) >= 0.5:
            child1[i,:] = parent1[i,:]
            child2[i,:] = parent2[i,:]
        # for uneven vice versa
        else:
            child1[i,:] = parent2[i,:]
            child2[i,:] = parent1[i,:]

    return child1, child2


def too_much(col, overflow):
    """
    we know that this city was delivered $overflow too much. we now go through
    a list of all the truck delivering this city (sorted from smallest
    amount to biggest amount) and make them stop delivering until we have
    the right amount
    """
    while overflow != 0:
        smallest = 10000000000
        idx_min = 0
        #print("NEW")
        for t, load in enumerate(col):
            if load > 0:
                if load < smallest:
                    smallest, idx_min = load, t
        #print(idx_min)
        #print(col[idx_min])
        if overflow >= col[idx_min]:
            overflow -= col[idx_min]
            col[idx_min] = 0
        else:
            col[idx_min] -= overflow
            overflow = 0
    return col

def too_few(column, missing, capacity, truck_cargo):

    #eine city hat zu wenig und soll mehr zugefahren kriegen
    missing *= -1
    #die trucks die eh schon fahren kriegen den rest aufgeteilt
    for index, i in enumerate(column):
        difference = 0
        if i != 0 and missing > 0:
            difference = capacity[index]-column[index]
            if difference >= missing:
                column[index] += missing
                truck_cargo[index] += missing
                missing = 0
                break
            else:
                column[index] += difference
                truck_cargo[index] += difference
                missing -= difference

    #wenn noch was gebraucht wird nimm einen der alles nehmen kann
    if missing > 0:
        for index, i in enumerate(column):
            difference = capacity[index]-truck_cargo[index]
            if (difference) >= missing:
                column[index] += missing
                truck_cargo[index] += missing
                missing = 0
                break


    #erstelle eine liste mit allen differenzen, also wie viel jeder truck noch aufnehmen kann
    difference_list = [i-j for i,j in zip(capacity, truck_cargo)]
    # wenn ein truck nicht alles nehmen kann, dann teile auf die wenigst möglichen auf
    while missing > 0:
        # finde den truck mit der meisten übriggebliebenen kapazität
        max_idx = argmax(difference_list)
        # gebe diesem truck so viel mit wie er noch nehmen kann
        column[max_idx] += difference_list[max_idx]
        truck_cargo[max_idx] += difference_list[max_idx]
        #ziehe das von difference ab für unsere bedingung
        missing -= difference_list[max_idx]
        #setze auf null damit man den nächstgrößeren truck findet
        difference_list[max_idx] = 0


    return column
