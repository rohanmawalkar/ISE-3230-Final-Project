import cvxpy as cp

## define the enemy invasion constraints
T = 50
inv_turns_1based = [25, 30, 35, 40, 45, 50]
inv_turns = [t - 1 for t in inv_turns_1based]
enemy_power = [5, 15, 30, 65, 100, 160]
K = len(inv_turns)
M = 1000.0

## defeine the combat ability 
sol1 = cp.Variable(T, integer=True)
sol2 = cp.Variable(T, integer=True)
ourCombat = cp.Variable(K)
pl = cp.Variable(K, integer=True)
pl_turn = cp.Variable(T)

constraints = []

## define the enemy combat constraints
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
