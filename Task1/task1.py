import matplotlib.pyplot as plt
from random import shuffle

from functions_week1 import *

# TODO:
# * multiple runs with avg value, weight and time for each
# * boxplot or something with multiple runs for each setup
# * add description to function_week1 to explain what each is for and how
#   its is done
# * include time for measurement of compuational efficiency
# * smarter, harder setup
# * instead of just adding them up, save history value for later distribution

# Task: You have multiple Items I_1, ..., I_N, each having
# a value V_1, ..., V_N and a corresponding Weight W_1, ..., W_N.
# The task is, given a maximum weight, find a combination of the objects
# so that you maximize the value while not overstepping the weight limit.

# Assumption: We can have each item only once


# Setup
if __name__ == "__main__":
    # nr of runs
    RUNS = 1000
    # plot? print?
    do_plot = False
    do_print = False

    # dictionary with items, values and weights
    ITEMS_DIC = {"small_coins": [10, 1000], "big_coins": [100, 2000],
    "gold_bars": [300, 4000], "rings": [1,5000], "gold_bucket":[200,5000]}

    # second, harder setup
    # NOTE: "gold_block" fucks up default hill climibng, since the weight
    # blocks all further improvements
    ITEMS_DIC2 = {"small_coins": [10, 1000], "big_coins": [100, 2000],
    "gold_bars": [300, 4000], "rings": [1,5000], "gold_bucket":[200, 5000],
    "gold_disk": [73, 3000], "gold_tooth": [7, 500], "gold_nugget": [25, 200],
    "iron_block": [125, 4000], "amulet": [2, 100]}

    # maximum weight
    MAX_WEIGHT = 400
    # available modes for finding neighbors
    MODES = ["linear", "square"]

    # for saving all value across all runs with form: [Weight, Value, Time]
    history = {"FCHC_linear": [0,0,0], "FCHC_square": [0,0,0],
    "DHC_linear": [0,0,0], "DHC_square": [0,0,0]}


    # run multiple runs to get average runs (since we have randomness)
    for _ in range(RUNS):
        for mode in MODES:
            # --- First Choice Hill Climbing
            best_setup, value_history = first_choice_hill_climbing(ITEMS_DIC2, MAX_WEIGHT, mode=mode)
            # values for best bag setup
            bag, weight, value = best_setup
            # add to history
            history["FCHC_"+mode][0] += weight
            history["FCHC_"+mode][1] += value
            #history["FCHC_"+mode][2] += time

            if do_print:
                print("[+] First Choice Hill Climbing with mode '{}':\n Bag={}, Weight={}, Value={}".format(mode, bag, weight, value))

            if do_plot:
                # plot value history
                plt.figure("V_HIS")
                plt.title("History of 'Value', First Choice Hill Climbing, mode: {}".format(mode))
                plt.ylabel("Value")
                plt.xlabel("Iterations")
                plt.plot(value_history)
                plt.show()

            # --- Default Hill Climbing
            best_setup, value_history = hill_climbing(ITEMS_DIC2, MAX_WEIGHT, mode=mode)
            # values for best bag setup
            bag, weight, value = best_setup
            # add to history
            history["DHC_"+mode][0] += weight
            history["DHC_"+mode][1] += value
            #history["DHC_"+mode][2] += time

            if do_print:
                print("[+] Default Hill Climbing with mode '{}':\n Bag={}, Weight={}, Value={}".format(mode, bag, weight, value))

            if do_plot:
                # plot value history
                plt.figure("V_HIS")
                plt.title("History of 'Value', Default Hill Climbing, mode: {}".format(mode))
                plt.ylabel("Value")
                plt.xlabel("Iterations")
                plt.plot(value_history)
                plt.show()

    # normalize values to get averages (in new lists)
    FCHC_LIN = [x/RUNS for x in history["FCHC_linear"]]
    FCHC_SQ = [x/RUNS for x in history["FCHC_square"]]
    DHC_LIN = [x/RUNS for x in history["DHC_linear"]]
    DHC_SQ = [x/RUNS for x in history["DHC_square"]]

    print(FCHC_LIN)
    print(FCHC_SQ)
    print(DHC_LIN)
    print(DHC_SQ)
