for i in range(50):
    ## constraints determining population used each turn is not above amt of existing population
    # create empty string
    equation = ''
    # add left side of equation
    equation = equation + "m.addConstr(sp[" + str(i) + "] + fp["  + str(i) + "] + wp["+ str(i) + "] + gp[" + str(i) + "] <= 6"
    # add population made in each turn and subtract soldiers made per turn
    for j in range(i):
       equation = equation + " + p[" + str(j) + "] - sol1[" + str(j) + "] - sol2[" + str(j) + "]"

    # add population lost in battle constraints
    if (i > 19):
        for k in range((i-20)//5+1):
            equation = equation + " - pl[" + str(k) + "]"
    
    # add closing parentheses
    equation = equation + ")"

    #print equation
    print(equation)