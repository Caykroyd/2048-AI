def avg_value(v,l):
    avg = 0
    for i in range(len(l)):
        if l[i] == v:
            avg += 1
    return avg/len(l)