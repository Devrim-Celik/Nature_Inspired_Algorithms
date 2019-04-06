import numpy as np




def vrp_crossover(parents, cap, demands):
    """
    Crossover: From two parents, create two children. The way that is done,
    is simply saying, that the first child, has the 0,2,4,... truck plan
    from parent 1 and the 1,3,5,... truck plan from parent 2. This way, the
    truck capacity demand is not violated. The problem is,
    that this way, the city demand constraint may be violated. To correct this,
    we employ a correction funciton, which fixes this problem in a rather
    optimal fashion.
    """

    # create an empty child list
    children = np.zeros((len(parents)))

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
        for idx, val in net_list_child1:
            if val > 0:
                child1[:,idx] = too_much(child1[:,idx], val)
        # child1 negative values
        #for idx, val in net_list_child1:
            #if val < 0:
                #child1[:,idx] = too_few(child1[:,idx], val)


        # child2 positive values
        for idx, val in net_list_child2:
            if val > 0:
                child2[:,idx] = too_much(child2[:,idx], val)
        # child2 negative values
        #for idx, val in net_list_child2:
            #if val < 0:
                #child2[:,idx] = too_few(child2[:,idx], val)


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
        if i%2==0:
            child1[i,:] = parent1[i,:]
            child2[i,:] = parent2[i,:]
        # for uneven vice versa
        elif i%2==1:
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
        idx_min = np.argmin(col)
        overflow -= col[idx_min]
        col[idx_min] = 0

    return col
