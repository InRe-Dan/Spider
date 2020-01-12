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

def count_lines(filename):
    f = open(filename, "r")
    done = False
    counter = -1
    while not done:
        line = f.readline()
        counter += 1
        if line == str():
            done = True
    f.close()
    return(counter)

def write(content, filename):
    with open(filename, "a") as f:
        f.write(content)

def delete_line(filename, content):
    with open(filename, "r+") as f:
        filecontent = f.readlines()
        f.seek(0)
        for i in filecontent:
            if i != content:
                f.write(i)
        f.truncate()