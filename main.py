### IMPORTS ###
import discord
import os
import json
from dotenv import dotenv_values

### VARIABLES ###
ApiKey : dict = dotenv_values(".env")
client = discord.Client(intents=discord.Intents.all())

### FUNCTIONS ###

## SAFELY GRAB ATTRIBUTE##
def GrabAtt(obj, attr, default=None):
    try:
        for part in attr.split("."):
            obj = getattr(obj, part, None)
            if obj is None:
                return default
        return obj
    except AttributeError:
        return default

## BACKUP MESSAGE TO JSON FILE ([GUILD.ID]/[CHANNEL.ID]/[MESSAGE.ID]) ##
async def BackupMessage2Json(Message:discord.Message):
    print(f"\n\nBaginning backup of message ({Message.id})") # Debug        
    MessageDataDict : dict = {} # Initialize the dictionary for this message
    
    
    # ACTIVITY #
    if Message.activity:
        MessageDataDict.update({"activity" : Message.activity})
    else: 
        MessageDataDict.update({"activity" : ""}) # Fill with nothing if none exists
        print("No activity!") # Debug
    
    
    # APPLICATION #
    if Message.application:
        if Message.application.icon:
            
            ApplicationIconDict : dict = {
                "url" : Message.application.icon.url,
                "key" : Message.application.icon.key
            }
        else:
            ApplicationIconDict : dict = {}
        
        if Message.application.cover:
            ApplicationCoverDict : dict = {
                "url" : Message.application.cover.url,
                "key" : Message.application.cover.key
            }
        else:
            ApplicationCoverDict : dict = {}
            
        MessageDataDict.update({"application":{
            "id" : Message.application.id,
            "description" : Message.application.description,
            "name" : Message.application.name,
            "icon" : ApplicationIconDict,
            "cover" : ApplicationCoverDict
        }})
    else: 
        MessageDataDict.update({"application" : ""}) # Fill with nothing if none exists
        print("No application!") # Debug
    
    
    # APPLICATION_ID #
    if Message.application_id:
        MessageDataDict.update({"application_id" : Message.application_id})
        print("Added application_id") # Debug
    else: 
        MessageDataDict.update({"application_id" : ""}) # Fill with nothing if none exists
        print("No application_id!") # Debug
    
    
    # ATTACHMENTS #
    if Message.attachments:
        MsgAttachmentsList : list = [] # Initialize the attachment list for this message
        for item in Message.attachments: # Iterate through attachments, appending attributes to the list
            MsgAttachmentsList.append({
               "url" : item.url,
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
                "waveform" : str(item.waveform),
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
    
    
    # AUTHOR #
    if hasattr(Message.author, "roles"): # Test for roles, if the user is not in the guild anymore, this will fail.
        AvatarDict : dict = {} # Initialize the avatar dict
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
        
        if Message.author.avatar: # Test for an avatar, if so, add it to a temp dict
             AvatarDict = {
                 "url" : Message.author.avatar.url,
                 "key" : Message.author.avatar.key
            }
        else:
            AvatarDict = {}
            
            
        MessageDataDict.update({"author" : { # FUCKING FINALLY add the member data to the main dict
            "nick" : Message.author.nick,
            "name" : Message.author.name,
            "id" : Message.author.id,
            "global_name" : Message.author.global_name,
            "bot" : Message.author.bot,
            "system" : Message.author.system,
            "avatar" : AvatarDict,
            "colour" : {
                "r" : Message.author.colour.r,
                "g" : Message.author.colour.g,
                "b" : Message.author.colour.b
            },
            "roles" : MsgAuthorRolesList
        }})
    elif hasattr(Message, "author"): # Tests if author even exists at all, it absolutely should, but discord is scary soo....
        if Message.author.display_avatar: # Test for an avatar, if so, add it to a temp dict
             AvatarDict = {
                 "url" : Message.author.display_avatar.url,
                 "key" : Message.author.display_avatar.key
            }
        else:
            AvatarDict = {}
                 
        MessageDataDict.update({"author" : {
            "name" : Message.author.name,
            "id" : Message.author.id,
            "global_name" : Message.author.global_name,
            "bot" :Message.author.bot,
            "system" : Message.author.system,
            "display_avatar" : AvatarDict
        }})
    else:
        MessageDataDict.update({"author" : ""}) # Fill with nothing if none exists
        print("No author????!??!?!?!?!?!!") # Debug
    
            
    # CHANNEL #        
    if Message.channel:
        MessageDataDict.update({"channel":{
            "name" : Message.channel.name,
            "id" : Message.channel.id,
            "category_id" : Message.channel.category_id,
            "topic" : Message.channel.topic,
            "slowmode_delay" : Message.channel.slowmode_delay,
            "nsfw" : Message.channel.nsfw,
            "jump_url" : Message.channel.jump_url,
            "type" : {
                "name" : Message.channel.type.name,
                "value" : Message.channel.type.value
            }
        }})
    else:
        MessageDataDict.update({"channel" : ""}) # Fill with nothing if none exists
        print("No channel????!??!?!?!?!?!!") # Debug
    
    
    # CONTENT #
    if Message.content:
        MessageDataDict.update({"content" : Message.content})
    else:
        MessageDataDict.update({"content" : ""}) # Fill with nothing if none exists
        print("No content") # Debug 
    
            
    # CLEAN_CONTENT #        
    if Message.clean_content:
        MessageDataDict.update({"clean_content" : Message.clean_content})
    else:
        MessageDataDict.update({"clean_content" : ""}) # Fill with nothing if none exists
        print("No clean_content") # Debug
    
        
    # CREATE_AT #
    if Message.created_at:
        MessageDataDict.update({"created_at" : str(Message.created_at.timestamp())})
    else:
        MessageDataDict.update({"created_at" : ""}) # Fill with nothing if none exists
        print("No created_at") # Debug
    
        
    # EDITED_AT #
    if Message.edited_at:
        MessageDataDict.update({"edited_at" : str(Message.edited_at.timestamp())})
    else:
        MessageDataDict.update({"edited_at" : ""}) # Fill with nothing if none exists
        print("No edited_at") # Debug
    
        
    # EMBEDS #
    if Message.embeds:
        EmbedList : list = []
        for item in Message.embeds:
           EmbedList.append({
               "title" : item.title,
               "type" : item.type,
               "description" : item.description,
               "url" : item.url
           })
           MessageDataDict.update({"embeds" : EmbedList})
    else:
        MessageDataDict.update({"embeds" : ""}) # Fill with nothing if none exists
        print("No embeds") # Debug
    
    
    # FLAGS #
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
    
        
    # ID #
    if Message.id:
        MessageDataDict.update({"id" : Message.id})
    else:
        MessageDataDict.update({"id" : ""}) # Fill with nothing if none exists
        print("WHAT THE FUCK NO ID?????????") # Debug
    
    
    # INTERACTION_METADATA #
    if Message.interaction_metadata:
        MessageDataDict.update({"interaction_metadata" : {
            "created_at" : Message.interaction_metadata.created_at.timestamp(),
            "user" : {
                "name" : Message.interaction_metadata.user.name,
                "id" : Message.interaction_metadata.user.id,
                "global_name" : Message.interaction_metadata.user.global_name,
                "bot" :Message.interaction_metadata.user.bot,
                "system" : Message.interaction_metadata.user.system,
                "display_avatar" : {
                    "url" : Message.interaction_metadata.user.display_avatar.url,
                    "key" : Message.interaction_metadata.user.display_avatar.key   
                }
            },
            "original_response_message_id" : Message.interaction_metadata.original_response_message_id,
            "type" : {
                "name" : Message.interaction_metadata.type.name,
                "value" : Message.interaction_metadata.type.value
            },
            "interacted_message_id" : Message.interaction_metadata.interacted_message_id
        }})
    else:
        MessageDataDict.update({"interaction_metadata" : ""}) # Fill with nothing if none exists
        print("No interaction_metadata") # Debug
    
    
    # JUMP_URL #
    if Message.jump_url:
        MessageDataDict.update({"jump_url" : Message.jump_url})
    else:
        MessageDataDict.update({"jump_url" : ""}) # Fill with nothing if none exists
        print("No jump_url") # Debug
    
        
    # MENTION_EVERYONE #
    if Message.mention_everyone:
        MessageDataDict.update({"mention_everyone" : Message.mention_everyone})
    else:
        MessageDataDict.update({"mention_everyone" : ""}) # Fill with nothing if none exists
        print("No mention_everyone") # Debug
    
    
    # MENTIONS #
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
    
    
    # PINNED #
    if Message.pinned:
        MessageDataDict.update({"pinned" : Message.pinned})
    else:
        MessageDataDict.update({"pinned" : ""}) # Fill with nothing if none exists
        print("No pinned") # Debug
    
        
    # POLLS #
    if Message.poll:
        PollAnswersList : list = []
        for item in Message.poll.answers:
            EmojiDict : dict = {}
            if item.emoji:
                EmojiDict.update({
                    "name" : item.emoji.name,
                    "id" : item.emoji.id,
                    "animated" : item.emoji.animated,
                    "url" : item.emoji.url
                })
            PollAnswersList.append({
                "id" : item.id,
                "text" : item.text,
                "emoji" : EmojiDict
            })
            
        MessageDataDict.update({"poll" : {
            "question" : Message.poll.question,
            "answers" : PollAnswersList,
            "expires_at" : Message.poll.expires_at.timestamp(),
            "created_at" : Message.poll.created_at.timestamp(),
            "total_votes" : Message.poll.total_votes
        }})
    else:
        MessageDataDict.update({"poll" : ""}) # Fill with nothing if none exists
        print("No poll") # Debug
    
        
    # REACTIONS #
    if Message.reactions:
        MessageReactionsList : list = []
        for item in Message.reactions:
            UsersReacted : list = []
            async for user in item.users():
                UsersReacted.append(user.id)
            MessageReactionsList.append({
                "emoji" : str(item.emoji),
                "count" : item.count,
                "users" : UsersReacted
                })
        MessageDataDict.update({"reactions" : MessageReactionsList})
    else:
        MessageDataDict.update({"reactions" : ""}) # Fill with nothing if none exists
        print("No reactions") # Debug
    
    
    # REFERENCE #
    if Message.reference:
        MessageDataDict.update({"reference" : {
            "message_id" : Message.reference.message_id,
            "channel_id" : Message.reference.channel_id,
            "guild_id" : Message.reference.guild_id,
            "jump_url" : Message.reference.jump_url
        }})
    else:
        MessageDataDict.update({"reference" : ""}) # Fill with nothing if none exists
        print("No reference") # Debug    
    
        
    # STICKERS #
    if Message.stickers:
        StickersList : list = []
        for item in Message.stickers:
            StickersList.append({
                "name" : item.name,
                "id" : item.id,
                "format" : {
                    "value" : item.format.value,
                    "file_extension" : item.format.file_extension,
                    "value" : item.format.value
                }
            })
        MessageDataDict.update({"stickers" : StickersList})
    else:
        MessageDataDict.update({"stickers" : ""}) # Fill with nothing if none exists
        print("No stickers") # Debug 
    
        
    # SYSTEM_CONTENT #
    if Message.system_content:
        MessageDataDict.update({"system_content" : Message.system_content})
    else:
        MessageDataDict.update({"system_content" : ""}) # Fill with nothing if none exists
        print("No system_content") # Debug     
    
        
    # THREADS #
    if Message.thread:
        MessageDataDict.update({"thread" : {
            "name" : Message.thread.name,
            "id" : Message.thread.id,
            "archived" : Message.thread.archived,
            "locked" : Message.thread.locked,
            "invitable" : Message.thread.invitable,
            "auto_archive_duration" : Message.thread.auto_archive_duration,
            "type" : {
                "name" : Message.thread.type.name,
                "value" : Message.thread.type.value
            },
            "owner" : {
                "name" : Message.author.name,
                "id" : Message.author.id,
                "global_name" : Message.author.global_name,
                "bot" : Message.author.bot,
                "system" : Message.author.system,
                "display_avatar" : {
                    "url" : Message.author.display_avatar.url,
                    "key" : Message.author.display_avatar.key                
                }
            },
            "jump_url" : Message.thread.jump_url
        }})
    else:
        MessageDataDict.update({"thread" : ""}) # Fill with nothing if none exists
        print("No thread") # Debug  
    
    
    # TTS #
    if Message.tts:
        MessageDataDict.update({"tts" : Message.tts})
    else:
        MessageDataDict.update({"tts" : ""})
        print("No tts") # Debug  
        
        
    # TYPE #
    if Message.type:
        MessageDataDict.update({"type" : {
            "name" : Message.type.name,
            "value" : Message.type.value
        }})
    else:
        MessageDataDict.update({"type" : ""})
        print("No type")
        
        
    # WEBHOOK_ID #
    if Message.webhook_id:
        MessageDataDict.update({"webhook_id" : Message.webhook_id})
    else:
        MessageDataDict.update({"webhook_id" : ""})
        print("No webhook_id")
        
        
    # WRITE TO FILE #
    MessageFilePath : str = f"Backups/{Message.guild.id}/{Message.channel.id}"
    
    if not os.path.exists(MessageFilePath):
        os.makedirs(MessageFilePath)    
    
    print("Saving to file ({Message.id})") # Debug      
    with open(f"{MessageFilePath}/{Message.id}.json", 'w') as fp:
        json.dump(MessageDataDict, fp, indent=4)
        
        print(f"Written to file ({Message.id})") # Debug


## BACKUP A FULL CHANNEL ##
async def BackupChannel(ChannelID:int, FullBackup:bool = False, NewestFirst:bool = False):
    TargetChannel = client.get_channel(ChannelID)

    async for Message in TargetChannel.history(limit=None,oldest_first= not NewestFirst):
        if not FullBackup:
            if os.path.exists(f"Backups/{Message.guild.id}/{Message.channel.id}/{Message.id}.json"):
                print(f"Message already exists ({Message.id})")
                continue
        await BackupMessage2Json(Message)
    print("All Done!")    
            
            
## BACKUP A FULL GUILD ##
async def BackupGuild(GuildID:int, FullBackup:bool = False, NewestFirst:bool = False):
    TargetGuild = client.get_guild(GuildID)
    for Channel in TargetGuild.text_channels:
        await BackupChannel(ChannelID=Channel.id, FullBackup=FullBackup, NewestFirst=NewestFirst)

### MAIN RUN ###

@client.event
async def on_ready():
    print(f"Connected as: {client.user.name}")
    await BackupGuild(GuildID=GuildIDInput, FullBackup=FullBackupInput, NewestFirst=NewestFirstInput)
    
    
def main():
    global GuildIDInput, FullBackupInput, NewestFirstInput
    GuildIDInput = int(input("What is the Guild ID? "))
    FullBackupInput  = input("Full Backup? (y/N)").lower() == "y"
    NewestFirstInput = input("Newest First? (y/N)").lower() == "y"
    client.run(ApiKey["TOKEN"])
if __name__ == "__main__":
    main()