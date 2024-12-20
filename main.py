###IMPORTS
import discord
import os
import datetime
import json
from dotenv import dotenv_values
from io import BytesIO
### VARIABLES
ApiKey : dict = dotenv_values(".env")
client = discord.Client(intents=discord.Intents.all())
TestMessageID : int = 1313081608563064862
TestGuildID : int = 1302499549931110413
TestChannelID : int = 1304499100749660250

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
    async for Message in TargetChannel.history(limit=None,oldest_first=True):
        MessageDataDict : dict = {} # Initialize the dictionary for this message

        ## ACTIVITY ##
        if Message.activity:
            MessageDataDict.update({"activity" : Message.activity})
        else: 
            MessageDataDict.update({"activity" : ""}) # Fill with nothing if none exists
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
            MessageDataDict.update({"application" : ""}) # Fill with nothing if none exists
            print("No application!") # Debug
        
        ## APPLICATION_ID ##
        if Message.application_id:
            MessageDataDict.update({"application_id" : Message.application_id})
            print("Added application_id") # Debug
        else: 
            MessageDataDict.update({"application_id" : ""}) # Fill with nothing if none exists
            print("No application_id!") # Debug
        
        ## ATTACHMENTS ##
        if Message.attachments:
            MsgAttachmentsList : list = [] # Initialize the attachment list for this message

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
        else:
            MessageDataDict.update({"attachments" : ""}) # Fill with nothing if none exists
            print("No attachments!") # Debug
        
        ## ROLES ##
        if hasattr(Message.author, "roles"): # Test for roles, if the user is not in the guild anymore, this will fail.
            print("Has roles, assuming user is member")
            MsgAuthorRolesList = [] # Initialize the list of roles
            for item in Message.author.roles: # Iterate through roles, adding them to the roles list (roles come first because otherwise something happens i forgot :P)
                 
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
                
            MessageDataDict.update({"author" : { # FUCKING FINALLY add the member data to the main dict
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
        elif hasattr(Message, "author"): # Tests if author even exists at all, it absolutely should, but discord is scary soo....
            MessageDataDict.update({"author" : {
                "name" : {Message.author.name},
                "id" : {Message.author.id},
                "global_name" : {Message.author.global_name},
                "bot" : {Message.author.bot},
                "system" : {Message.author.system},
                "display_avatar" : {
                    "url" : {Message.author.display_avatar.url},
                    "key" : {Message.author.display_avatar.key}                
                }
            }})
        else:
            MessageDataDict.update({"author" : ""}) # Fill with nothing if none exists
            print("No author????!??!?!?!?!?!!") # Debug
                
        ## CHANNEL ##        
        if Message.channel:
            MessageDataDict.update({"channel":{
                "name" : Message.channel.name,
                "id" : Message.channel.id,
                "category_id" : Message.channel.category_id,
                "topic" : Message.channel.topic,
                "slowmode_delay" : Message.channel.slowmode_delay,
                "nsfw" : Message.channel.nsfw,
                "jump_url" : Message.channel.jump_url,
                "type" : Message.channel.type
            }})
        else:
            MessageDataDict.update({"channel" : ""}) # Fill with nothing if none exists
            print("No channel????!??!?!?!?!?!!") # Debug
        
        ## CONTENT ##
        if Message.content:
            MessageDataDict.update({"content" : Message.content})
        else:
            MessageDataDict.update({"content" : ""}) # Fill with nothing if none exists
            print("No content") # Debug 
                
        ## CLEAN_CONTENT ##        
        if Message.clean_content:
            MessageDataDict.update({"clean_content" : Message.clean_content})
        else:
            MessageDataDict.update({"clean_content" : ""}) # Fill with nothing if none exists
            print("No clean_content") # Debug
            
        ## CREATE_AT ##
        if Message.created_at:
            MessageDataDict.update({"created_at" : str(Message.created_at.timestamp())})
        else:
            MessageDataDict.update({"created_at" : ""}) # Fill with nothing if none exists
            print("No created_at") # Debug
            
        ## EDITED_AT ##
        if Message.edited_at:
            MessageDataDict.update({"edited_at" : str(Message.edited_at.timestamp())})
        else:
            MessageDataDict.update({"edited_at" : ""}) # Fill with nothing if none exists
            print("No edited_at") # Debug
            
        ## EMBEDS ##
        if Message.embeds:
            EmbedList : list = []
            for item in Message.embeds:
               EmbedList.append({
                   "title" : item.title,
                   "type" : item.type,
                   "description" : item.description,
                   "url" : item.url,
                   "colour" : {
                       "r" : item.colour.r,
                       "g" : item.colour.g,
                       "b" : item.colour.b
                   }
               })
               MessageDataDict.update({"embeds" : EmbedList})
        else:
            MessageDataDict.update({"embeds" : ""}) # Fill with nothing if none exists
            print("No embeds") # Debug
        
        ## FLAGS ##
        if Message.flags:
            MessageDataDict.update({"flags" : {
                "value" : Message.flags.value,
                "crossposted" : Message.flags.crossposted,
                "is_crossposted" : Message.flags.is_crossposted,
                "suppress_embeds" : Message.flags.suppress_embeds,
                "suppress_notifications" : Message.flags.suppress_notifications,
                "urgent" : Message.flags.urgent,
                "has_thread" : Message.flags.has_thread,
                "ephemeral" : Message.flags.ephemeral,
                "source_message_deleted" : Message.flags.source_message_deleted,
                "voice" : Message.flags.voice
            }})
        else:
            MessageDataDict.update({"flags" : ""}) # Fill with nothing if none exists
            print("No flags") # Debug
            
        ## ID ##
        if Message.id:
            MessageDataDict.update({"id" : Message.id})
        else:
            MessageDataDict.update({"id" : ""}) # Fill with nothing if none exists
            print("WHAT THE FUCK NO ID?????????") # Debug
        
        ## INTERACTION_METADATA ##
        if Message.interaction_metadata:
            MessageDataDict.update({"interaction_metadata" : Message.interaction_metadata.id})
        else:
            MessageDataDict.update({"interaction_metadata" : ""}) # Fill with nothing if none exists
            print("No interaction_metadata") # Debug
        
        ## JUMP_URL ##
        if Message.jump_url:
            MessageDataDict.update({"jump_url" : Message.jump_url})
        else:
            MessageDataDict.update({"jump_url" : ""}) # Fill with nothing if none exists
            print("No jump_url") # Debug
            
        ## MENTION_EVERYONE ##
        if Message.mention_everyone:
            Message.update({"mention_everyone" : Message.mention_everyone})
        else:
            MessageDataDict.update({"mention_everyone" : ""}) # Fill with nothing if none exists
            print("No mention_everyone") # Debug
        
        ## MENTIONS ##
        if Message.mentions:
            MentionList : list = []
            for item in Message.mentions:
                MentionList.append({
                    "name" : item.name,
                    "id" : item.id,
                    "global_name" : item.global_name,
                    "bot" : item.bot,
                    "system" : item.system,
                    "display_avatar" : {
                        "url" : item.display_avatar.url,
                        "key" : item.display_avatar.key
                    }
                })    
            MessageDataDict.update({"mentions" : MentionList})
        else:
            MessageDataDict.update({"mentions" : ""}) # Fill with nothing if none exists
            print("No mentions") # Debug
            
        print(f"{MessageDataDict}\n\n")
        
        MessageFilePath : str = f"Backups/{Message.guild.id}/{Message.channel.id}"
        if not os.path.exists(MessageFilePath):
            os.makedirs(MessageFilePath)    
        with open(f"{MessageFilePath}/{Message.id}.json", 'w') as fp:
            json.dump(MessageDataDict, fp, indent=4)






@client.event
async def on_ready():

    print(f"Connected as: {client.user.name}")
    await BackupChannel(TestChannelID)




client.run(ApiKey["CPTOKEN"]) # Grabs CPTOKEN from .env file