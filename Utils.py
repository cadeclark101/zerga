def roundCoords(x, base):
    x = list(x)
    y = [base * round(x[0]/base), base * round(x[1]/base)]
    return tuple(y)