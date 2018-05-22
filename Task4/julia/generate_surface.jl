# NOTE Enter this REPL and it works

using JLD
using Plots
plotlyjs()

dic=load("param/surface_parameter.jld")

x = dic["F"]
y = dic["Cr"]
z1 = dic["Fit_Avg"]
z2 = dic["Fit_Best"]
z3 = dic["Fit_Worst"]

#TODO figsize
surface(x, y, z1)
