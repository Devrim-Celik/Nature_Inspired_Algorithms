"""
Module for executing Differential Evolution Algorithm on Task 4
"""

import math
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from de_functions import differential_evolution

################################################################################
# --- CLASSES REQUIRED FOR TASK
################################################################################
class Plant:
    """
    Class for defining Plants
    Attributes
        kWh                 kWh per plant
        cost                cost per plant
        maximum             maximum number of plants that can be used
    """
    def __init__(self, kWh, cost, maximum):
        self.kWh = kWh
        self.cost = cost
        self.maximum = maximum

class Market:
    """
    Class for defining Markets
    Attributes
        max_price       maximum price at which customers buy
        max_demand      maximum demand
    """
    def __init__(self, max_price, max_demand):
        self.max_price = max_price
        self.max_demand = max_demand

################################################################################
# --- FUNCTIONS REQUIRED FOR TASK
################################################################################
def calculate_cost(x, plant):
    """
    Calculates costs for a given amount of require energy and type of energy
        plant
    Args:
        x               required energy in [kW]
        plant           type of plant
    Returns:
        0               if required energy < 0
        -1              if required energy cant theoretically be produced by
                            type of plant
                        else cost to produce required energy
    """
    # if required energy < 0
    if x <= 0:
        return 0
    # if required enery > maximum number of plant type * energy produced by each
    elif x > plant.kWh * plant.maximum:
        return 10000000000000 #float("infinity")
    # else we are "fine"
    return math.ceil(x / plant.kWh) * plant.cost



def calculate_demand(price, market):
    """
    Calculates deman for a given price and a type of market
    Args:
        price               demand
        market              type of market
    Returns:
        0                   if the price is bigger than the maximum price
                                of the market type
        market.max_demand   if price is free (ignore negative price)
        else                TODO
    """
    # price is too high for the maket
    if price > market.max_price:
        return 0
    # price is for free
    elif price <= 0:
        return market.max_demand
    # TODO Explanation
    return market.max_demand - price**2 * market.max_demand / market.max_price**2


def profit_fitness(setup):
    """
    Given by the task. Used as our fitness function to be maximised.
    """
    # assign components of setup
    e_list = setup[0:3]
    s_list = setup[3:6]
    p_list = setup[6:10]

    purchasing_cost = max([sum(s_list) - sum(e_list), 0]) * 0.6

    production_cost = 0
    revenue = 0

    for i in range(3):
        production_cost += calculate_cost(e_list[i], plant_list[i])
        revenue += min([calculate_demand(p_list[i], market_list[i]), s_list[i]])

    cost = production_cost + purchasing_cost

    profit = revenue - cost

    return profit

################################################################################
# --- MAIN - SETUP
################################################################################
if __name__=="__main__":
    SINGLE = True
    SURFACE = False

    path = "picture/"
    if not os.path.exists(path):
        os.makedirs(path)


    # SETUP
    plant1 = Plant(50000.0, 10000.0, 100.0)
    plant2 = Plant(600000.0, 80000.0, 50.0)
    plant3 = Plant(4000000.0, 400000.0, 3.0)
    plant_list = [plant1, plant2, plant3]

    market1 = Market(0.45, 2000000.0)
    market2 = Market(0.25, 30000000.0)
    market3 = Market(0.2, 20000000.0)
    market_list = [market1, market2, market3]


    # PARAMETERS
    population_size     =   [50, 100, 200, 500, 1000]
    minimum_values      =   [0, 0, 0, 0, 0, 0, 0, 0, 0]
    maximum_values      =   [50000.0, 600000.0, 4000000.0, 2000000.0,
                                30000000.0, 20000000.0, 0.45, 0.25, 0.2]
    F                   =   np.linspace(0.4, 1.0, 13)   # usually in [0.4 ; 1]
    Cr                  =   np.linspace(0.0, 0.5, 11)   # usually smaller values
    modules             =   ["BINOMIAL", "EXPONENTIAL"]


    if SINGLE:
        population, avg, best, worst = differential_evolution(population_size[3],
        minimum_values, maximum_values, F[0], Cr[2], profit_fitness, 150,
        modules[0], True)


        max_value = max(best)*1.154
        min_value = min(worst)+min(worst)*0.154

        plt.figure("Differential Evolution")
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=15)
        plt.title("Differential Evolution", fontsize=20)
        plt.ylabel("Profit", fontsize=20)
        plt.xlabel("Generation", fontsize=20)
        plt.plot(best, lw=3, label="Best Individual")
        plt.plot(worst, lw=3, label="Worst Individual")
        plt.plot(avg, lw=3, label="Average Individual")
        plt.legend()
        plt.savefig(path+"best.png")

        plt.figure("Best Individual")
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=15)
        plt.title("Best Individual", fontsize=20)
        plt.ylabel("Profit", fontsize=20)
        plt.xlabel("Generation", fontsize=20)
        plt.plot(best, lw=3)
        plt.savefig(path+"best.png")

        plt.figure("Worst Individual")
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=15)
        plt.title("Worst Individual", fontsize=20)
        plt.ylabel("Profit", fontsize=20)
        plt.xlabel("Generation", fontsize=20)
        plt.plot(worst, lw=3)
        plt.savefig(path+"worst.png")

        plt.figure("Average Individual")
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=15)
        plt.title("Average Individual", fontsize=20)
        plt.ylabel("Profit", fontsize=20)
        plt.xlabel("Generation", fontsize=20)
        plt.plot(avg, lw=3)
        plt.savefig(path+"average.png")

        #plt.show()



    if SURFACE:
        # create array to save the value for different setups
        # 1.dimension: F dimension with length(F)
        # 2.dimension: Cr diension with lenth(Cr)
        # 3.dimension: size 3 --> for average, best & worst value for this run
        surface_data = np.zeros((len(F), len(Cr), 3))

        for indx_F in range(len(F)):
            for indx_Cr in range(len(Cr)):
                print("+++++++++ {}, {} ++++++++++".format(indx_F, indx_Cr))
                population, avg, best, worst = differential_evolution(
                population_size[3], minimum_values, maximum_values, F[indx_F],
                Cr[indx_Cr], profit_fitness, 25, modules[0], True)

                # set corresponding data
                surface_data[indx_F, indx_Cr, :] = avg[-1], best[-1], worst[-1]


        # Grid and Average Data
        X, Y = np.meshgrid(Cr, F)
        Z = surface_data[:, :, 1]

        fig = plt.figure("SURFACE")

        ax = plt.axes(projection='3d')
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
        ax.set_xlabel('Cross-Ratio')
        ax.set_ylabel('F')
        ax.set_zlabel('Profit');
        ax.set_title('SURFACE: F vs Cross-Ratio');

        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)

        plt.show()
