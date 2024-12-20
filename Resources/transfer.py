## IMPORTS
import discord
import csv
import os
import json
from io import BytesIO
from imports import ChannelAssociations, Token, ConvertChannel, WriteCSV
client = discord.Client(intents=discord.Intents.all())
SourceGuildID = 773421979348500480
DestinationGuildID = 1313011783316934666


@client.event
async def on_ready():
    SourceGuild = client.get_guild(SourceGuildID)
    DestinationGuild = client.get_guild(DestinationGuildID)
    print(f"\nContingency Plan Online. Mode: Transfer\nConnected as {client.user.name}\n")
    print(f"Source: {SourceGuild.name}")
    print(f"Destination: {DestinationGuild.name}")
    print()
    input("start?")
    for SourceChannel in SourceGuild.text_channels:
        print("Backing up a channel:")
        print(f"Channel: {SourceChannel.name}")
        
        async for Message in SourceChannel.history(limit=None,oldest_first=True):
            if not Message.content:
                files = []
                DestinationChannel = client.get_channel(ConvertChannel(SourceChannel.id))
                print(f"\n{Message}\n")
                WriteCSV(Message)

                 # Handle User Join
                if Message.type == discord.MessageType.new_member:
                    Message.content = f"[SYSTEM MESSAGE] {Message.author.name} Joined the server!"
                
                if Message.type == discord.MessageType.pins_add:
                    Message.content = f"[SYSTEM MESSAGE] {Message.author.name} Pinned a message."

                if Message.stickers:
                    Message.stickers = discord.utils.get(client.stickers, id=1318609705014268014)



                # Handle Attachments
                if Message.attachments:
                    for attachment in Message.attachments:
                        print(f"Downloading: {attachment.filename}")
                        file_bytes = await attachment.read()
                        discord_file = discord.File(fp=BytesIO(file_bytes), filename=attachment.filename)
                        files.append(discord_file)

                # Handle Tenor GIFs
                if Message.embeds:
                    for embed in Message.embeds:
                        if embed.url[:23] == "https://tenor.com/view/":
                            Message.embeds.remove(embed)

                # Send Messages
                try:
                    if len(Message.content) > 2000:
                        Half1 = Message.content[:2000]
                        Half2 = Message.content[2000:]
                        await DestinationChannel.send(content=Half1,embeds=Message.embeds,stickers=Message.stickers,files=files)
                        await DestinationChannel.send(content=Half2,embeds=Message.embeds,stickers=Message.stickers,files=files)
                        await DestinationChannel.send(f"-# From: <@{Message.author.id}> at <t:{int(Message.created_at.timestamp())}> [Details](https://discord.jackthiess.com/Saved) [Message split in 2]\n")
                    else:
                        await DestinationChannel.send(content=Message.content,embeds=Message.embeds,stickers=Message.stickers,files=files)
                        await DestinationChannel.send(f"-# From: <@{Message.author.id}> at <t:{int(Message.created_at.timestamp())}>\n")
                        
                except Exception as e:
                    print(f"FAILURE\n {Message}\n {e}\n\n\n")
                    await client.get_channel(1318600974079758417).send(f"@jiggly.bits An errror has occurred.\n Message ID:{Message.id}\n Error:{e}")







def main():
    client.run(Token)
if __name__ == "__main__":
    main()
