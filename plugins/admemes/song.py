

from pyrogram import Client, filters

import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
import time

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------

@Client.on_message(filters.command("song") & ~filters.channel & ~filters.edited)
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('`π»π₯πππ½πππ πΈπππ π²ππππΆ.....`')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"[α΄α΄Ι’Ι΄α΄s α΄Ι’ α΄α΄sΙͺα΄]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**<b>π¨ πΊπ π­ππ π₯ππππ½ π±πΎππππ π¨π πΈπππ π±πΎπππΎππ β€οΈ.π―ππΎπΊππΎ π³ππ π πππππΎπ π²πππ π?π π΄ππΎ π’ππππΎπΌπ πΆπππ½π!</b>**')
            return
    except Exception as e:
        m.edit(
            "**π€πππΎπ ππ²πππ π­πΊππΎ πΆπππ π’ππππΊππ½π**β\nπ₯ππ π€ππΊππππΎ: `/song Alone Marshmellow`"
        )
        print(str(e))
        return
    m.edit("`π΄ππππΊπ½πππ...π»`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'πΉ <b>π³ππππΎ:</b> <a href="{link}">{title}</a>\nποΈ <b>π£πππΊππππ:</b> <code>{duration}</code>\nπ΅ <b>π΅ππΎππ:</b> <code>{views}</code>\nπ» <b>π±πΎπππΎπππΎπ½ π‘π:</b> {message.from_user.mention()} \nπΆ <b>π΄ππππΊπ½πΎπ½ π‘π: @Universal_MoviesZ</b> π'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
        message.delete()
    except Exception as e:
        m.edit('**π π π€ππππ π?πΌπΌπππΎπ½ π―ππΎπΊππΎ π±πΎππππ π³πππ ππ @MagnusTG !!**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
