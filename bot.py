# ©️ LISA-KOREA | @LISA_FAN_LK | NT_BOT_CHANNEL | LISA-KOREA/YouTube-Video-Download-Bot

# [⚠️ Do not change this repo link ⚠️] :- https://github.com/LISA-KOREA/YouTube-Video-Download-Bot

import logging
import asyncio
import yt_dlp
from pyrogram import Client, filters

# Replace these with your actual API ID, API Hash, and Bot Token
API_ID = 21349365
API_HASH = '3cc94b13c23e232d282c2293963c213e'
BOT_TOKEN = '7262630597:AAF4c4raNMqM4HEAAB2nEYoIFFr3yTrTAVo'

youtube_dl_username = None  
youtube_dl_password = None 

# Dictionary to store chat states
user_states = {}

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Welcome! Use /yt to download a YouTube video.")

@app.on_message(filters.command("yt"))
async def ask_for_youtube_link(client, message):
    chat_id = message.chat.id
    user_states[chat_id] = "waiting_for_link"
    await message.reply_text("Please paste the YouTube link now.")

@app.on_message(filters.text & filters.regex(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'))
async def process_youtube_link(client, message):
    chat_id = message.chat.id
    if user_states.get(chat_id) != "waiting_for_link":
        return  # Ignore if no `/yt` command was given before
    
    youtube_link = message.text
    try:
        downloading_msg = await message.reply_text("Downloading video...")

        ydl_opts = {
            'outtmpl': 'downloaded_video_%(id)s.%(ext)s',
            'progress_hooks': [lambda d: print(d['status'])],
            'cookiefile': 'cookies.txt'
        }

        if youtube_dl_username is not None:
            ydl_opts['username'] = youtube_dl_username
        if youtube_dl_password is not None:
            ydl_opts['password'] = youtube_dl_password

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=False)
            title = info_dict.get('title', None)

            if title:
                ydl.download([youtube_link])
                uploading_msg = await message.reply_text("Uploading video...")
                video_filename = f"downloaded_video_{info_dict['id']}.mp4"
                with open(video_filename, 'rb') as video_file:
                    await client.send_video(chat_id, video=video_file, caption=title)

                await asyncio.sleep(2)
                await downloading_msg.delete()
                await uploading_msg.delete()

                await message.reply_text("\n\nOWNER : @LISA_FAN_LK 💕\n\nSUCCESSFULLY UPLOADED!")
            else:
                logging.error("No video streams found.")
                await message.reply_text("Error: No downloadable video found.")
    except Exception as e:
        logging.exception("Error processing YouTube link: %s", e)
        await message.reply_text("Error: Failed to process the YouTube link. Please try again later.")
    finally:
        # Reset the state after processing
        user_states[chat_id] = None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run()
