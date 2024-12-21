# Discord Message Attributes

## Goal
The goal of this project is to be able to backup a discord server in its entirety, create an effective mirror of the server, and have a backup web source containing every attribute captured.

## Backing up
The current progress of the backup is identified by the checkmarks in the [Attributes section](#attributes). Backups should be stored in JSON format, and they ideally will contain more information than they need too, as to not miss anything.

## Restoring
Restoring is on hold until [Backing up](#backing-up) is finalized. Restoring should include a bot sending all of the contents of the message, along with subtext indicating who it was from and when. (It possibly would have a link to the web source, however this is all massively TBD)

## Web Source
I see the web source as being one of two things, either a simple webserver hosting the json files directly, requiring the user to get to it using the replicated message, or possibly as a fully-fledged website that mimics the looks of a normal channel in discord, the insiration of this comes from [PLACEHOLDER's repo](#discord-message-attributes).

## Attributes
Below is the list of attributes tracked for the project, organized in a nested structure. Attributes that are finished being tracked are checked off.

### Activity✅
- **activity** (dict)✅

### Application✅
- **application** (discord.MessageApplication)✅
  - **id** (int)✅
  - **description** (str)✅
  - **name** (str)✅
  - **icon** (Asset)✅
    - **url** (str)✅
    - **key** (str)✅
  - **cover** (Asset)✅
    - **url** (str)✅
    - **key** (str)✅

### Application ID✅
- **application_id** (int)✅

### Attachments✅
- **attachments** (list[Attachment])✅
  - **id** (int)✅
  - **size** (int)✅
  - **height** (int)✅
  - **width** (int)✅
  - **filename** (str)✅
  - **url** (str)✅
  - **proxy_url** (str)✅
  - **content_type** (str)✅
  - **description** (str)✅
  - **ephemeral** (bool)✅
  - **duration** (float)✅
  - **waveform** (bytes)✅
  - **flags** (AttachmentFlags)✅
    - **value** (int)✅
    - **clip** (bool)✅
    - **thumbnail** (bool)✅
    - **remix** (bool)✅

### Author✅
- **author**✅
  - **Member**✅
    - **nick** (str)✅
    - **name** (str)✅
    - **id** (int)✅
    - **global_name** (str)✅
    - **bot** (bool)✅
    - **system** (bool)✅
    - **avatar** (Asset)✅
      - **url** (str)✅
      - **key** (str)✅
    - **colour** (Colour)✅
      - **r** (int)✅
      - **g** (int)✅
      - **b** (int)✅
    - **roles** (list[Role])✅
      - **id** (int)✅
      - **name** (str)✅
      - **hoist** (bool)✅
      - **managed** (bool)✅
      - **mentionable** (bool)✅
      - **colour** (Colour)✅
        - **r** (int)✅
        - **g** (int)✅
        - **b** (int)✅
      - **icon** (Asset)✅
        - **url** (str)✅
        - **key** (str)✅
  - **User**✅
    - **name** (str)✅
    - **id** (int)✅
    - **global_name** (str)✅
    - **bot** (bool)✅
    - **system** (bool)✅
    - **display_avatar** (Asset)✅
      - **url** (str)✅
      - **key** (str)✅

### Channel✅
- **channel** (TextChannel)✅
  - **name** (str)✅
  - **id** (int)✅
  - **category_id** (int)✅
  - **topic** (str)✅
  - **slowmode_delay** (int)✅
  - **nsfw** (bool)✅
  - **jump_url** (str)✅
  - **type** (str)✅

### Content✅
- **content** (str)✅

### Clean_content✅
- **clean_content** (str)✅

### Created_at✅
- **created_at** (datetime.datetime)✅

### Edited_at✅
- **edited_at** (datetime.datetime)✅

### Embeds✅
- **embeds** (list[Embed])✅
  - **title** (str)✅
  - **type** (str)✅
  - **description** (str)✅
  - **url** (str)✅
  - **colour** (Colour)✅
    - **r** (int)✅
    - **g** (int)✅
    - **b** (int)✅

### Flags✅
- **flags** (MessageFlags)✅
  - **value** (int)✅
  - **crossposted** (bool)✅
  - **is_crossposted** (bool)✅
  - **suppress_embeds** (bool)✅
  - **source_message_deleted** (bool)✅
  - **urgent** (bool)✅
  - **has_thread** (bool)✅
  - **ephemeral** (bool)✅
  - **suppress_notifications** (bool)✅
  - **voice** (bool)✅

### Metadata✅
- **id** (int)✅
- **interaction_metadata** (MessageInteractionMetadata)✅
  - **id** (int)✅

### URLs✅
- **jump_url** (str)✅

### Mentions✅
- **mention_everyone** (bool)✅
- **mentions** (list[User])✅
  - **name** (str)✅
  - **id** (int)✅
  - **global_name** (str)✅
  - **bot** (bool)✅
  - **system** (bool)✅
  - **display_avatar** (Asset)✅
    - **url** (str)✅
    - **key** (str)✅

### Message Properties✅
- **pinned** (bool)✅

### Polls✅
- **poll** (Poll)✅
  - **question** (str)✅
  - **answers** (list[PollAnswer])✅
    - **id** (int)✅
    - **text** (str)✅
    - **emoji** (Emoji)✅
      - **name** (str)✅
      - **id** (int)✅
      - **require_colons** (bool)✅
      - **animated** (bool)✅
      - **managed** (bool)✅
      - **guild_id** (int)✅
      - **available** (bool)✅
      - **url** (str)✅
    - **vote_count** (int)✅
  - **expires_at** (datetime.datetime)✅
  - **created_at** (datetime.datetime)✅
  - **total_votes** (int)✅

### Reactions✅
- **reactions** (list[Reaction])✅
  - **emoji**✅
    - **name** (str)✅
    - **id** (int)✅
    - **require_colons** (bool)✅
    - **animated** (bool)✅
    - **managed** (bool)✅
    - **guild_id** (int)✅
    - **available** (bool)✅
    - **url** (str)✅
  - **count** (int)✅

### References✅
- **reference** (MessageReference)✅
  - **message_id** (int)✅
  - **channel_id** (int)✅
  - **guild_id** (int)✅
  - **cached_message** (Message)✅
  - **jump_url** (str)✅

### Stickers✅
- **stickers** (list[StickerItem])✅
  - **name** (str)✅
  - **id** (int)✅
  - **format** (StickerFormatType)✅
  - **url** (str)✅

### System✅
- **system_content** (str)✅

### Threads
- **thread** (Thread)
  - **name** (str)
  - **id** (int)
  - **archived** (bool)
  - **locked** (bool)
  - **invitable** (bool)
  - **auto_archive_duration** (int)
  - **archive_timestamp** (datetime.datetime)
  - **type** (ChannelType)
  - **owner** (Member)
  - **jump_url** (str)

### Miscellaneous
- **tts** (bool)
- **type** (MessageType)
- **webhook_id** (int)
