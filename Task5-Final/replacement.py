import numpy as np

def replacement(old_pop, new_pop, mode="delete-all", n=None,
    based_on_fitness=True, fitness_old=[], fitness_new=[]):
    """
    Replacement of old population through new population

    Args:
        old_pop: old population
        new_pop: new population
        mode: chosen from options: ['delete-all', 'steady-state']
            * 'delete-all': replace part of old population through new ones
            * 'steady-state': replace n members of the old population by n
                members of the new population
        n: number of members to be replaced if 'stead-state' is chosen as mode
        based_on_fitness: boolean, if chosen, you will replace the n worst
            members of the old population the n best members of the new
            population
        fitness_old: corresponding fitness values for the old population
        fitness_new: corresponding fitness values for the new population

    Returns:
        population: replaced population
    """

    if mode == "delete-all":
        if fitness_old == []:
            raise ValueError("[!] 'fitness_old' has to be filled!")

        population = [None]*len(old_pop)

        # take over all members of new population
        for i in range(len(new_pop)):
            population[i] = new_pop[i]

        # list of members sorted from best to worse
        sorted_members = [member for _, member in sorted(zip(fitness_old, old_pop), key=lambda pair: -pair[0])][:n]

        # fill up rest with best of old population
        for i in range(len(new_pop), len(old_pop)):
            population[i] = sorted_members[i-len(new_pop)]

        return population

    # if not, check if n was supplied
    if n is None:
        raise Exception("[-] Please supply n when using steady-state modes!")

    # generate list for the resulting population, starting as the old_pop
    population = old_pop[:]

    # here we generate lists of indx for the old population and values to
    # replace them with from the new population

    # for the "steady-state mode" ...
    if mode == "steady-state" and not based_on_fitness:
        # choose n random indexes from the old_pop
        # replace=False ensures no duplicates
        indx_list = np.random.choice(range(len(old_pop)), size=n, replace=False)
        # and n random values from new_pop
        value_list = np.random.choice(new_pop, size=n, replace=False)

    elif mode == "steady-state" and based_on_fitness:
        """
        check if fitness lsits are defined
        build two correpsonding lists of indx and values to replace
        """

        if len(fitness_old) != len(old_pop) or len(fitness_new) != len(new_pop):
            raise Exception("""[-] Both 'fitness_old' and 'fitness_new' need to be
            the same length as 'old_pop' and 'new_pop'""")
        # check if sort the right way
        # sort populations, based on their fitness score as sort key
        # (for old population we want the n worst member, thus default sorted
        # [small to big] does just fine, for the new population we want the
        # n best member, thus we include a -)
        # for old population, sort the indexes to be replace
        # for new population, sort the member to replace with
        indx_list = [indx_old for _, indx_old in \
            sorted(zip(fitness_old, range(len(old_pop))), \
            key=lambda pair: pair[0])][:n]
        value_list = [member for _, member in \
            sorted(zip(fitness_new, new_pop), \
            key=lambda pair: -pair[0])][:n]

    # now that we got our lists, simply replace them
    for indx, val in zip(indx_list, value_list):
        population[indx] = val

    return population
