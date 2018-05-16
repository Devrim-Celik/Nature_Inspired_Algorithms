#Pkg.add("StatsBase") TODO takes forever, have to include?
#Pkg.add("Plots")

# TODO its right, that if x = ones(3,4)
# x[1] != x[1,:]

# TODO using modules dauer alles EWIG, was geht?
using StatsBase
using Plots

# TODO welche ist "beste"?
pyplot()

println("[+] MODULES LOADED")

# ---------------------------------------------------------------------------- #
function de_initializer(pop_size::Int64, minimum_values, maximum_values)
    """
    Initial target population

    Args
        pop_size::Int64     size of population
        minimum_values      array with minimal values for component range
        maximum_values      array with maximal values for component range

    Returns
        target              target population
    """

    target = zeros(pop_size, length(minimum_values))

    # TODO columns first like this?
    # go through all possible genomes
    for component in 1:length(minimum_values)
        # go through all members
        for member in 1:pop_size
            # generate a ellele by taking the minimum value for this particular
            # feature and randomly adding the scaled [by a float ϵ [0;1]]
            # difference to the maxim value for this feature
            target[member, component]  = minimum_values[component] + rand()*(maximum_values[component] - minimum_values[component])
        end
    end
    target
end

# ---------------------------------------------------------------------------- #
# TODO how to specify type of "target"???
function de_mutation(target, F::Float64, minimum_values, maximum_values)
    """
    Creates donor population (mutation population) from target population

    Args
        target      target population
        F::Float64  mutation parameter (whats its influence)

    Returns
        donor       donor population
    """

    donor = zeros(size(target))

    # for each member...
    for member in 1:size(target)[1]
        # get 3 random unique integers, which arent equal to member
        indx = sample(1:size(target)[1], 3, replace = false)
        # TODO BUG ugly done
        # exclude cases where member is part of indices
        while member in indx
            indx = sample(1:size(target)[1], 3, replace = false)
        end

        # generate new member, by using the 3 randomly chosen members;
        # subtracting the third member from the second one, scaling
        # this distance by F, and then adding it to the first member
        # TODO BUG since this can create values, higher/lower than defined, we should
        # take the min/max of this and the max/min allowed value
        # DONE BUT UGLY TODO
        temp = target[indx[1],:] + F*(target[indx[2],:]-target[indx[3],:])
        # remove to high values
        temp = min.(temp, maximum_values)
        # remove to low values
        temp = max.(temp, minimum_values)

        donor[member,:] = temp
    end
    donor
end

# ---------------------------------------------------------------------------- #
function de_crossover(target, donor, Cr::Float64, mode)
    """
    Create trial population, which is a crossover between the target and the
    donor population

    Args
        target          target population
        donor           donor population
        Cr              crossover rate
        mode            mode, either "EXPONENTIAL" or "BINOMIAL"

    Returns
        trial           trial population
    """

    trial = zeros(size(target))

    if mode == "EXPONENTIAL"
        # starting point for crossover
        n = rand(1:size(target)[2])
        # number of components the donor vector actually contributes to the
        # trial vector
        L = rand(1:size(target)[2])

        #TODO NOT FINISHED

    elseif mode == "BINOMIAL"
        # choose one component, which will be taken from the donor population
        # for sure, to get some "mutation". Do this for each member of the
        # target population
        j_rand = rand(1:size(target)[2], size(target)[1])

        # TODO COL BEFORE ROWS?
        for component in 1:size(target)[2]
            for member in 1:size(target)[1]
                # if we hit the crossover probability or we arrived
                # at our selected component for this member, use
                # donor population values, otherwise dont
                if rand() < Cr || component == j_rand[member]
                    trial[member, component] = donor[member, component]
                # otherwise use the target component
                else
                    trial[member, component] = target[member, component]
                end
            end
        end
    end
    trial
end

# ---------------------------------------------------------------------------- #

function de_selection(target, trial, fitness_function::Function)
    """
    Select either the target or trial population, by checking their fitness

    Args
        target                      target population
        trial                       trial population
        fitness_function::Function  function, measuring the fitness of
                                        one (or more!) members
    Returns
        new_target                  new target population after selection
    """

    # new target population
    new_target = zeros(size(target))

    for member in 1:size(target)[1]
        # if the fitness value of the target member is lower/equal the
        # fitness value of the trial member, it gets replaced in the new
        # target population (NOTE: also when equal, so you can move out of
        # flat function landscapes)
        if fitness_function(target[member,:]) <= fitness_function(trial[member,:])
            new_target[member,:] = trial[member,:] # TODO I hope no reference copies...
        else
            new_target[member,:] = target[member,:]
        end
    end
    new_target
end

# ---------------------------------------------------------------------------- #
#
function differential_evolution(pop_size::Int64, minimum_values, maximum_values,
    F::Float64, Cr::Float64, fitness_function::Function, nr_iterations::Int64, crossover_mode,
    save_plots::Bool)
    """
    Differential Evolution Algorithm

    Args
        pop_size::Int64                 population size
        minimum_values                  minimum value for components
        maximum_values                  maximum value for components
        F::Float64
        Cr::Float64                     crossover rate
        fitness_function::Function      fitness_function
                NOTE: fitness function needs to take one member of the
                    population in, and return a score (higher = better)
        nr_iterations::Int64            number of iterations
        crossover_mode                  which crossover mode
                NOTE: either "EXPONENTIAL" / "BINOMIAL"
        save_plots::Bool                create, save and display plots?

    Returns
        target                          final target population
        average_history                 history of population average
        best_history                    history of best members
        worst_history                   history of worst members
    """

    # TODO check if minimum_values and maximum_values are iterable

    if !(length(minimum_values) == length(maximum_values))
        println("[-]ERROR") # TODO EXCEPTION
    end

    # for saving the average/best/worst score of the target population
    average_history = []
    best_history = []
    worst_history = []


    # generate initial taret population
    target = de_initializer(pop_size, minimum_values, maximum_values)

    for iter in 1:nr_iterations
        println("Iteration Nr $iter")

        # ------------------------------------------------------ #
        # generate donor population
        donor = de_mutation(target, F, minimum_values, maximum_values)
        # crossover to generate trial population
        trial = de_crossover(target, donor, Cr, crossover_mode)
        # use selection, to find new best members
        target = de_selection(target, trial, fitness_function)
        # ------------------------------------------------------ #

        # TODO: instead generate fitness function of all members at once,
        # than use inbuild "sum(), max(), min()"

        # set average to 0
        average = 0.0
        # set best to minus infinity
        best = -Inf
        # set worst to plus infinity
        worst = Inf

        # go through all members
        for member in 1:pop_size
            # add fitness scores on average variable
            average += fitness_function(target[member,:])

            # if fitness score of current member is better than the
            # current best ...
            if fitness_function(target[member,:]) > best
                # ...set it to the new best
                best = fitness_function(target[member,:])
            end

            # if fitness score of current member is worse than the current
            # worst ....
            if fitness_function(target[member,:]) < worst
                # set it to the new worst
                worst = fitness_function(target[member,:])
            end
        end
        # divide average
        average /= pop_size
        push!(average_history, average)
        push!(best_history, best)
        push!(worst_history, worst)
    end


    # if enabled, save plots in a default plots folder
    if save_plots
        # plot 3 lines (avg, best, worst)
        plot(average_history, title="Differential Evolution. $pop_size-$F-$Cr-$nr_iterations-$crossover_mode",
            label="Average of Population", lw=3)
        plot!(best_history, label="Best Individual of Population", lw=3)
        plot!(worst_history, label="Worst Individual of Population", lw=3)
        # set axis limit
        plot!(ylims = (0, maximum(best_history)), figsize=(10,5))
        # set axis label
        xlabel!("Generation")
        ylabel!("Fitness")
        # save figures
        savefig("plots/differential_evolution_final_$(pop_size)_$(F)_$(Cr)_$(nr_iterations)_$(crossover_mode).png")
        # show plot
        show()
    end


    target, average_history, best_history, worst_history
end
