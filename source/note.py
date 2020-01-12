import textfile

def read(number, filename): # Reads a specified note number - should add whitespace removal
    if int(number) < 1 or int(number) > int(textfile.count_lines(filename)):
        return("This ID is out of range.")
    f = open(filename, "r")
    linesread = 0
    while True:
        linesread += 1
        line = f.readline()
        if linesread == int(number):
            f.close()
            return(line)

def read_all(filename): # output all notes - needs to be improved to send the whole txt if the note file is too long
    full = str()
    f = open(filename, "r")
    for i in range(0, int(textfile.count_lines(filename))):
        full = str(full) + str(f.readline())
    return("Here are your notes:\n" + full)

def clear(filename): # remove all of a user's notes
    f = open(filename, "w")
    f.close()

def delete(number, filename): # not sure how to make this feature yet
    pass