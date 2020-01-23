import textfile

def read(number, filename): # Reads a specified note number - should add whitespace removal
    if int(number) < 1 or int(number) > int(textfile.count_lines(filename)):
        return("This ID is out of range.")
    linesread = 0
    with open(filename, "r") as f:
        while True:
            linesread += 1
            line = f.readline()
            if linesread == int(number):
                return(line)

def read_all(filename): # output all notes - needs to be improved to send the whole txt if the note file is too long
    full = str()
    f = open(filename, "r")
    for i in range(0, int(textfile.count_lines(filename))):
        full = str(full) + str(f.readline())
    return("Here are your notes:\n" + full)

def clear(filename): # remove all of a user's notes
    with open(filename, "w") as f:
        pass

def delete(number, filename): # not sure how to make this feature yet
    pass