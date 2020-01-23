prefix = # Type str(), default "//"
class channel(): # IDs, type int()
    spamlog = # This channel will be ignored and not processed by the bot
    log = # This channel will be ignored and not processed by the bot
    announcement = # Moderator messages using the "botannounce" command will be sent here
    commands = # Overdue reminders will be read out here
class user(): # IDs, type int()
    owner = # Currently unused
class role(): # IDs, type int()
    admin = # Administrator role. Current commands are "shutdown"
    mod = # Moderator role. Current commands are "botannounce"
    botuser = # Regular user role. Current commands are the note and reminder commands
reminderfile = "reminders.txt" # Default file name, can be renamed if required

# Discord user token is lower down to avoid accidentally revealing it














































































# Main account for the bot
token = # Primary bot ID here, type str()
# Account used for development and testing. Leave blank if you do not intend to develop the bot.
devtoken = "1 "# Secondary bot ID here, type str()