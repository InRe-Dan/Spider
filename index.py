import discord
import os
from datetime import datetime # not yet used
import c # Constant file, containing IDs and other
import note # Importing other functions
import textfile
import secret # token file
client = discord.Client()

# To-do
#    Reorganize functions and features into more classes and files
#    Add a reminder systems based on the current note system

# Functions

def clean_command(content, length): # Remove the prefix from a command
    without_command = content[length:]
    if False:
        pass # additional actions based on command name, i.e. extract different parameters or conditions and return them
    else:
        return(without_command)

# Events

@client.event # On startup
async def on_ready(): # logging, checks and initialization
    print("Bot by InternetRecluse#6974")
    print("I have logged in as {0.user}".format(client)) 
    await client.change_presence(activity = discord.Game(name = "with Sentience"))


@client.event # Reading messages sent
async def on_message(message): # First, log the message in the console, unless it's already in a logs channel
    if message.channel.id == c.channel.spamlog or message.channel.id == c.channel.log: # ignore logs
        return
    print(str(message.author.name) + "#" + str(message.author.discriminator) + " (" + str(message.author.id)  + "): " + str(message.content))

    # Actions on Spider's own messages

    if message.author == client.user and message.channel.id == c.channel.personal: # React to mod announcements
        await message.add_reaction("👍")
        await message.add_reaction("👎")
    # Commands - ideally organize in order of useage to optimize

    if message.content.startswith(c.prefix + "botannounce ") and message.author.id == c.user.dan: # Announce message
        await client.get_channel(c.channel.personal).send(str(clean_command(message.content, len(c.prefix + "botannounce "))))
        return

    if message.content.startswith(c.prefix + "die") and message.author.id == c.user.dan: # Remote bot shutdown
        await client.get_channel(message.channel.id).send("✌️")
        print("Now quitting...")
        exit()
        return

    # Note system - will change "message.author.id == c.user.dan" to a condition that evaluates if a user has "Note User" role
    if message.content.startswith(c.prefix + "addnote ") and int(message.author.id) in c.permittedusers.notes:
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
         textfile.create(filename)
        note.save(clean_command(message.content, len(c.prefix + "addnote ")), filename)
        await client.get_channel((message.channel).id).send("Saved as note number " + str(note.get_amount(filename)) + "!")
        return

    if message.content.startswith(c.prefix + "readnote ") and int(message.author.id) in c.permittedusers.notes:
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
            await client.get_channel((message.channel).id).send("You don't have any notes stored.")
        else:
            await client.get_channel((message.channel).id).send(note.read(clean_command(message.content, len(c.prefix + "readnote ")), filename))
        return 

    if message.content.startswith(c.prefix + "notes") and int(message.author.id) in c.permittedusers.notes:
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
            await client.get_channel((message.channel).id).send("You don't have any notes stored.")
        else:
            await client.get_channel((message.channel).id).send(note.read_all(filename))
        return

    if message.content.startswith(c.prefix + "deletenote ") and int(message.author.id) in c.permittedusers.notes:
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
         textfile.create(filename)
        if note.get_amount(filename):
            note.delete(clean_command(message.content, len(c.prefix + "deletenote ")), filename)
        return

    if message.content.startswith(c.prefix + "clearnotes") and int(message.author.id) in c.permittedusers.notes:
        filename = str(message.author.id) + "notes.txt"
        if textfile.check(filename):
            os.remove(filename)
            await client.get_channel((message.channel).id).send("Notes deleted.")
        else:
            await client.get_channel((message.channel).id).send("You don't have any notes to delete.")
        return

client.run(secret.token)