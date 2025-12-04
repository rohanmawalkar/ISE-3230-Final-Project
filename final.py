import gurobipy as gp
from gurobipy import GRB

m = gp.Model("age_of_empires_ii")
m.Params.LogToConsole = 1 
m.Params.TimeLimit = 90

n = 50
turns = range(n)       
states = range(n + 1)  

# Buildings built in each turn (s for stones, f for food, w for wood, g for gold)
s = m.addVars(turns, vtype=GRB.BINARY, name="sBuild")  # stone building
f = m.addVars(turns, vtype=GRB.BINARY, name="fBuild")  # food building
w = m.addVars(turns, vtype=GRB.BINARY, name="wBuild")  # wood building
g = m.addVars(turns, vtype=GRB.BINARY, name="gBuild")  # gold building

# Buildings available at start of each turn
sb = m.addVars(states, lb=0, vtype=GRB.INTEGER, name="sb")
fb = m.addVars(states, lb=0, vtype=GRB.INTEGER, name="fb")
wb = m.addVars(states, lb=0, vtype=GRB.INTEGER, name="wb")
gb = m.addVars(states, lb=0, vtype=GRB.INTEGER, name="gb")

# Resources at start of each turn
stone = m.addVars(states, lb=0.0, vtype=GRB.CONTINUOUS, name="stone")
food = m.addVars(states, lb=0.0, vtype=GRB.CONTINUOUS, name="food")
wood = m.addVars(states, lb=0.0, vtype=GRB.CONTINUOUS, name="wood")
gold = m.addVars(states, lb=0.0, vtype=GRB.CONTINUOUS, name="gold")

# The number of population
civ = m.addVars(states, lb=0.0, vtype=GRB.INTEGER, name="civ")

# The population created each turn
popNew = m.addVars(turns, lb=0, vtype=GRB.INTEGER, name="popNew")

# Soldiers trained
sol1_start = m.addVars(turns, lb=0, vtype=GRB.INTEGER, name="sol1_start") # type 1 soldiers(inferior one)
sol2_start = m.addVars(turns, lb=0, vtype=GRB.INTEGER, name="sol2_start") # type 2 soldiers(superior one)

# The current number of soldiers alive 
# (We keep the track of their number because some soldiers may have combat ability remaining)
sol1_alive = m.addVars(states, lb=0.0, vtype=GRB.INTEGER, name="sol1_alive")
sol2_alive = m.addVars(states, lb=0.0, vtype=GRB.INTEGER, name="sol2_alive")

# Workers assigned to each resource
spop = m.addVars(turns, lb=0.0, vtype=GRB.INTEGER, name="spop")
fpop = m.addVars(turns, lb=0.0, vtype=GRB.INTEGER, name="fpop")
wpop = m.addVars(turns, lb=0.0, vtype=GRB.INTEGER, name="wpop")
gpop = m.addVars(turns, lb=0.0, vtype=GRB.INTEGER, name="gpop")

# Define each invasion with its turn and enemy power
invasion_turns_1based = [t for t in range(25, n + 1, 5)]
enemy_power_map = {25: 5, 30: 10, 35: 15, 40: 30, 45: 55, 50: 90}

num_inv = len(invasion_turns_1based)
inv_idx = range(num_inv)

pl = m.addVars(inv_idx, lb=0, vtype=GRB.INTEGER, name="pl")

# Determine combat power at each invasion
combat = m.addVars(inv_idx, lb=0.0, vtype=GRB.CONTINUOUS, name="combat")
turn_to_inv = {}
for k, t1 in enumerate(invasion_turns_1based):
    t_end = t1 - 1 
    turn_to_inv[t_end] = k


# Starting buildings
m.addConstr(sb[0] == 0, "init_sb")
m.addConstr(fb[0] == 0, "init_fb")
m.addConstr(wb[0] == 0, "init_wb")
m.addConstr(gb[0] == 0, "init_gb")

# Starting resources
m.addConstr(stone[0] == 0,   "init_stone")
m.addConstr(food[0]  == 0,   "init_food")
m.addConstr(wood[0]  == 200, "init_wood")
m.addConstr(gold[0]  == 0,   "init_gold")

# Starting population + soldiers
m.addConstr(civ[0] == 6, "init_civ")
m.addConstr(sol1_alive[0] == 0, "init_sol1")
m.addConstr(sol2_alive[0] == 0, "init_sol2")

# Add the building planned to build this turn to the available buildings next turn
for t in turns:
    m.addConstr(sb[t + 1] == sb[t] + s[t], name=f"sb_update_{t}")
    m.addConstr(fb[t + 1] == fb[t] + f[t], name=f"fb_update_{t}")
    m.addConstr(wb[t + 1] == wb[t] + w[t], name=f"wb_update_{t}")
    m.addConstr(gb[t + 1] == gb[t] + g[t], name=f"gb_update_{t}")

# Add worker capacity constraints based on buildings
for t in turns:
    m.addConstr(spop[t] <= 10 * sb[t], name=f"cap_spop_{t}")
    m.addConstr(fpop[t] <= 5 * fb[t],  name=f"cap_fpop_{t}")
    m.addConstr(wpop[t] <= 10 * wb[t], name=f"cap_wpop_{t}")
    m.addConstr(gpop[t] <= 10 * gb[t], name=f"cap_gpop_{t}")

# Keep track of population number each turn
for t in turns:
    loss_expr = 0.0
    if t in turn_to_inv:
        k = turn_to_inv[t]
        loss_expr = pl[k]
    # This defines the number of civilians balance constraint =  new civilians - soldiers transferred - invasion losses
    m.addConstr(civ[t + 1] == civ[t] + popNew[t] - sol1_start[t] - sol2_start[t] - loss_expr, name=f"civ_balance_{t}")
    # This defines the civilian usage constraint
    m.addConstr(spop[t] + fpop[t] + wpop[t] + gpop[t] + sol1_start[t] + sol2_start[t] <= civ[t], name=f"civ_usage_{t}")


# Add the soliders planned to build this turn to the available soliders pool
# Type 1: 1-turn build
for t in turns:
    m.addConstr(
        sol1_alive[t + 1] == sol1_alive[t] + sol1_start[t],
        name=f"sol1_alive_update_{t}"
    )

# Type 2: 5-turn build
for t in turns:
    if t < 5:
        m.addConstr(
            sol2_alive[t + 1] == sol2_alive[t],
            name=f"sol2_alive_update_{t}"
        )
    else:
        m.addConstr(
            sol2_alive[t + 1] == sol2_alive[t] + sol2_start[t - 5],
            name=f"sol2_alive_update_{t}"
        )

# keep track of resource production and consumption each turn (how they are gathered and spent)
for t in turns:
    m.addConstr(stone[t + 1] == stone[t] - 100 * g[t] - 2.5 * gb[t] + 3.8 * spop[t], name=f"stone_balance_{t}")
    m.addConstr(food[t + 1] == food[t] - 30 * popNew[t] - 60 * sol1_start[t] - 240 * sol2_start[t] + 3.8 * fpop[t], name=f"food_balance_{t}")
    m.addConstr(wood[t + 1] == wood[t] - 100 * s[t] - 50 * f[t] - 100 * w[t]- 10 * sol1_start[t] + 3.4 * wpop[t],name=f"wood_balance_{t}")
    m.addConstr(gold[t + 1] == gold[t] - 120 * sol2_start[t] + 2.8 * gpop[t], name=f"gold_balance_{t}")

# Define when invasions happen and their effects
for k, t1 in enumerate(invasion_turns_1based):
    t_end = t1 - 1
    t_state = t_end + 1
    C_enemy = enemy_power_map[t1]

    ## Define combat power when invasion happens
    m.addConstr(
        combat[k] == sol1_alive[t_state] + 15 * sol2_alive[t_state],
        name=f"combat_{k}"
    )

    # Define population loss based on combat power
    m.addConstr(pl[k] >= 0, name=f"pl_nonneg_{k}")
    m.addConstr(pl[k] >= 10 + C_enemy - combat[k], name=f"pl_lb_{k}")
    m.addConstr(pl[k] <= 10 + C_enemy, name=f"pl_ub_{k}")

m.setObjective(gold[n], GRB.MAXIMIZE)

m.optimize()

print("obj_func = ", m.objVal)
for v in m.getVars():
    print('%s = %g' % (v.varName, v.x))
