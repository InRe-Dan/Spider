def check(filename): # Return to see if a file exists
    try:
        f = open(filename, "r")
        result = True
        f.close
    except:
        result = False
    return(result)
def create(filename):
    f = open(filename, "x")
    f.close()