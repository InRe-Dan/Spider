import discord, os, time, asyncio
import textfile, reminder, note, secret, c
client = discord.Client()

# Functions

def clean_command(content): # Remove the prefix from a command
    return(content.partition(" ")[2])

async def check_for_reminders():
    await client.wait_until_ready()
    while True:
        overdue = reminder.check()
        if overdue != []:
            print(overdue)
            for i in range(0, len(overdue)):
                await client.get_channel(c.channel.commands).send(reminder.read(overdue[i]))
                textfile.delete_line(c.reminderfile, overdue[i])
        await asyncio.sleep(10)

@client.event # On startup
async def on_ready(): # logging, checks and initialization
    print("Bot by InternetRecluse#6974")
    print("Logged in as {0.user}".format(client)) 
    await client.change_presence(activity = discord.Game(name = "with Sentience"))
    if not textfile.check(c.reminderfile):
        textfile.create(c.reminderfile)


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
        await client.get_channel(c.channel.personal).send(str(clean_command(message.content)))
        return()

    if message.content.startswith(c.prefix + "die") and message.author.id == c.user.dan: # Remote bot shutdown
        await client.get_channel(message.channel.id).send("✌️")
        print("Now quitting...")
        exit()
        return

    # Note system
    if message.content.startswith(c.prefix + "addnote ") and c.role.botuser in str(message.author.roles):
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
            textfile.create(filename)
        if textfile.count_lines(filename) > 20:
            await client.get_channel((message.channel).id).send("You've stored too many notes. Please delete some to add more.")
            return
        textfile.write(clean_command(message.content) + "\n", filename)
        await client.get_channel((message.channel).id).send("Saved as note number " + str(textfile.count_lines(filename)) + "!")
        return

    if message.content.startswith(c.prefix + "readnote ") and c.role.botuser in str(message.author.roles):
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
            await client.get_channel((message.channel).id).send("You don't have any notes stored.")
        else:
            await client.get_channel((message.channel).id).send(note.read(clean_command(message.content), filename))
        return 

    if message.content.startswith(c.prefix + "notes") and c.role.botuser in str(message.author.roles):
        filename = str(message.author.id) + "notes.txt"
        if not textfile.check(filename):
            await client.get_channel((message.channel).id).send("You don't have any notes stored.")
        else:
            await client.get_channel((message.channel).id).send(note.read_all(filename))
        return

    if message.content.startswith(c.prefix + "deletenote ") and c.role.botuser in str(message.author.roles):
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
        if textfile.count_lines(filename) == 0:
            os.remove(filename)
        await client.get_channel((message.channel).id).send("Note deleted.")
        
    if message.content.startswith(c.prefix + "clearnotes") and c.role.botuser in str(message.author.roles):
        filename = str(message.author.id) + "notes.txt"
        if textfile.check(filename):
            os.remove(filename)
            await client.get_channel((message.channel).id).send("Notes deleted.")
        else:
            await client.get_channel((message.channel).id).send("You don't have any notes to delete.")
        return

    # Reminder system

    if message.content.startswith(c.prefix + "addreminder ") and c.role.botuser in str(message.author.roles):
        
        if textfile.count_lines(c.reminderfile) > 50:
            await client.get_channel((message.channel).id).send("There are too many reminders at the moment. Please try again later.")
            return
        elif len(message.content) > 200:
            await client.get_channel((message.channel).id).send("I'm not gonna remember that. Please make your message shorter.")
            return
        timecode, messagecontent = reminder.take_data(clean_command(message.content))
        seconds = reminder.get_time(timecode)
        if seconds == 0 or seconds == 1:
            await client.get_channel((message.channel).id).send(reminder.say_error(seconds))
        else:
            textfile.write(str(int(time.time()) + int(seconds)) + " " + str(message.author.id) + " " +  str(messagecontent) + "\n", c.reminderfile)
            await client.get_channel((message.channel).id).send("Reminder set.")

        
        
client.loop.create_task(check_for_reminders())
client.run(secret.token)