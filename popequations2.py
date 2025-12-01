for i in range((50-20)//5 + 1):
    ## constraints determining population lost at each battle
    # pl[i] <= M(1-e[i])
    print("m.addConstr(pl[" + str(i) + "] <= GRB.INFINITY * (1-e[" + str(i) + "]))")

    # pl[i] <= NUMENEMIES - NUMSOLDIERS + 10 + M(e)
    print("m.addConstr(pl[" + str(i) + "] <= ", end= '')
    print('NUMENEMIES',end='') #TODO:insert number of enemies statement here

    #subtract num soldiers existing
    # sol1 made 1 or more turn before
    for j in range(i * 5 + 19):
        print(" - sol1[" + str(j) + "]",end='')
    #sol2 made 5 or more turns before
    for j in range(i * 5 + 15):
        print(" - sol2[" + str(j) + "]",end='')
    print(" + GRB.INFINITY * e[" + str(i) + "])")

    # pl[i] >= NUMENEMIES - NUMSOLDIERS + 10 - M(e)
    print("m.addConstr(pl[" + str(i) + "] >= ", end= '')
    print('NUMENEMIES',end='') #TODO:insert number of enemies statement here

    #subtract num soldiers existing
    # sol1 made 1 or more turn before
    for j in range(i * 5 + 19):
        print(" - sol1[" + str(j) + "]",end='')
    #sol2 made 5 or more turns before
    for j in range(i * 5 + 15):
        print(" - sol2[" + str(j) + "]",end='')
    print(" - GRB.INFINITY * e[" + str(i) + "])")
