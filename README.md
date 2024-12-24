# Discord Message Attributes

## Goal
The goal of this project is to be able to backup a discord server in its entirety, create an effective mirror of the server, and have a backup web source containing every attribute captured.

## Backing up
Backing up is finally done! Everything has been fully bug-tested, and it saves FAR more than it honestly should. You can choose between a full backup (overwritting previous .json files) or a quick backup (skipping any message that has previously been backed up). This allows you to choose between not needing to wait for 5 decades and having up-to-date backups in case of edits to messages.

Messages are backed up into a individual .json files, containing a grossly large amount of data, to the point of being redundant. The file path of messages are as follows:
```./{Guild.id}/{Channel.id}/{Message.id}.json```


You can run a full backup of a guild by first entering your token in ```.env```, then running ```backup.py```, and entering your [Guild ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID). Just be certain that the bot has all the read access it needs.

## Restoring
Restoring should include a bot sending all of the contents of the message, along with subtext indicating who it was from and when. (It possibly would have a link to the web source, however this is all massively TBD)

## Web Source
I see the web source as being one of two things, either a simple webserver hosting the json files directly, requiring the user to get to it using the replicated message, or possibly as a fully-fledged website that mimics the looks of a normal channel in discord, the insiration of this comes from [PLACEHOLDER's repo](#discord-message-attributes).