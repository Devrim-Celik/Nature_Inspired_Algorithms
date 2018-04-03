import matplotlib.pyplot as plt
from random import shuffle

from functions_week1 import *

# TODO:
# * harder task
# * boxplot or something with multiple runs for each setup
# * add description to function_week1 to explain what each is for and how
#   its is done

# Task: You have multiple Items I_1, ..., I_N, each having
# a value V_1, ..., V_N and a corresponding Weight W_1, ..., W_N.
# The task is, given a maximum weight, find a combination of the objects
# so that you maximize the value while not overstepping the weight limit.

# Assumption: We can have each item only once


# Setup
if __name__ == "__main__":
    # dictionary with items, values and weights
    ITEMS_DIC = {"small_coins": [10, 1000], "big_coins": [100, 2000], \
    "gold_bars": [300, 4000], "rings": [1,5000], "gold_bucket":[200,5000]}
    # maximum weight
    MAX_WEIGHT = 400
    # available modes for finding neighbors
    MODES = ["linear", "square"]

    for mode in MODES:
        # --- First Choice Hill Climbing
        best_setup, value_history = first_choice_hill_climbing(ITEMS_DIC, MAX_WEIGHT, mode=mode)
        # values for best bag setup
        bag, weight, value = best_setup

        print("[+] First Choice Hill Climbing with mode '{}': Bag={}, \
        Weight={}, Value={}".format(mode, bag, weight, value))

        # plot value history
        plt.figure("V_HIS")
        plt.title("History of 'Value', First Choice Hill Climbing, mode: {}".format(mode))
        plt.ylabel("Value")
        plt.xlabel("Iterations")
        plt.plot(value_history)
        plt.show()

        # --- Default Hill Climbing
        best_setup, value_history = hill_climbing(ITEMS_DIC, MAX_WEIGHT, mode=mode)
        # values for best bag setup
        bag, weight, value = best_setup

        print("[+] Default Hill Climbing with mode '{}': Bag={}, Weight={}, \
        Value={}".format(mode, bag, weight, value))

        # plot value history
        plt.figure("V_HIS")
        plt.title("History of 'Value', Default Hill Climbing, mode: {}".format(mode))
        plt.ylabel("Value")
        plt.xlabel("Iterations")
        plt.plot(value_history)
        plt.show()
