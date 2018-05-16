
mutable struct Plant
    kWh::Float64
    cost::Float64
    maximum::Float64
end


mutable struct Market
    max_price::Float64
    max_demand::Float64
end

function calculate_cost(x::Float64, plant::Plant)
    """
    Calculates costs for a given amount of require energy and type of energy
        plant

    Args:
        x::Float64          required energy in [kW]
        plant::Plant        type of plant
    Returns:
        0       if required energy < 0
        -1      if required energy cant theoretically be produced by
                    type of plant
        else    cost to produce required energy
    """
    # if required energy < 0
    if x <= 0
        return 0
    # if required enery > maximum number of plant type * energy produced by each
    elseif x > plant.kWh * plant.maximum
        return 100
    # else we are "fine"
    else
        return ceil(x / plant.kWh) * plant.cost
    end
end

function calculate_demand(price::Float64, market::Market)
    """
    Calculates deman for a given price and a type of market

    Args:
        price::Float64          demand
        market::Market          type of market
    Returns:
        0                   if the price is bigger than the maximum price
                                of the market type
        market.max_demand   if price is free (ignore negative price)
        else                TODO
    """
    # price is too high for the maket
    if price > market.max_price
        return 0
    # price is for free
    elseif price <= 0
        return market.max_demand
    # TODO
    else
        return market.max_demand - price^2 * market.max_demand / market.max_price^2
    end
end
