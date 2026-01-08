import os
import yt_dlp
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup (Errors dekhne ke liye)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = '8486804481:AAGeW5hcI1QMSoF_Tvtws4OvmJDG36PxpII'

# --- FUNCTION: MP3 DOWNLOAD ---
async def download_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Link toh do bhai! Example: `/mp3 https://youtube.com/...`")
        return
    
    url = context.args[0]
    status_msg = await update.message.reply_text("🎵 MP3 nikaal raha hoon... (SEZ YT H4KS)")

    # MP3 Settings: FFmpeg ko force kar rahe hain mp3 banane ke liye
    ydl_opts_mp3 = {
        'format': 'bestaudio/best',
        'outtmpl': 'sez_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_mp3) as ydl:
            ydl.download([url])
        
        # Sahi file name check karna
        filename = 'sez_audio.mp3'
        
        if os.path.exists(filename):
            await status_msg.edit_text("📤 Audio upload ho raha hai...")
            with open(filename, 'rb') as audio:
                await update.message.reply_audio(
                    audio=audio, 
                    caption="✅ Audio by SEZ YT H4KS",
                    write_timeout=300 # 5 minute upload time
                )
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Error: MP3 file nahi mili. FFmpeg check karein!")

    except Exception as e:
        print(f"Audio Error: {e}")
        await status_msg.edit_text(f"❌ Audio Error: {str(e)}")
    
    finally:
        if os.path.exists('sez_audio.mp3'):
            os.remove('sez_audio.mp3')

# --- FUNCTION: VIDEO DOWNLOAD ---
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        return

    status_msg = await update.message.reply_text("🎬 Video process ho rahi hai... (SEZ YT H4KS)")

    ydl_opts_video = {
        'format': 'best[height<=480][ext=mp4]/best', # Size chota rakhne ke liye 480p default
        'outtmpl': 'sez_video.mp4',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([url])

        if os.path.exists('sez_video.mp4'):
            file_size_mb = os.path.getsize('sez_video.mp4') / (1024 * 1024)
            
            if file_size_mb > 50:
                await status_msg.edit_text(f"❌ Size {file_size_mb:.1f}MB hai! Telegram limit 50MB hai.")
            else:
                await status_msg.edit_text("📤 Uploading Video...")
                with open('sez_video.mp4', 'rb') as video:
                    await update.message.reply_video(
                        video=video, 
                        caption=f"✅ Video by SEZ YT H4KS\n📊 Size: {file_size_mb:.2f} MB",
                        write_timeout=600
                    )
                await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Download fail ho gaya.")
            
    except Exception as e:
        print(f"Video Error: {e}")
        await status_msg.edit_text(f"❌ Video Error: {str(e)}")
    
    finally:
        if os.path.exists('sez_video.mp4'):
            os.remove('sez_video.mp4')

# --- MAIN ---
def main():
    # Timeout settings ko aur badha diya hai
    app = Application.builder().token(BOT_TOKEN).connect_timeout(120).write_timeout(600).build()
    
    app.add_handler(CommandHandler("mp3", download_mp3))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("━━━━━━━━━━━━━━━━━━━━━")
    print("YT Bot LIVE (Video + MP3) - SEZ YT H4KS")
    print("━━━━━━━━━━━━━━━━━━━━━")
    app.run_polling()

if __name__ == '__main__':
    main()