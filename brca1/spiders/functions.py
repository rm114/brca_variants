def remove_parenthesis (i):
    start = i.find("(")
    end = i.find(")")
    if start != -1 and end != -1:
        i = i[start+1:end]
        return (i)
    elif start == -1 and end != -1:
        i = i[:end]
        return (i)
    elif start != -1 and end == -1:
        i = i[start+1:]
        return (i)
    else:
        return (i)
def remove_p(i):
    if "p." in i:
        i = i.replace("p.", "")
        return(i)
    else:
        return (i)
def remove_c(i):
    if "c." in i:
        i = i.replace("c.", "")
        return (i)
    else:
        return (i)

def remove_ast(i):
    if "*" in i:
        i = i.replace("*", "ter")
        return(i)
    else:
        return(i)
def remove_x(i):
    if "x" in i:
        i = i.replace("x", "*")
        return(i)
    else:
        return(i)
def remove_ivs(i):
    if "ivs" in i:
        i = i.replace("ivs", "")
        return(i)
    else:
        return(i)