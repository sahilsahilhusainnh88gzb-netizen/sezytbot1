from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()
    import os
import yt_dlp
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
BOT_TOKEN = '8486804481:AAGeW5hcI1QMSoF_Tvtws4OvmJDG36PxpII'
OWNER_NAME = "Sez YT" 
INSTAGRAM_URL = "https://www.instagram.com/im_sahil_sez/"

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        f"👋 Hello! Main hu YouTube Downloader Bot.\n\n"
        f"👤 **Owner:** {SEZ YT}\n"
        f"📸 **Instagram:** [Follow Me]({https://www.instagram.com/im_sahil_sez/})\n\n"
        "Commands:\n"
        "🎵 `/mp3 [link]` - Audio download karne ke liye\n"
        "🎬 Just send link - Video download karne ke liye"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown', disable_web_page_preview=True)

# --- FUNCTION: MP3 DOWNLOAD ---
async def download_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Link toh do bhai! Example: `/mp3 https://youtube.com/...`")
        return

    url = context.args[0]
    status_msg = await update.message.reply_text("🎵 Audio nikal raha hoon... (Original Name)")

    # MP3 Settings: Original Title ke liye '%(title)s' setup
    ydl_opts_mp3 = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s', 
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_mp3) as ydl:
            info = ydl.extract_info(url, download=True)
            # Original title nikalna
            original_title = info.get('title', 'audio')
            filename = f"{original_title}.mp3"

        if os.path.exists(filename):
            await status_msg.edit_text(f"📤 Uploading: {original_title}")
            with open(filename, 'rb') as audio:
                await update.message.reply_audio(
                    audio=audio, 
                    caption=f"✅ Audio: {original_title}\n👤 Owner: {OWNER_NAME}\n📸 Insta: {INSTAGRAM_URL}",
                    write_timeout=300
                )
            await status_msg.delete()
            os.remove(filename) 
        else:
            await status_msg.edit_text("❌ Error: MP3 file PC mein nahi mili.")

    except Exception as e:
        await status_msg.edit_text(f"❌ Audio Error: {str(e)}")

# --- FUNCTION: VIDEO DOWNLOAD ---
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        return

    status_msg = await update.message.reply_text("🎬 Video process ho rahi hai...")

    ydl_opts_video = {
        'format': 'best[height<=480][ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'video')
            filename = f"{video_title}.mp4"

        if os.path.exists(filename):
            file_size_mb = os.path.getsize(filename) / (1024 * 1024)

            if file_size_mb > 50:
                await status_msg.edit_text(f"❌ Size {file_size_mb:.1f}MB hai! Limit 50MB hai.")
                os.remove(filename)
            else:
                await status_msg.edit_text(f"📤 Uploading Video: {video_title}")
                with open(filename, 'rb') as video:
                    await update.message.reply_video(
                        video=video, 
                        caption=f"✅ Video: {video_title}\n👤 Owner: {OWNER_NAME}\n📸 Insta: {https://www.instagram.com/im_sahil_sez/}",
                        write_timeout=600
                    )
                await status_msg.delete()
                os.remove(filename)
        else:
            await status_msg.edit_text("❌ Video file download nahi hui.")

    except Exception as e:
        await status_msg.edit_text(f"❌ Video Error: {str(e)}")

# --- MAIN ---
def main():
    # Token yahan add kar diya hai
    app = Application.builder().token(8486804481:AAGeW5hcI1QMSoF_Tvtws4OvmJDG36PxpII).connect_timeout(120).write_timeout(600).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mp3", download_mp3))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print(f"━━━━━━━━━━━━━━━━━━━━━")
    print(f"Bot Active: {OWNER_NAME}")
    print(f"━━━━━━━━━━━━━━━━━━━━━")
    app.run_polling()

if __name__ == '__main__':
    main()
