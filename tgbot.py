import requests
import tgtypes

class Bot():
    def __init__(self,token):
        self.token = token
        self.url = 'https://api.telegram.org/bot{}/'.format(token)

    parse_mode_markdown = 'Markdown'
    parse_mode_html = 'HTML'
    def send_message(self, chat_id,text,parse_mode = None,
                     disable_web_page_preview = False,
                     disable_notification = False,
                     reply_to_message_id = None,
                     reply_to_markup = None):
        """
        :param chat_id: required int()
        :param text:  required str()
        :param parse_mode: Bot.parse_mode_markdown or
                           Bot.parse_mode_html
        :param disable_web_page_preview: optional bool()
        :param disable_notification: optional bool()
        :param reply_to_message_id:  optional int()
        :param reply_to_markup: optional InlineKeyboardMarkup or
                                ReplyKeyboardMarkup or
                                ReplyKeyboardRemove or
                                ForceReply
        :return: deserialized json with bool() field "ok"
                 if ["ok"] == false it has also "error_code" int() field
                 and "description" that is str()
        """
        args = dict(chat_id=chat_id, text=text, parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    reply_to_message_id=reply_to_message_id,
                    reply_to_markup=reply_to_markup)
        conn = requests.get(self.url+'sendMessage', params=args)
        return conn.json()

    def send_audio(self,chat_id,audio):
        args = dict(chat_id = chat_id,audio = audio)
        conn = requests.get(self.url+'sendAudio',params=args)
        return conn.json()

    def send_photo(self,chat_id,photo):
        args = dict(chat_id = chat_id, photo = photo)
        conn = requests.get(self.url + 'sendPhoto', params=args)
        return conn.json()

    def get_file(self,file_id):
        """
        :param file_id: string()
        :return: deserialized json with bool() field "ok"
                 and field "result". "result" has "file_id",
                 "file_size","file_path".
                 if ["ok"] == false it has also "error_code" int() field
                 and "description" that is str()
        """
        args = dict(file_id = file_id)
        conn = requests.get(self.url+'getFile',params=args)
        return  conn.json()