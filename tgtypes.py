class Update():
    def __init__(self, json_str):
        self.UpdateId = json_str.get('update_id')  # int
        self.Message = Message(json_str.get('message'))  # message

class User():
    def __init__(self, user_dict):
        self.Id = user_dict.get('id')  # int
        self.IsBot = user_dict.get('is_bot') # bool()
        self.FirstName = user_dict.get('first_name')  # string
        self.LastName = user_dict.get('last_name')  # string
        self.Username = user_dict.get('username')  # string
        self.LanguageCode = user_dict.get('language_code')  # str()

class Chat():
    def __init__(self, chat_dict):
        self.Id = chat_dict.get('id')  # int
        # Type of chat, can be
        # either “private”, “group”,
        # “supergroup” or “channel”
        self.Type = chat_dict.get('type')  # string
        self.Title = chat_dict.get('title')  # string
        self.Username = chat_dict.get('username')  # string
        self.FirstName = chat_dict.get('first_name')  # string
        self.LastName = chat_dict.get('last_name')  # string

    @property
    def id(self):
        return self.Id

    @property
    def type(self):
        return  self.Type

    @property
    def title(self):
        return self.Title

    @property
    def username(self):
        return self.Username

    @property
    def first_name(self):
        return self.FirstName

    @property
    def last_name(self):
        return self.LastName

class Message():
    def __init__(self, message_dict):
        self.MessageId = message_dict.get('message_id')  # int
        self.From = User(message_dict.get('from'))  # User
        self.Date = message_dict.get('date')  # int (time since epoch)
        self.Chat = Chat(message_dict.get('chat'))  # Chat

        ff = message_dict.get('forward_from')
        if ff is not None:
            ff = User(ff)
        self.ForwardFrom = ff  # User

        ffc = message_dict.get('forward_from_chat')
        if ffc is not None:
            ffc = Chat(ffc)
        self.ForwardFromChat = ffc


        self.ForwardFromMessageId = message_dict.get('forward_from_message_id')  # int()
        self.ForwardSignature = message_dict.get('forward_signature')  # str()
        self.ForwardDate = message_dict.get('forward_date')

        rtm = message_dict.get('reply_to_message')
        if rtm is not None:
            rtm = Message(rtm)
        self.ReplyToMessage = rtm


        self.EditDate = message_dict.get('edit_date') # int()
        self.MediaGroupId = message_dict.get('media_group_id')
        self.AuthorSignature = message_dict.get('author_signature')
        self.Text = message_dict.get('text')  # str()

        ent = message_dict.get('entities')
        if ent is not None:
            entities_list = [MessageEntity(entity) for entity in ent]
            ent = entities_list
        self.Entities = ent

        cap_ent = message_dict.get('caption_entities')
        if cap_ent is not None:
            entities_list = [MessageEntity(caption_entity) for caption_entity in cap_ent]
            cap_ent = entities_list
        self.CaptionEntities = cap_ent


        #audio
        #document
        #photo
        #sticker
        #video
        vc = message_dict.get('voice')
        if vc is not None:
            vc = Voice(vc)
        self.Voice = vc

        #video_note
        #caption

class MessageEntity():
    def __init__(self,mess_en_dict):
        self.Type = mess_en_dict.get('type')
        self.Offset = mess_en_dict.get('offset')  # int()
        self.Length = mess_en_dict.get('length') # int()
        self.Url = mess_en_dict.get('url') #str()

        u = mess_en_dict.get('user')
        if u is not None:
            u = Chat(u)
        self.User = u

class PhotoSize():
    def __init__(self,photo_sz_dict):
        self.FileId = photo_sz_dict.get('file_id')
        self.Width = photo_sz_dict.get('width')
        self.Height = photo_sz_dict.get('height')
        self.FileSize = photo_sz_dict.get('file_size')

class Audio():
    def __init__(self,audio_dict):
        self.FileId = audio_dict.get('file_id')
        self.Duration = audio_dict.get('duration')
        self.Performer = audio_dict.get('performer')
        self.Title = audio_dict.get('title')
        self.MimeType = audio_dict.get('mime_type')
        self.FileSize = audio_dict.get('file_size')







class Voice():
    def __init__(self,voice_dict):
        self.FileId = voice_dict.get('file_id')
        self.Duration = voice_dict.get('duration')
        self.MimeType = voice_dict.get('mime_type')
        self.FileSize = voice_dict.get('file_size')