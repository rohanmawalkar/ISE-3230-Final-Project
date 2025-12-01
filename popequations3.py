for i in range(50):
    ## pop working on each type of building must be less than the num buildings times some constant (depends on type)
    ## STONE BUILDING
    # create empty string
    equation = ''
    # add left side of equation (by default if no buildings are built sp[i] = 0)
    equation = equation + "m.addConstr(sp[" + str(i) + "] <= 0"
    # add more for buildings built in previous turns
    for j in range(i):
        equation = equation + " + 10*s[" + str(j) + "]"

        
    # add closing parentheses
    equation = equation + ")"

    #print equation
    print(equation)

    ## FOOD BUILDING
    # create empty string
    equation = ''
    # add left side of equation (by default if no buildings are built fp[i] = 0)
    equation = equation + "m.addConstr(fp[" + str(i) + "] <= 0"
    # add more for buildings built in previous turns
    for j in range(i):
        equation = equation + " + 5*f[" + str(j) + "]"

        
    # add closing parentheses
    equation = equation + ")"

    #print equation
    print(equation)

    ## WOOD BUILDING
    # create empty string
    equation = ''
    # add left side of equation (by default if no buildings are built wp[i] = 0)
    equation = equation + "m.addConstr(wp[" + str(i) + "] <= 0"
    # add more for buildings built in previous turns
    for j in range(i):
        equation = equation + " + 10*w[" + str(j) + "]"

        
    # add closing parentheses
    equation = equation + ")"

    #print equation
    print(equation)

    ## GOLD BUILDING
    # create empty string
    equation = ''
    # add left side of equation (by default if no buildings are built gp[i] = 0)
    equation = equation + "m.addConstr(gp[" + str(i) + "] <= 0"
    # add more for buildings built in previous turns
    for j in range(i):
        equation = equation + " + 10*g[" + str(j) + "]"

        
    # add closing parentheses
    equation = equation + ")"

    #print equation
    print(equation)