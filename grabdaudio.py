import os
import subprocess
import telebot

# Token del bot de Telegram
BOT_TOKEN = '7016184289:AAGdf0Pl6m6uN4JVZf55NdmxAdCwYHc8PDQ'

# ID del chat donde se enviará el audio
CHAT_ID = 5827778078

# Ruta del archivo de audio
AUDIO_FILE = 'audio.mp3'

# Crear instancia del bot
bot = telebot.TeleBot(BOT_TOKEN)
# Eliminar el webhook
bot.delete_webhook()
# Manejador de comando /iniciargrabacion
@bot.message_handler(commands=['iniciargrabacion'])
def start_recording(message):
    # Verificar si ya hay una grabación en curso
    if os.path.exists(AUDIO_FILE):
        bot.reply_to(message, 'Ya hay una grabación en curso. Utiliza el comando /detenergrabacion para detenerla.')
        return

    # Iniciar la grabación de audio en segundo plano
    subprocess.Popen(['termux-microphone-record', '-q', '-e', AUDIO_FILE])
    bot.reply_to(message, 'Grabación de audio iniciada.')

# Manejador de comando /detenergrabacion
@bot.message_handler(commands=['detenergrabacion'])
def stop_recording(message):
    # Verificar si hay una grabación en curso
    if not os.path.exists(AUDIO_FILE):
        bot.reply_to(message, 'No hay una grabación en curso. Utiliza el comando /iniciargrabacion para iniciarla.')
        return

    # Detener la grabación de audio
    subprocess.Popen(['termux-microphone-record', '--action', 'stop'])
    bot.reply_to(message, 'Grabación de audio detenida.')

    # Convertir el archivo de audio a formato MP3
    subprocess.Popen(['ffmpeg', '-i', AUDIO_FILE, AUDIO_FILE.replace('.mp3', '.ogg')])
    os.rename(AUDIO_FILE.replace('.mp3', '.ogg'), AUDIO_FILE)

    # Enviar el archivo de audio al chat
    bot.send_audio(CHAT_ID, open(AUDIO_FILE, 'rb'))

# Iniciar el bot
bot.polling()
