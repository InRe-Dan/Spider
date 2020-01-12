import textfile, c
import time, discord

def get_time(code): # not proud of this one, will hopefully improve using Regex and dictionaries
    mult = 0
    if "m" in code:
        mult = 60
        code = code.replace("m", "")
    elif "h" in code:
        mult = 3600
        code = code.replace("h", "")
    elif "d" in code:
        mult = 86400
        code = code.replace("d", "")
    try:
        int(code.replace("d", ""))
        int(code.replace("h", ""))
        int(code.replace("m", ""))
    except:
        return(0)
    added_time = int(code) * mult
    if added_time > 604800:
        return(1)
    if added_time < 60:
        return(0)
    return(added_time)

def say_error(errorcode): # Use a code provided by get_time to output a suitable message if the command failed
    if errorcode == 0:
        return("Correct format: `addreminder <#d/#h/#m> <reminder>")
    if errorcode == 1:
        return("That's too long. You can set reminders for up to 7 days.")

def check(): # return a list of reminder IDs that have to be read out
    f = open(c.reminderfile, "r")
    overdue = []
    for i in range(0, textfile.count_lines(c.reminderfile)):
        current_line = f.readline()
        if int(current_line.partition(" ")[0]) < round(time.time()):
            overdue.append(current_line)
    return(overdue)

def take_data(line):
    timecode = line.partition(" ")[0]
    content = line.partition(" ")[2]
    return(timecode, content)

def read(content):
    reminder_message = content.partition(" ")[2].partition(" ")[2]
    reminder_user = "<@!" + str(content.partition(" ")[2].partition(" ")[0]) + ">"
    return("Reminder for " + reminder_user + ": " + reminder_message)


        





