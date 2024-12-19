###IMPORTS
import discord
import os
import datetime
import json
from dotenv import dotenv_values
from io import BytesIO
### VARIABLES
ApiKey = dotenv_values(".env")
client = discord.Client(intents=discord.Intents.all())
TestMessageID = 1313081608563064862
TestGuildID = 1302499549931110413
TestChannelID = 1304499100749660250

def GrabAtt(obj, attr, default=None):
    try:
        for part in attr.split("."):
            obj = getattr(obj, part, None)
            if obj is None:
                return default
        return obj
    except AttributeError:
        return default

async def BackupChannel(ChannelID:int):
    TargetChannel = client.get_channel(ChannelID)
    #print(f"Press Enter to backup: \"{TargetChannel.name}\"")
    #input()
    async for Message in TargetChannel.history(limit=None,oldest_first=True):
        MessageDataDict = {} # Initialize the dictionary for this message

        ## ACTIVITY ##
        if Message.activity:
            MessageDataDict.update({"activity" : Message.activity})
        else: 
            MessageDataDict.update({"activity" : ""})
            print("No activity!") # Debug
        
        ## APPLICATION ##
        if Message.application:
            MessageDataDict.update({"application":{
                "id" : Message.application.id,
                "description" : Message.application.description,
                "name" : Message.application.name,
                "icon" : {
                    "url" : Message.application.icon.url,
                    "key" : Message.application.icon.key
                },
                "cover" : {
                    "url" : Message.application.cover.url,
                    "key" : Message.application.cover.key
                }
            }})
        else: 
            MessageDataDict.update({"application":""})
            print("No application!") # Debug
        
        ## APPLICATION_ID ##
        if Message.application_id:
            MessageDataDict.update({"application_id" : Message.application_id})
            print("Added application_id") # Debug
        else: 
            
            print("No application_id!") # Debug
        
        ## ATTACHMENTS ##
        if Message.attachments:
            MsgAttachmentsList = [] # Initialize the attachment list for this message

            for item in Message.attachments: # Iterate through attachments, appending attributes to the list
                MsgAttachmentsList.append({
                    "id" : item.id,
                    "size" : item.size,
                    "height" : item.height,
                    "width" : item.width,
                    "filename" : item.filename,
                    "url" : item.url,
                    "proxy_url" : item.proxy_url,
                    "content_type" : item.content_type,
                    "description" : item.description,
                    "ephemeral" : item.ephemeral,
                    "duration" : item.duration,
                    "waveform" : item.waveform,
                    "flags" : {
                        "value" : item.flags.value,
                        "clip" : item.flags.clip,
                        "thumbnail" : item.flags.thumbnail,
                        "remix" : item.flags.remix
                    }
                })
            MessageDataDict.update({"attachments":MsgAttachmentsList})
            print("Added attachments") # Debug
        else: print("No attachments!") # Debug
        

        if hasattr(Message.author, "roles"): # Test for roles, if the user is not in the guild anymore, this will fail.
            print("Has roles, assuming user is member")
            MsgAuthorRolesList = [] # Initialize the list of roles
            for item in Message.author.roles: # Iterate through roles, adding them to the roles list
                 
                RolesAttributesDict = { # Role attributes that should always existy
                    "id" : item.id,
                    "name" : item.name,
                    "hoist" : item.hoist,
                    "managed" : item.managed,
                    "mentionable" : item.mentionable,
                    "colour" : {
                        "r" : item.colour.r,
                        "g" : item.colour.g,
                        "b" : item.colour.b
                }}
                
                if item.icon: # Test for an icon, if so, add it to the dict
                    RolesAttributesDict.update(
                    {   "icon" : {
                            "url" : item.icon.url,
                            "key" : item.icon.key
                    }})
                MsgAuthorRolesList.append(RolesAttributesDict)
                
            MessageDataDict.update({"Member" : { # FUCKING FINALLY add the member data to the main dict
                "nick" : Message.author.nick,
                "name" : Message.author.name,
                "id" : Message.author.id,
                "global_name" : Message.author.global_name,
                "bot" : Message.author.bot,
                "system" : Message.author.system,
                "avatar" : {
                    "url" : Message.author.avatar.url,
                    "key" : Message.author.avatar.key
                },
                "colour" : {
                    "r" : Message.author.colour.r,
                    "g" : Message.author.colour.g,
                    "b" : Message.author.colour.b
                },
                "roles" : MsgAuthorRolesList
            }})
        print(f"{MessageDataDict}\n\n")







@client.event
async def on_ready():

    print(f"Connected as: {client.user.name}")
    await BackupChannel(TestChannelID)




client.run(ApiKey["CPTOKEN"]) # Grabs CPTOKEN from .env file