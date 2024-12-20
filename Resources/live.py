## IMPORTS
import discord
import datetime
import os
import json
from io import BytesIO
from imports import ChannelAssociations, Token, ConvertChannel, SaveMessageData
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_message(Message:discord.Message):
    if Message.guild.id == 1302499549931110413:
        files = []
        Channel = client.get_channel(ConvertChannel(Message.channel.id))
        print(f"\nMESSAGEINFO:\n{Message}\n\n\n")
        # Backup Message
        #WriteCSV(Message)
        # Handle User Join
        if Message.type == discord.MessageType.new_member:
            Message.content = f"[SYSTEM MESSAGE]{Message.author.name} Joined the server!"

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
                    
        # Handle Long Messages
        if len(Message.content) > 2000:
             Half1 = Message.content[:2000]
             Half2 = Message.content[2000:]
             await Channel.send(content=Half1,embeds=Message.embeds,stickers=Message.stickers,files=files)
             await Channel.send(content=Half2,embeds=Message.embeds,stickers=Message.stickers,files=files)
             await Channel.send(f"-# From: <@{Message.author.id}> at <t:{int(Message.created_at.timestamp())}>\n-# (Message split in 2)")
        else:
            
            await Channel.send(content=Message.content,embeds=Message.embeds,stickers=Message.stickers,files=files)
            await Channel.send(f"-# From: <@{Message.author.id}> at <t:{int(Message.created_at.timestamp())}>")
        
@client.event
async def on_ready():
    print(f"\nContingency Plan Online.\nConnected as {client.user.name}\nMode: Live\n")


def main():
    client.run(Token)
if __name__ == "__main__":
    main()