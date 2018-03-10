from flask import Flask, request, make_response
from tgbot import Bot
from tgtypes import Update, InlineQuery, InlineQueryResultPhoto, InputTextMessageContent
from translate import send_translate, get_translates
import start_command
import help_command
import json
from wit import Wit
from os import path
import os
import urllib.request
import cloudconvert
import random
import string


app = Flask(__name__)
bot = Bot('486458556:AAHOgHe39oNIYJgUOxzf-hH6Hp28mBAXF3I')
convert_client = cloudconvert.Api("_xzKzdqMWtaqtLEQEVuKJZtG47rL4ck70zeYU" 
                                  "-_C2VKdU17V3tAIqhPoR4eYm6mxBwjfFgNP3OlecWtWO6uSyg")
voice_client = Wit(access_token="EFM2XCEDOKQVQDA5PGDYWEZYH3PXMYOT")


@app.route('/')
def hello_world():
    return 'Telegram app'

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def handle_command(update):
    chat_id = update.Message.Chat.id
    if update.Message.Text == '/help':
        bot.send_message(chat_id=chat_id,
                         text=help_command.help1(),
                         parse_mode=bot.parse_mode_markdown,
                         disable_web_page_preview=True)
        bot.send_message(chat_id, text=help_command.help2())
    elif update.Message.Text == '/start':
        bot.send_message(chat_id=chat_id,
                         text=start_command.start(),
                         parse_mode=bot.parse_mode_markdown,
                         disable_web_page_preview=True)
    else:
        bot.send_message(chat_id=chat_id,text='Oops! Unknown command 🤷')

def handle_voice(update):
    chat_id = update.Message.Chat.id
    voice_info = bot.get_file(update.Message.Voice.FileId)
    if(voice_info.get("ok") == False):
        messages = ["Something goes wrong!😢","Try again. 😉"]
        for txt in messages:
            bot.send_message(chat_id=chat_id,text = txt)

    file_path = voice_info.get("result").get("file_path")
    url = "https://api.telegram.org/file/bot{}/{}".format(bot.token,file_path)

    file_name = id_generator()

    with urllib.request.urlopen(url) as f:
        with open(file_name+'.ogg', 'wb') as fin:
            fin.write(f.read()) # create ogg file

    process = None
    try:
        process = convert_client.convert({
            "inputformat": "ogg",
            "outputformat": "mp3",
            "input": "upload",
            "file": open(path.join(path.dirname(path.realpath(file_name+'.ogg')), file_name+'.ogg'), 'rb')
        })
        process.wait()
    except:
        if path.exists(file_name + '.ogg'):
            print('zero remove')
            os.remove(file_name+'.ogg')
            print(path.exists(file_name + '.ogg'))
            messages = ["Something goes wrong!😢", "Try later. 😉"]
            for txt in messages:
                bot.send_message(chat_id=chat_id, text=txt)
            return

    process.download() # create mp3 file

    voice_text = None
    with open(path.join(path.dirname(path.realpath(file_name + '.mp3')), file_name + '.mp3'), 'rb') as file:
        try:
            voice_text = voice_client.speech(file, headers={'Content-Type': 'audio/mpeg'})
        except:
            if path.exists(file_name+'.ogg') and path.exists(file_name+'.mp3'):
                print("the first exists")
                os.remove(file_name+'.ogg')
                os.remove(file_name+'.mp3')
                print(path.exists(file_name + '.ogg'), path.exists(file_name + '.mp3'))
                return bot.send_message(chat_id=chat_id,text="Couldn't recognize what you said ☹")


    send_translate(bot,chat_id,voice_text['_text']) # send result
    if path.exists(file_name + '.ogg') and path.exists(file_name + '.mp3'):
        print("the second exists")
        os.remove(file_name + '.ogg')
        os.remove(file_name + '.mp3')
        print(path.exists(file_name + '.ogg'), path.exists(file_name + '.mp3'))



def inline_processing(update):
    text = update.InlineQuery.Query
    id = update.InlineQuery.Id
    translate_obj = get_translates(text)
    inlq_results = [InlineQueryResultPhoto(id=picture,
                                           photo_url=picture,
                                           thumb_url=picture,
                                           title='❤',
                                           description=translate,
                                           input_message_content=InputTextMessageContent(message_text=translate)
                                           ).serialized()
                    for translate,picture in zip(translate_obj.translates, translate_obj.pictures)
                    ]
    print(inlq_results)
    bot.answer_inline_query(inline_query_id=id,results=inlq_results)

def message_processing(update):
    if update.Message.Text is not None:
        if update.Message.Text[0] == '/':
            handle_command(update)
        else:
            send_translate(bot,chat_id=update.Message.Chat.id,text=update.Message.Text)
    elif update.Message.Voice is not None:
        if update.Message.Chat.id == 164898079:
            handle_voice(update)
        else:
            bot.send_message(update.Message.Chat.id, "Voice recognition temporary is not available. 🤐")
    else:
        bot.send_message(update.Message.Chat.id,"Hmm... 🤔🤔🤔 Try to send something else.")



@app.route('/webhook/', methods=['POST',])
def handle_update():

    update_dict = request.data
    print(update_dict)
    update = Update(json.loads(update_dict))
    if update.InlineQuery is not None:
        inline_processing(update)
    else:
        message_processing(update)
    return make_response(('Ok',200,))


if __name__ == '__main__':
    app.run()