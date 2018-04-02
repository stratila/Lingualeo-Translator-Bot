import requests
import re

class TranslateData:
    def __init__(self,data):
        self.is_valid = False
        self.__picture = None
        self.__translates = None
        self.__transcription = None
        self.__sound = None
        if data.get('error_msg') == '':
            self.is_valid = True
            self.__picture = data.get('pic_url')
            self.__translates = [word.get('value') for word in data.get('translate')]
            self.__pictures = [word.get('pic_url') for word in data.get('translate')]
            self.__transcription = data.get('transcription')
            self.__default_sound = data.get('sound_url')
            m = re.search(r'/[\w-]+\.mp3',self.__default_sound )
            if m:
                self.__sound = 'http://audiocdn.lingualeo.com/v2/0{}'.format(m.group())
                print(m.group())


    def __bool__(self):
        return self.is_valid

    @property
    def picture(self):
        return self.__picture

    @property
    def translates(self):
        return self.__translates

    @property
    def pictures(self):
        return self.__pictures

    @property
    def transcription(self):
        return  self.__transcription

    @property
    def sound(self):
        return  self.__sound

    @property
    def default_sound(self):
        return self.__default_sound

def get_translates(word):
    url = 'http://api.lingualeo.com/gettranslates'
    args = {'word' : word}
    conn = requests.get(url=url,params=args)
    return TranslateData(conn.json())

def send_translate(bot,chat_id,text):

    translate_result = get_translates(text)

    if not translate_result:
        sending_text = 'There is no translate for *%s* 🤔 \n See ' \
                       '\\help command if you want to translate from Russian' % text
        return bot.send_message(chat_id=chat_id,
                                text = sending_text,
                                parse_mode=bot.parse_mode_markdown)

    sending_text = '🔎 Translates for *%s*\n\n' % text
    if translate_result.transcription is not None:
        sending_text+='🔑 Transcription: _%s_\n' % translate_result.transcription

    for translated_word in translate_result.translates:
        line = '📌 {}\n'.format(translated_word)
        sending_text += line

    if translate_result.picture is not None:
        bot.send_photo(chat_id=chat_id,photo=translate_result.picture)

    bot.send_message(chat_id=chat_id,
                     text=sending_text,
                     parse_mode=bot.parse_mode_markdown)

    if translate_result.sound is not None:
        bot.send_audio(chat_id=chat_id,audio=translate_result.sound)
    else:
        bot.send_audio(chat_id=chat_id, audio=translate_result.default_sound)


