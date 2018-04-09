import matplotlib.pyplot as plt
from functions_week1 import first_choice_hill_climbing, hill_climbing
import time

# TODO:
# * smarter, harder setup

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
    ITEMS_DIC = {
        "small_coins": [10, 1000],
        "big_coins": [100, 2000],
        "gold_bars": [300, 4000],
        "rings": [1, 5000],
        "gold_bucket": [200, 5000]
        }

    # second, harder setup
    # NOTE: "gold_block" fucks up default hill climibng, since the weight
    # blocks all further improvements
    ITEMS_DIC2 = {
        "small_coins": [10, 1000],
        "big_coins": [100, 2000],
        "gold_bars": [300, 4000],
        "rings": [1, 5000],
        "gold_bucket": [200, 5000],
        "gold_disk": [73, 3000],
        "gold_tooth": [7, 500],
        "gold_nugget": [25, 200],
        "iron_block": [125, 4000],
        "amulet": [2, 100]
        }

    # maximum weight
    MAX_WEIGHT = 400
    # available modes for finding neighbors
    MODES = ["linear", "square"]

    # for saving all value across all runs with form: [Weight, Value, Time]
    # for all but the first value we want to save each value to later plot a
    # distribution later on
    history = {
        "FCHC_linear": [0, [], [], []],
        "FCHC_square": [0, [], [], []],
        "DHC_linear": [0, [], [], []],
        "DHC_square": [0, [], [], []]
        }

    # run multiple runs to get average runs (since we have randomness)
    for _ in range(RUNS):
        for mode in MODES:
            start = time.time() * 1000  # Store the starting time in ms
            # --- First Choice Hill Climbing
            best_setup, value_history, nr_iter = first_choice_hill_climbing(
                ITEMS_DIC2,
                MAX_WEIGHT,
                mode=mode
                )
            end = time.time() * 1000  # Store the ending time in ms
            elapsed = end - start  # Calculate the execution time
            # values for best bag setup
            bag, weight, value = best_setup
            # add to history
            history["FCHC_"+mode][0] += weight
            history["FCHC_"+mode][1].append(value)
            history["FCHC_"+mode][2].append(elapsed)
            history["FCHC_"+mode][3].append(nr_iter)

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

            start = time.time() * 1000  # Store the starting time in ms
            # --- Default Hill Climbing
            best_setup, value_history, nr_iter = hill_climbing(
                ITEMS_DIC2,
                MAX_WEIGHT,
                mode=mode
                )
            end = time.time() * 1000  # Store the ending time in ms
            elapsed = end - start  # Calculate the execution time
            # values for best bag setup
            bag, weight, value = best_setup
            # add to history
            history["DHC_"+mode][0] += weight
            history["DHC_"+mode][1].append(value)
            history["DHC_"+mode][2].append(elapsed)
            history["DHC_"+mode][3].append(nr_iter)

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

    # normalize values to get averages (for non-list properties)
    for value_list in history.values():
        value_list[0] = value_list[0]/RUNS

    # lists, where we save all available lists of the current value for one
    # complete boxplot plot
    value_lists_final = []
    elapsed_per_iter_lists_final = []
    nr_iterations_lists_final = []

    for key, value in history.items():
        #print(key, value[0])
        # append all lists
        value_lists_final.append(value[1])
        # NOTE: we want the iteration per cycle, thus divide total number by
        #   number of cycles
        elapsed_per_iter_lists_final.append([total/nr for total, nr in zip(value[2], value[3])])
        nr_iterations_lists_final.append(value[3])

    # VALUE
    plt.figure("Value Distribution Boxplots", figsize=(20,10))
    plt.title("Value Distribution Boxplots with {} Runs".format(RUNS))
    plt.boxplot(value_lists_final)
    plt.xticks([1,2,3,4], ["FCHC-lin", "FCHC-sqr", "DHC-lin", "DHC-sqr"])
    plt.ylabel("Value")
    plt.savefig("values.png")

    # ELAPSED TIME PER CYCLE
    plt.figure("Elapsed Time per Iteration Distribution Boxplots", figsize=(20,10))
    plt.title("Elapsed Time per Iteration Distribution Boxplots with {} Runs".format(RUNS))
    plt.boxplot(elapsed_per_iter_lists_final)
    plt.xticks([1,2,3,4], ["FCHC-lin", "FCHC-sqr", "DHC-lin", "DHC-sqr"])
    plt.ylabel("Elapsed Time per Iteration [ms]")
    plt.savefig("time_per_iteration.png")

    # NUMBER OF ITERATIONS
    plt.figure("Number Iterations Distribution Boxplots", figsize=(20,10))
    plt.title("Number Iterations Distribution Boxplots with {} Runs".format(RUNS))
    plt.boxplot(nr_iterations_lists_final)
    plt.xticks([1,2,3,4], ["FCHC-lin", "FCHC-sqr", "DHC-lin", "DHC-sqr"])
    plt.ylabel("Number of Iterations")
    plt.savefig("nr_of_iterations.png")

    plt.show()
