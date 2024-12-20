## IMPORTS
import discord
from discord.ext import commands
from discord import Interaction
import csv
import os
import ast

## VARIABLES
# BOT INTENTS
intents = discord.Intents.all()
intents.message_content = True # Somehting about message contetnt
intents.members = True #
client = discord.Client(intents=intents)

## FUNCTIONS

# SETUP CSV FILE
def CreateCSV(ChannelID):
    if not os.path.isfile(f"{ChannelID}.csv"):
        with open(f"{ChannelID}.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter="Ɇ", quoting=csv.QUOTE_ALL, quotechar="×")
            writer.writerow(["Author", "Content", "Timestamp", "Message ID", "Attachments", "Embeds"])

# WRITE TO CSV FILE
def WriteCSV(ChannelID, author, content, timestamp, messageid, attachments, embeds):
    
    with open(f"{ChannelID}.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file ,delimiter="Ɇ", quoting=csv.QUOTE_ALL, quotechar="×")
        writer.writerow([author, content, timestamp, messageid, attachments, embeds])

# READ CSV FILE
def ReadCSV(ChannelID):
    ChannelMessages = []
    if not os.path.isfile(f"{ChannelID}.csv"):
        print("File does not exist (Error code 123510513638234807325140872358724358072345872380472380573240723047208376832476234580763450873048573540873542087234580)")
    else:
        with open(f"{ChannelID}.csv", mode='r', newline='', encoding='utf-8') as file:
            CSVDict = csv.DictReader(file, delimiter="Ɇ", quoting=csv.QUOTE_ALL, quotechar="×")
            for item in CSVDict:
                ChannelMessages.append(item)
                ChannelMessages.reverse()
            return ChannelMessages

# WRITE TO TXT FILE
def WriteTXT(Content):
    with open("Attachments.txt", "a") as file:
        file.write(Content)
    
    
# BACKUP A SERVER
async def BkupSrvr():
    i=0
    for guild in client.guilds:
        print(f"{i}) {guild}")
        i = i + 1
        
    GuildChoice = int(input("What server would you like to backup? "))
    print(f"\nYou chose: {client.guilds[GuildChoice]}")
    print(f"There are {len(client.guilds[GuildChoice].text_channels)} channels.\n")
    input("Press Enter to begin backing up all of them.")
    
    for Channel in client.guilds[GuildChoice].text_channels:
        print(f"Backing up: {Channel}")
        CreateCSV(Channel.id) # GENERATE THE CSV FILE FOR THIS CHANNEL
        print("Created CSV File")
        
        async for Message in Channel.history(limit=None):
            MessageContent = Message.content.replace("\n","[NEWLINEABC123]").replace("\r","[NEWLINEABC123]") # REPLACES ANY LINEBREAKS WITH A PLACEHOLDER SO CSV DONT BREAK
                
            if len(MessageContent) > 1500: # HANDLE MESSAGE APPROACHING LIMIT
                MessageContentPart1, MessageContentPart2 = MessageContent[:len(MessageContent)//2], MessageContent[len(MessageContent)//2:] # SPLIT MESSAGE CONTENT IN HALF
                MessageAttachments = []
                for attach in Message.attachments: # I CANT THINK ANYMORE THIS IS HELL FUCK ME PLEASE KILL ME
                    MessageAttachments.append(str(attach))
                    
                    
                WriteCSV(Channel.id, Message.author.id, MessageContentPart1, int(Message.created_at.timestamp()), Message.id, "", Message.embeds) # ADD FIRST HALF
                WriteCSV(Channel.id, Message.author.id, MessageContentPart2, int(Message.created_at.timestamp()), Message.id, MessageAttachments, Message.embeds) # ADD SECOND HALF
            else:
                MessageAttachments = []
                for attach in Message.attachments: # I CANT THINK ANYMORE THIS IS HELL FUCK ME PLEASE KILL ME
                    MessageAttachments.append(str(attach))
                    WriteTXT(f"{str(attach)}\n")
                    
                
                WriteCSV(Channel.id, Message.author.id, MessageContent, int(Message.created_at.timestamp()), Message.id, MessageAttachments, Message.embeds) # SAVE ANY IMPORTANT INFO
        print(f"{Channel} Backed up successfully!\n\n")
        
    input("Server backed up completely! Press enter to continue!")


# RESTORE BACKUPS
async def RstrBkup():
    
    i=0
    for guild in client.guilds:
        print(f"{i}) {guild}")
        i = i + 1
        
    GuildChoice = int(input("What server would you like to restore to? "))
    print(f"\nYou chose: {client.guilds[GuildChoice].name}\n")
    
    i=0
    for channel in client.guilds[GuildChoice].text_channels:
        print(f"{i}) {channel}")
        i = i + 1
        
    ChannelChoice = int(input("What channel would you like to restore to? "))
    SelectedChannel = client.guilds[GuildChoice].text_channels[ChannelChoice]
    print(f"\nYou chose: {SelectedChannel.name}\n")
    CSVRestoreFile = input("ID of backupped channel: ")
    ChannelMessages = ReadCSV(CSVRestoreFile)
    for iteration in ChannelMessages:
        MessageContent = f"{iteration["Content"]} \n-# From: <@{iteration["Author"]}> at <t:{iteration["Timestamp"]}>"
        MessageContent = MessageContent.replace("[NEWLINEABC123]","\n")
        await SelectedChannel.send(MessageContent)
        ListOAttachments= ast.literal_eval(iteration["Attachments"])
        for item in ListOAttachments:
            await SelectedChannel.send(item)
    
    
    input("Successful Restore! Press enter to continue!")


## BOT ACTIONS
@client.event
async def on_ready():
    
    print(f"\nContingency Plan Online.\nConnected as {client.user.name}\n")
    while True:
        print("""
B - Backup a server
R - Restore from a backup
Q - Quit          
              """)
        choice = input("Choice: ").lower()
        if choice == "q": exit()
        elif choice == "b": await BkupSrvr()
        elif choice == "r": await RstrBkup()

print("""
Unethical Bot        - A
The Contingency Plan - Enter
      """)
UserSelect = input("What bot do you want to use? ").lower()
if UserSelect == 'a': token = UnethicalBottoken
else: token = ContingencyPlantoken
client.run(token)