messages = { # this is disgusting
    "notes": "Commands:\n`note <message>`: Add a note.\n`readnote <ID>`: Read a specified note number.\n`notes`: Read all of your notes.\n`deletenote <ID>`: Delete a specified note number.\n`clearnotes`: Delete all of your notes.",
    "reminders": "Commands:\n`addreminder <time in format #d, #h or #m> <message>`: Add a reminder to be read out to you in a set amount of time.",
    "time": "Commands:\n`time <timezone>`: Get the exact time in a specified timezone.\n`time timezones`: View the accepted timezone formats.",
    "vote": "Cast a :thumbsup: and :thumbsdown: vote on the last message sent in a channel."
}
commands = list((messages.keys()))
plaintext_commands = str()
for i in range(len(commands)):
    plaintext_commands += "`" + commands[i] + "` "


generic = "You can use `help <command>` to get information about individual fuctions.\n My current commands are " + plaintext_commands

def output_message(msg):
    try:
        return(messages[msg])
    except KeyError:
        return("No such command exists.")
