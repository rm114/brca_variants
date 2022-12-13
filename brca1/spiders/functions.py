import json

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
        
def output_match_table(i):
                
    jsonFile = open("match_table.json", "w")
    jsonFile.write(json.dumps(i, indent=4))
    jsonFile.close()
    print('JSON Match Table saved!')
    return(i)

def output_no_match_table(i):

    jsonFile = open("no_match_table.json", "w")
    jsonFile.write(json.dumps(i, indent=4))
    jsonFile.close()
    print('JSON No Match Table saved!')
    return(i)

def output_misc_table(i):

    jsonFile = open("misc_table.json", "w")
    jsonFile.write(json.dumps(i, indent=4))
    jsonFile.close()
    print('JSON Misc Table saved!')
    return(i)
