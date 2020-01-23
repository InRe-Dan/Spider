import os
import time
import asyncio

import discord
from discord.utils import get

import textfile
import reminder
import note
import times
import commandhelp
import c

client = discord.Client()

# Functions

def clean_command(content):
    """Removes a one word prefix from a command and returns the cleaned message."""
    return(content.partition(" ")[2])

def get_roles(msg):
    """Return a more comprehensible list of an author's roles. Must pass a message object as parameter"""
    role_list = []
    if get(msg.guild.roles, id = c.role.admin) in msg.author.roles:
        role_list.append("admin")
    if get(msg.guild.roles, id = c.role.mod) in msg.author.roles:
        role_list.append("mod")
    if get(msg.guild.roles, id = c.role.botuser) in msg.author.roles:
        role_list.append("botuser")
    return(role_list)



# Background functions

async def check_for_reminders():
    """Iterate through the reminder file and send overdue ones every second. No parameters and no returned variables."""
    await client.wait_until_ready()
    while True:
        overdue = reminder.check()
        if overdue != []:
            for i in range(0, len(overdue)):
                await client.get_channel(c.channel.commands).send(reminder.read(overdue[i]))
                textfile.delete_line(c.reminderfile, overdue[i])
        await asyncio.sleep(10)

@client.event # On startup
async def on_ready(): # logging, checks and initialization
    print("Bot by InternetRecluse#6974")
    print("Logged in as {0.user}".format(client)) 
    await client.change_presence(activity = discord.Game(name = "Animal Crossing: New Leaf"))
    if not textfile.check(c.reminderfile):
        textfile.create(c.reminderfile)


@client.event # Reading messages sent
async def on_message(message): # First, log the message in the console, unless it's already in a logs channel
    if message.channel.id == c.channel.spamlog or message.channel.id == c.channel.log: # ignore logs
        return
    print(str(message.author.name) + "#" + str(message.author.discriminator) + " (" + str(message.author.id)  + "): " + str(message.content))
    user_roles = get_roles(message)
    
    # Help commands

    if message.content.startswith(c.prefix + "help "):
        await client.get_channel((message.channel).id).send(commandhelp.output_message(clean_command(message.content)))
    elif message.content.startswith(c.prefix + "help"):
        await client.get_channel((message.channel).id).send(commandhelp.generic)
    if message.content == ("<@!" + str(client.user.id) + ">"):
        await client.get_channel((message.channel).id).send(" My prefix is `" + c.prefix + "` and you can use `" + c.prefix + "help` to see a list of available commands.")
    
    # Moderator and administrator commands

    if message.content.startswith(c.prefix + "botannounce ") and "mod" in user_roles: # Announce message
        await client.get_channel(c.channel.announcement).send(str(clean_command(message.content)))
        return()

    if message.content.startswith(c.prefix + "shutdown") and "admin" in user_roles: # Remote bot shutdown
        await client.get_channel(message.channel.id).send("✌️")
        print("Now quitting...")
        exit()
        return
    
    if message.content.startswith(c.prefix + "vote"):
        history = await message.channel.history(limit = 2).flatten()
        to_react = history[1]
        await message.delete()
        await to_react.add_reaction("👍")
        await to_react.add_reaction("👎")
        
        # This doesn't work yet. Suggested methods are "history = await channel.history(limit=2)" or "async for message in ctx.channel.history(limit=3)"

    # Note system

    if message.content.startswith(c.prefix + "note ") and "botuser" in user_roles:
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
            textfile.create(filename)
        if textfile.count_lines(filename) > 50:
            await client.get_channel((message.channel).id).send("You've stored too many notes. Please delete some to add more.")
            return
        if len(clean_command(message.content)) > 200:
            await client.get_channel((message.channel).id).send("I'm not gonna remember that. Please try and shorten the note.")
        textfile.write(clean_command(message.content) + "\n", filename)
        await client.get_channel((message.channel).id).send("Saved as note number " + str(textfile.count_lines(filename)) + "!")
        return

    if message.content.startswith(c.prefix + "readnote ") and "botuser" in user_roles:
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
            await client.get_channel((message.channel).id).send("You don't have any notes stored.")
        else:
            await client.get_channel((message.channel).id).send(note.read(clean_command(message.content), filename))
        return 

    if message.content.startswith(c.prefix + "notes") and "botuser" in user_roles:
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
            await client.get_channel((message.channel).id).send("You don't have any notes stored.")
        else:
            if len(note.read_all(filename))> 1900:
                await client.get_channel((message.channel).id).send(content = "Your notes are too long to be sent. Here's a file: ", file = discord.File(filename, filename = "notes.txt"), delete_after = 20.0)
            else:
                await client.get_channel((message.channel).id).send(note.read_all(filename))
        return

    if message.content.startswith(c.prefix + "deletenote ") and "botuser" in user_roles:
        filename = str(message.author.id) + "notes.txt"
        try:
            note_id = int(clean_command(message.content))
        except:
            await client.get_channel((message.channel).id).send("Correct Syntax - `deletenote <note ID>`")
            return
        if note_id > textfile.count_lines(filename):
            await client.get_channel((message.channel).id).send("You don't have that many notes stored.")
            return
        textfile.delete_line(filename, str(note.read(note_id, filename)))
        return
        
    if message.content.startswith(c.prefix + "clearnotes") and "botuser" in user_roles:
        filename = str(message.author.id) + "notes.txt"
        if textfile.check(filename):
            os.remove(filename)
            await client.get_channel((message.channel).id).send("Notes deleted.")
        else:
            await client.get_channel((message.channel).id).send("You don't have any notes to delete.")
        return

    # Reminder system

    if message.content.startswith(c.prefix + "reminder ") and "botuser" in user_roles:
        if textfile.count_lines(c.reminderfile) > 50:
            await client.get_channel((message.channel).id).send("There are too many reminders at the moment. Please try again later.")
            return
        elif len(message.content) > 200:
            await client.get_channel((message.channel).id).send("I'm not gonna remember that. Please make your message shorter.")
            return
        timecode, messagecontent = reminder.take_data(clean_command(message.content))
        seconds = reminder.get_time(timecode)
        if seconds == 0 or seconds == 1: # This whole process here could do with some cleaning
            await client.get_channel((message.channel).id).send(reminder.say_error(seconds))
            return
        else:
            textfile.write(str(int(time.time()) + int(seconds)) + " " + str(message.author.id) + " " +  str(messagecontent) + "\n", c.reminderfile)
            await client.get_channel((message.channel).id).send("Reminder set.")
            return
    
    # Timezone and time command system

    if message.content.startswith(c.prefix + "time "):
        timezone = (clean_command(message.content)).upper()
        await client.get_channel((message.channel).id).send(times.get_output(timezone))

client.loop.create_task(check_for_reminders())
client.run(c.token)
