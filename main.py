import pyrogram
from pyrogram import Client,filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from os import environ, remove
from threading import Thread
from json import load
from re import search

from texts import HELP_TEXT
import bypasser
import freewall
from time import time


# bot
with open('config.json', 'r') as f: DATA = load(f)
def getenv(var): return environ.get(var) or DATA.get(var, None)

bot_token = getenv("TOKEN")
api_hash = getenv("HASH") 
api_id = getenv("ID")
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  


# handle ineex
def handleIndex(ele,message,msg):
    result = bypasser.scrapeIndex(ele)
    try: app.delete_messages(message.chat.id, msg.id)
    except: pass
    for page in result: app.send_message(message.chat.id, page, reply_to_message_id=message.id, disable_web_page_preview=True)


# loop thread
def loopthread(message,otherss=False):

    urls = []
    if otherss: texts = message.caption
    else: texts = message.text

    if texts in [None,""]: return
    for ele in texts.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0: return

    if bypasser.ispresent(bypasser.ddl.ddllist,urls[0]):
        msg = app.send_message(message.chat.id, "⚡ __generating...__", reply_to_message_id=message.id)
    elif freewall.pass_paywall(urls[0], check=True):
        msg = app.send_message(message.chat.id, "🕴️ __jumping the wall...__", reply_to_message_id=message.id)
    else:
        if "https://olamovies" in urls[0] or "https://psa.wf/" in urls[0]:
            msg = app.send_message(message.chat.id, "⏳ __this might take some time...__", reply_to_message_id=message.id)
        else:
            msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)

    strt = time()
    links = ""
    temp = None
    for ele in urls:
        if search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
            handleIndex(ele,message,msg)
            return
        elif bypasser.ispresent(bypasser.ddl.ddllist,ele):
            try: temp = bypasser.ddl.direct_link_generator(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        elif freewall.pass_paywall(ele, check=True):
            freefile = freewall.pass_paywall(ele)
            if freefile:
                try: 
                    app.send_document(message.chat.id, freefile, reply_to_message_id=message.id)
                    remove(freefile)
                    app.delete_messages(message.chat.id,[msg.id])
                    return
                except: pass
            else: app.send_message(message.chat.id, "__Failed to Jump", reply_to_message_id=message.id)
        else:    
            try: temp = bypasser.shortners(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        print("bypassed:",temp)
        if temp != None: links = links + temp + "\n"
    end = time()
    print("Took " + "{:.2f}".format(end-strt) + "sec")

    if otherss:
        try:
            app.send_photo(message.chat.id, message.photo.file_id, f'__{links}__', reply_to_message_id=message.id)
            app.delete_messages(message.chat.id,[msg.id])
            return
        except: pass

    try: 
        final = []
        tmp = ""
        for ele in links.split("\n"):
            tmp += ele + "\n"
            if len(tmp) > 4000:
                final.append(tmp)
                tmp = ""
        final.append(tmp)
        app.delete_messages(message.chat.id, msg.id)
        tmsgid = message.id
        for ele in final:
            tmsg = app.send_message(message.chat.id, f'__{ele}__',reply_to_message_id=tmsgid, disable_web_page_preview=True)
            tmsgid = tmsg.id
    except Exception as e:
        app.send_message(message.chat.id, f"__Failed to Bypass : {e}__", reply_to_message_id=message.id)
        


# start command
@app.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, f"__👋ʜɪ **{message.from_user.mention}**,ɪ ᴀᴍ ʟɪɴᴋ ʙʏᴘᴀꜱꜱᴇʀ ʙᴏᴛ, ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋꜱ ᴀɴᴅ ɪ ᴡɪʟʟ ʏᴏᴜ ɢᴇᴛ ʏᴏᴜ ʀᴇꜱᴜʟᴛꜱ.\n\nᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ <a href=https://t.me/professorr_x>Professorr</a>",
    reply_markup=InlineKeyboardMarkup([
        [ InlineKeyboardButton("ᴏᴡɴᴇʀ😈", url="https://t.me/professorr_x"),
        InlineKeyboardButton("ᴅᴏɴᴀᴛᴇ😥", url="https://telegra.ph/Buy-Me-Coffee-12-25")
        ],[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ‼", url="https://telegra.ph/Buy-Me-Coffee-12-25"),
         InlineKeyboardButton("ᴍᴏᴠɪᴇ ʀᴇQᴜᴇꜱᴛ ɢʀᴏᴜᴘ👻", url="https://t.me/terabox_movie_request_group")]]) 
        reply_to_message_id=message.id)


# help command
@app.on_message(filters.command(["help"]))
def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, HELP_TEXT, reply_to_message_id=message.id, disable_web_page_preview=True)


# links
@app.on_message(filters.text)
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = Thread(target=lambda:loopthread(message),daemon=True)
    bypass.start()


# doc thread
def docthread(message):
    msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)
    print("sent DLC file")
    file = app.download_media(message)
    dlccont = open(file,"r").read()
    links = bypasser.getlinks(dlccont)
    app.edit_message_text(message.chat.id, msg.id, f'__{links}__', disable_web_page_preview=True)
    remove(file)


# files
@app.on_message([filters.document,filters.photo,filters.video])
def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    
    try:
        if message.document.file_name.endswith("dlc"):
            bypass = Thread(target=lambda:docthread(message),daemon=True)
            bypass.start()
            return
    except: pass

    bypass = Thread(target=lambda:loopthread(message,True),daemon=True)
    bypass.start()


# server loop
print("Bot Starting")
app.run()
