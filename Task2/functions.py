"""
This module provides multiple functions for Genetic Algorithms such as
combination or mutation functions
"""

import random
import numpy as np


def k_point_crossover(chrom1, chrom2, k=1, swap_p=0.5):
    """
    k Point Crossover

    Args
        chrom1: chromosome of parent 1
        chrom2: chromosome of parent 2
        k     : number of crossovers
        swap_p: swapping probability
    Returns
        offspring1: first offspring
        offspring2: second offspring
    """

    if k > (len(chrom1)-1) or k < 1:
        raise Exception("""[-] k was chosen to be {}, but k is only allowed to
            be chosen from the interval [1; {}]!""".format(k, len(chrom1)-1))


    # generate empty chromosomes for offsprings
    offspring1 = np.empty((len(chrom1),))
    offspring2 = np.empty((len(chrom1),))

    # randomly generate sections for crossover, by generating the indexing,
    # at which the next section start (returns a list)
    crossover_indx = random.sample(range(1, len(chrom1)), k) # vor dem value
    # for easier iteration later, add the amount of genes to this list, since
    # one can interprete it either as the end of our last section
    # or the "start" of the next (not exisiting) section
    crossover_indx.append(len(chrom1))
    # sort them, so we can iterate properly
    crossover_indx.sort()

    # iterator for gene reference
    gene = 0

    # k+1 because, e.g. if k=1, we have two sections
    for section in range(k+1):
        #print(section)
        # generate number between 0 and 1, responsible for deciding
        # whether to swap sections
        r = random.uniform(0, 1)

        # iterate through all genes in the current section
        while gene < crossover_indx[section]:
            # if r is smaller/equal than the swap probability, we want to swap
            if r <= swap_p:
                offspring1[gene] = chrom2[gene]
                offspring2[gene] = chrom1[gene]
            # else do not swap
            else:
                offspring1[gene] = chrom1[gene]
                offspring2[gene] = chrom2[gene]

            # reference next gene
            gene += 1

    return offspring1, offspring2


# ---


def uniform_crossover(chrom1, chrom2, swap_p=0.6):
    """
    Uniform Crossover

    Args
        chrom1: chromosome of parent 1
        chrom2: chromosome of parent 2
    Returns
        offspring1: first offspring
        offspring2: second offspring
    """

    # generate empty chromosomes for offsprings
    offspring1 = np.empty((len(chrom1),))
    offspring2 = np.empty((len(chrom1),))

    # iterate through the values (alleles) for each gene
    for i, (allele1, allele2) in enumerate(zip(chrom1, chrom2)):
        # generate number between 0 and 1, responsible for deciding
        # whether to swap allele1 and allele2
        r = random.uniform(0, 1)

        # if r is smaller/equal than the swap probability, we want to swap
        if r <= swap_p:
            offspring1[i] = allele2
            offspring2[i] = allele1
        # else do not swap
        else:
            offspring1[i] = allele1
            offspring2[i] = allele2

    return offspring1, offspring2


# ---


def mutation(chrom, allele_list, p_m=0.05):
    """
    Default Mutation

    Args
        chrom      : chromosome list
        allele_list: list of possible allele to mutate to
        p_m        : mutation probability
    Returns
        chrom      : mutated chromose list
    """

    for i in range(len(chrom)):
        # generate number between 0 and 1, responsible for deciding
        # whether to appply mutation
        r = random.uniform(0, 1)

        # if r is smaller/equal the mutation probability, mutate!
        if r <= p_m:
            # choose random allele from list of possible alleles
            chrom[i] = random.choice(allele_list)

    return chrom


# ---


def bitflip_mutation(chrom, p_m=0.05):
    """
    Bit-Flip Mutation

    Args
        chrom      : chromosome list
        p_m        : mutation probability
    Returns
        chrom      : mutated chromose list
    """

    for i in range(len(chrom)):
        # generate number between 0 and 1, responsible for deciding
        # whether to appply mutation
        r = random.uniform(0, 1)

        # if r is smaller/equal the mutation probability, mutate!
        if r <= p_m:
            # flip bit at position
            chrom[i] = 1 - chrom[i]

    return chrom


# ---


def replacement(old_pop, new_pop, n=None, fitness_old=[], fitness_new=[],
    based_on_fitness=True, mode="delete-all"):
    """
    TODO
    modes = ["delete-all", "steady-state", "steady-state-no-duplicates"]
    """
    # if mode is "delete-all", simply return the new population
    if mode == "delete-all":
        return new_pop

    # if not, check if n was supplied
    if n is None:
        raise Exception("[-] Please supply n when using steady-state modes!")

    # generate list for the resulting population, starting as the old_pop
    population = old_pop[:]

    # here we generate lists of indx for the old population and values to
    # replace them with from the new population

    # for the "steady-state mode" ...
    if mode == "steady-state":
        # choose n random indexes from the old_pop
        # replace=False ensures no duplicates
        indx_list = np.random.choice(range(len(old_pop)), size=n, replace=False)
        # and n random values from new_pop
        value_list = np.random.choice(new_pop, size=n, replace=False)

    elif mode == "steady-state-no-duplicates":
        """
        check if fitness lsits are defined
        build two correpsonding lists of indx and values to replace
        """
        pass

    # now that we got our lists, simply replace them
    for indx, val in zip(indx_list, value_list):
        population[indx] = val

    return population



x = [0,0,0,0,0,0,0,0]
y = [1,2,3,4,5,6,7,8]

k = replacement(x,y,n=3,mode="steady-state")
print(k)


# TODO replacement and selection
