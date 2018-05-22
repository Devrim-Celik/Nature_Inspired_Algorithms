include("task_types.jl")
include("diff_evoluation.jl")

#using JLD
using Plots
gr()

# ---------------------------------------------------------------------------- #
# SETUP
plant1 = Plant(50000.0, 10000.0, 100.0)
plant2 = Plant(600000.0, 80000.0, 50.0)
plant3 = Plant(4000000.0, 400000.0, 3.0)
plant_list = [plant1, plant2, plant3]

market1 = Market(0.45, 2000000.0)
market2 = Market(0.25, 30000000.0)
market3 = Market(0.2, 20000000.0)
market_list = [market1, market2, market3]

# ---------------------------------------------------------------------------- #
# OBJECTIVE/FITNESS FUNCTION
function profit_fitness(setup) # TODO CHECK IF IT IS RIGHT
    # assign components of setup
    e1, e2, e3, s1, s2, s3, p1, p2, p3 = setup
    e_list = [e1, e2, e3]
    s_list = [s1, s2, s3]
    p_list = [p1, p2, p3]

    purchasing_cost = maximum([sum(s_list) - sum(e_list), 0]) * 0.6

    production_cost = 0
    revenue = 0
    for i in 1:3
        production_cost += calculate_cost(e_list[i], plant_list[i])
        revenue += minimum([calculate_demand(p_list[i], market_list[i]), s_list[i]])
    end

    cost = production_cost + purchasing_cost

    profit = revenue - cost

    profit
end

# ---------------------------------------------------------------------------- #
# PARAMETERS
population_size     =   [50, 100, 200, 500, 1000]
minimum_values      =   [0, 0, 0, 0, 0, 0, 0, 0, 0]
maximum_values      =   [1000000000, 1000000000, 1000000000, 1000000000,
                            1000000000, 1000000000, 1, 1, 1]
# NOTE This parameter is the exploration/convergence parameter:
    # For bigger values, we cover a bigger space [higher exploration]
    # But if you want to reach a certain point (local optimum) you need smaller
    # vectors (smaller F since its scaling this vector) [faster convergence]
F                   =   LinSpace(0.4, 1.0, 13)      # usually in [0.4 ; 1]
Cr                  =   LinSpace(0.0, 0.5, 11)      # usually smaller values
nr_generations      =   10
modules             =   ["BINOMIAL", "EXPONENTIAL"]
# ---------------------------------------------------------------------------- #
single_case = true
surface_case = true

if single_case
    population, avg, best, worst = differential_evolution(population_size[2],
    minimum_values, maximum_values, F[1], Cr[3], profit_fitness,
    nr_generations, modules[2], true)
end

if surface_case
    # create array to save the value for different setups
    # 1.dimension: F dimension with length(F)
    # 2.dimension: Cr diension with lenth(Cr)
    # 3.dimension: size 3 --> for average, best & worst value for this run
    surface_data = zeros(length(F), length(Cr), 3)
    # NOTE: columns first ;)
    for indx_Cr in 1:length(Cr)
        for indx_F in 1:length(F)
            population, avg, best, worst = differential_evolution(
            population_size[2], minimum_values, maximum_values, F[indx_F],
            Cr[indx_Cr], profit_fitness, nr_generations, modules[2], false)

            # set corresponding data
            surface_data[indx_F, indx_Cr, :] = [avg[end], best[end], worst[end]]
        end
    end

    """
    # save parameters for 3D plot
    save("param/surface_parameter.jld", "F", F, "Cr", Cr, "Fit_Avg",
    surface_data[:, :, 1], "Fit_Best", surface_data[:, :, 2], "Fit_Worst",
    surface_data[:, :, 3], )
    """
    surface(F, Cr, surface_data[:, :, 1])
    savefig("here.png")
end
