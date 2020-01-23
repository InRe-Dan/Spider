import time
from datetime import datetime

timezones = { 
    "PST": -28800,
    "MST": -25200,
    "CST": -21600,
    "EST": -18000,
    "GMT": 0,
    "UTC": 0,
    "CET": 3600}

def determine_format(code):
    """Inputs the timezone code and return either 'UTC', an integer of difference between UTC and the specified timezone or `Invalid`"""
    if code.startswith("UTC") and len(code) > 4 and (("-" in code) ^ ("+" in code)):
        return("UTC")
    try:
        int(timezones[code])
        return("Other")
    except:
        return("Invalid")


def get_output(code):
    if code == "HELP":
        return("This command accepts any `UTC+X` or `UTC-X` timezone, as well as the following standard timezones: \n" + str(timezones.keys()).strip("dict_keys()[]"))

    format_type = determine_format(code)
    if format_type == "Invalid":
        return("Couldn't recognize timezone. Use `time help` to see which timezone formats are accepted.")
    elif format_type == "Other":
        specific_time = time.time() + timezones[code]
    elif format_type == "UTC":
        try:
            offset = int(code.partition("+")[2])
            specific_time = time.time() + (offset * 3600)
        except:
            try:
                offset = int(code.partition("-")[2])
                specific_time = time.time() + (offset * -3600)
            except:
                format_type = "Invalid"
                print("Invalid")

    print(format_type)
    if format_type == "Invaild":
        return("Couldn't recognize timezone. Use `time help` to see which timezone formats are accepted.")
    else:
        return(str(code) + " time right now is `" + str(datetime.fromtimestamp(specific_time)).partition(".")[0] + "`")
