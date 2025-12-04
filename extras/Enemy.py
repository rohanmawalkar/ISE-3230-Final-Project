import cvxpy as cp
import numpy as np

## define the enemy invasion constraints
T = 50
inv_turns_1based = [25, 30, 35, 40, 45, 50]
inv_turns = [t - 1 for t in inv_turns_1based]
enemy_power = [5, 15, 30, 65, 100, 160]
K = len(inv_turns)
M = 1000.0

## defeine the resource variables
s = cp.Variable(T, boolean=True)
f = cp.Variable(T, boolean=True)
w = cp.Variable(T, boolean=True)
g = cp.Variable(T, boolean=True)

## define the population and combat variables
p = cp.Variable(T, integer=True)
sol1 = cp.Variable(T, integer=True)
sol2 = cp.Variable(T, integer=True)

sp = cp.Variable(T, integer=True)
fp = cp.Variable(T, integer=True)
wp = cp.Variable(T, integer=True)
gp = cp.Variable(T, integer=True)

civ_pop = cp.Variable(T + 1)
B_s = cp.Variable(T + 1)
B_f = cp.Variable(T + 1)
B_w = cp.Variable(T + 1)
B_g = cp.Variable(T + 1)

wood = cp.Variable(T + 1)
stone = cp.Variable(T + 1)
food = cp.Variable(T + 1)
gold = cp.Variable(T + 1)

E = cp.Variable(K, boolean=True)
pl = cp.Variable(K, integer=True)
ourCombat = cp.Variable(K)
pl_turn = cp.Variable(T)

## define the constraints
constraints = []

constraints += [
    civ_pop[0] == 10,
    wood[0] == 200,
    stone[0] == 0,
    food[0] == 0,
    gold[0] == 0,
    B_s[0] == 0,
    B_f[0] == 0,
    B_w[0] == 0,
    B_g[0] == 0,
]

constraints += [
    p >= 0, sol1 >= 0, sol2 >= 0,
    sp >= 0, fp >= 0, wp >= 0, gp >= 0,
    civ_pop >= 0, wood >= 0, stone >= 0,
    food >= 0, gold >= 0,
    B_s >= 0, B_f >= 0, B_w >= 0, B_g >= 0,
    pl_turn >= 0, pl >= 0
]

## define the logic of the how different variables interact
for t in range(T):
    constraints += [
        B_s[t + 1] == B_s[t] + s[t],
        B_f[t + 1] == B_f[t] + f[t],
        B_w[t + 1] == B_w[t] + w[t],
        B_g[t + 1] == B_g[t] + g[t],

        sp[t] <= 10 * B_s[t],
        fp[t] <= 5 * B_f[t],
        wp[t] <= 10 * B_w[t],
        gp[t] <= 10 * B_g[t],

        sp[t] + fp[t] + wp[t] + gp[t] <= civ_pop[t],

        wood[t + 1] == wood[t] + 3.4 * wp[t]
                       - 100 * s[t] - 50 * f[t] - 100 * w[t]
                       - 10 * sol1[t],

        stone[t + 1] == stone[t] + 1.8 * sp[t]
                        - 100 * g[t] - 2.5 * B_g[t],

        food[t + 1] == food[t] + 3.8 * fp[t]
                       - 30 * p[t]
                       - 60 * sol1[t]
                       - 240 * sol2[t],

        gold[t + 1] == gold[t] + 1.8 * gp[t]
                       - 120 * sol2[t],

        civ_pop[t + 1] == civ_pop[t] + p[t] - sol1[t] - sol2[t] - pl_turn[t],

        sol1[t] + sol2[t] <= civ_pop[t],
    ]

## link the per-turn plunder to the invasion turns
for t in range(T):
    if t in inv_turns:
        k = inv_turns.index(t)
        constraints += [pl_turn[t] == pl[k]]
    else:
        constraints += [pl_turn[t] == 0]

for k in range(K):
    t_inv = inv_turns[k]
    enemy = enemy_power[k]
    if t_inv >= 5:
        heavy_active = cp.sum(sol2[:t_inv - 4])
    else:
        heavy_active = 0
    constraints += [
        ourCombat[k] == cp.sum(sol1[:t_inv + 1]) + 15 * heavy_active,
        ourCombat[k] >= 0,
        ourCombat[k] - enemy >= -M * (1 - E[k]),
        ourCombat[k] - enemy <= -1 + M * E[k],
        pl[k] >= 10 + enemy - ourCombat[k] - M * E[k],
        pl[k] <= 10 + enemy - ourCombat[k] + M * E[k],
        pl[k] <= M * (1 - E[k]),
    ]

objective = cp.Maximize(gold[T])
problem = cp.Problem(objective, constraints)

problem.solve(
    solver=cp.GUROBI,
    verbose=True,
    MIPGap=0.05,
    TimeLimit=60
)



