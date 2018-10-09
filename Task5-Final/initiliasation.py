import numpy as np
import pandas as pd

## EMMA --> THE FUNCTION YOU NEED TO LOOK AT: complete_init() !!!
# TIPS:
# Extract pure numpy array from dataframe: dataframe.values!

def load_data(task_nr=1):
    """
    Function to load all the data from the .txt file into numpy
    arrays and then into a pandas array

    task_nr : 1 or 2 for either task 1 or task 2
    """
    # create the path string, depending on chosen task nr (1 or 2)
    path = "VRP{}".format(task_nr)

    # load all data from txt files into numpy arrays
    capacity_np = np.loadtxt(path+"/capacity.txt")
    demand_np = np.loadtxt(path+"/demand.txt")
    distance_np = np.loadtxt(path+"/distance.txt")
    transportation_cost_np = np.loadtxt(path+"/transportation_cost.txt")

    return (capacity_np, demand_np, distance_np, transportation_cost_np)


def test_task(cap, demands):
    """
    Given the capacity and the demands, the function tests, whether
    a given setup can be fulfilled, or...
    """
    return sum(cap) >= sum(demands)


def init_matrix(capacitys, demands):
    """
    Given capacitys and demands, construct a initial dataframe. The Idea
    is:

    Truck 1 will drive to City 1 first, then City 2, then City 3 and so on,
    until it is empty. Then Truck 2 will pick up where Truck 1 left it and
    continue....
    """
    # "extract" number of cities and number of trucks
    nr_trucks = capacitys.shape[0]
    nr_citys = demands.shape[0]

    # names of the rows and cols of the dataframe
    truck_labels = ["truck_{}".format(i+1) for i in range(nr_trucks)]
    city_labels = ["city_{}".format(i+1) for i in range(nr_citys)]

    # create dataframe (filled with zeros for now)
    df = pd.DataFrame(np.zeros((nr_trucks, nr_citys)),
            index=truck_labels,
            columns=city_labels)


    # filling the dataframe
    # go through each truck...
    city_counter = 0
    for truck in range(nr_trucks):
        # get the capacity of the truck
        current_cargo = capacitys[truck]

        # while the truck still has cargo...
        while current_cargo:
            # then check if the truck can fullfil the demand
            # of the current city:

            if current_cargo >= demands[city_counter]:
                # if it can...

                # the truck delivers the city and fullfils its demands
                # [note that in the dataframe]
                df.values[truck, city_counter] = demands[city_counter]

                # of cause, it loses this amount of cargo
                current_cargo -= demands[city_counter]

                # and the demand is fulfilled
                demands[city_counter] = 0
                # ... and we move on to the next city
                city_counter += 1

            else:
                # if it doesnt have enough to completly fullfil the demands
                # it only delivers as much as it can...
                df.values[truck, city_counter] = current_cargo

                # and the demand is partly fulfilled
                demands[city_counter] -= current_cargo

                # and it doesnt have any cargo anymore
                current_cargo = 0

            # when we deliverd all cities, stop!
            if (city_counter == nr_citys):
                return df


def complete_init(task_nr=1):
    """
    Given a task_nr (1 or 2) the function will load all the data of the task,
    check if it is completable,
    will generate a dataframe for the representation of our solution,
    will fill this representation (description in the function),
    and return everything you need to continue with the task
    """

    # load capacity, demands, distance_matrix, transportation_costs
    cap, demands, dist, tc = load_data()

    # test if task is possible
    if test_task(cap, demands):
        print("[+] Task is possible!")
    else:
        raise("[-] ERRROR: BAD TASK!")

    # initialize matrix with given data
    dataframe = init_matrix(cap, demands)


    # return everything
    # (initialised dataframe, capacites, demands, distances, transportationcost)
    return dataframe, cap, demands, dist, tc



if (__name__=="__main__"):
    df, _, _, _, _ = complete_init(task_nr=1)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)
