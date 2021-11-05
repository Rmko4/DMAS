import pandas as pd
import copy
from trust.model import PDTModel

import numpy as np
import sys

N = 1000
n_min = 10
n_max = 100
n_stepsize = 10
mob_rate_min = 0
mob_rate_max = 1
mob_rate_stepsize = 0.1


if (len(sys.argv) == 1):
    print("Please specify name of Output file")
    sys.exit()

if (len(sys.argv) == 3 ):
    if sys.argv[2] =='MSAgent':
        print('MSAgent')
        model_args = {'AgentClass': 'MSAgent', 'mobility_rate': 0.2, 'number_of_agents': 1000, 'neighbourhood_size': 30}
    elif sys.argv[2] == 'WHAgent':
        print('WHAgent')
        model_args = {'AgentClass': 'WHAgent', 'mobility_rate': 0.2, 'number_of_agents': 1000, 'neighbourhood_size': 30}
    elif (sys.argv[2] == "RLAgent_NO_RELATIVE"):
        print("RLAgent")
        model_args = {'AgentClass': 'RLAgent', 'mobility_rate': 0.2, 'number_of_agents': 1000, 'neighbourhood_size': 30, 'learning_rate': 0.02, 'social_learning_rate': 0.1, 'discount_factor': 0.8, 'relative_reward': False}
    elif (sys.argv[2] == "RLAgent_NO_SOCIAL"):
        print("RLAgent")
        model_args = {'AgentClass': 'RLAgent', 'mobility_rate': 0.2, 'number_of_agents': 1000, 'neighbourhood_size': 30, 'learning_rate': 0.02, 'social_learning_rate': 0, 'discount_factor': 0.8, 'relative_reward': True}
    elif (sys.argv[2] == "RLAgent"):
        print("RLAgent")
        model_args = {'AgentClass': 'RLAgent', 'mobility_rate': 0.2, 'number_of_agents': 1000, 'neighbourhood_size': 30, 'learning_rate': 0.02, 'social_learning_rate': 0.5, 'discount_factor': 0.8, 'relative_reward': True}  
    elif (sys.argv[2] == "RLGossipAgent"):
        print("RLGossipAgent")
        model_args = {'AgentClass': 'RLGossipAgent', 'mobility_rate': 0.2, 'number_of_agents': 1000, 'neighbourhood_size': 30, 'learning_rate': 0.05, 'social_learning_rate': 0.5, 'discount_factor': 0.8, 'relative_reward': True, 'memory_size': 25}
    else:
        print("invalid agent type. choices are 'MSAgent', 'WHAgent', 'RLAgent' or 'GossipAgent'")
        sys.exit()
else:
    print('MSAgent')
    model_args = {'AgentClass': 'MSAgent', 'mobility_rate': 0.2, 'number_of_agents': 1000, 'neighbourhood_size': 30} 

run_args = {'T_onset': 100, 'T_record': 100}

print("Model params: " + str(model_args))
print("Run params: " + str(run_args))


with open(str(sys.argv[1]) + ".out", 'w') as f:
    with open(str(sys.argv[1]) + "TrustDensity.out", 'w') as g:
        f.write(str(n_min) +" " + str(n_max) +" " + str(n_stepsize) +" " + str(mob_rate_min) +" " + str(mob_rate_max) + " " +str(mob_rate_stepsize) + "\n")
        g.write(str(n_min) +" " + str(n_max) +" " + str(n_stepsize) +" " + str(mob_rate_min) +" " + str(mob_rate_max) + " " +str(mob_rate_stepsize) + "\n")

        print("Number of agents: " + str(N))
        for n in np.arange(n_min,n_max + 0.001,n_stepsize):
            for mob_rate in np.arange(mob_rate_min,mob_rate_max + 0.0001,mob_rate_stepsize):
                print("Neighborhood size: " + str(n) + ", Mobility rate: " + str(mob_rate))

                model_args["mobility_rate"] = mob_rate
                model_args["neighbourhood_size"] = n

                model = PDTModel(**model_args)

                model.run_model(**run_args)
                df_m = model.datacollector.get_model_vars_dataframe()
                df_a = model.datacollector.get_agent_props_dataframe()

                f.write(str(df_m["Market_Size"].mean()) + " ")
                f.write(str(df_m["Trust_in_Strangers"].mean()) + " ")
                f.write(str(df_m["Signal_Reading"].mean()) + " ")
                f.write(str(df_m["Trust_Rate"].mean()) + " ")
                f.write(str(df_m["Cooperating_Agents"].mean()) + " ")
                f.write(str(df_m["Trust_in_Neighbors"].mean()) + " ")
                f.write(str(df_m["Trust_in_Newcomers"].mean()) + "\n")
                for value in df_a["Trust_in_Stranger_proportion"]:
                    g.write(str(value) + " ")
                g.write("\n")