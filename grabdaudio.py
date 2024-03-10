import os
import subprocess
from telegram.ext import Updater, CommandHandler

# Token del bot de Telegram
BOT_TOKEN = '7016184289:AAGdf0Pl6m6uN4JVZf55NdmxAdCwYHc8PDQ'

# ID del chat donde se enviará el audio
CHAT_ID = '5827778078'

# Ruta del archivo de audio
AUDIO_FILE = 'audio.mp3'

# Crear instancia del updater
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Manejador de comando /iniciargrabacion
def start_recording(update, context):
    # Verificar si ya hay una grabación en curso
    if os.path.exists(AUDIO_FILE):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ya hay una grabación en curso. Utiliza el comando /detenergrabacion para detenerla.')
        return

    # Iniciar la grabación de audio en segundo plano
    subprocess.Popen(['termux-microphone-record', '-q', '-e', AUDIO_FILE])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Grabación de audio iniciada.')

# Manejador de comando /detenergrabacion
def stop_recording(update, context):
    # Verificar si hay una grabación en curso
    if not os.path.exists(AUDIO_FILE):
        context.bot.send_message(chat_id=update.effective_chat.id, text='No hay una grabación en curso. Utiliza el comando /iniciargrabacion para iniciarla.')
        return

    # Detener la grabación de audio
    subprocess.Popen(['termux-microphone-record', '--action', 'stop'])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Grabación de audio detenida.')

    # Convertir el archivo de audio a formato MP3
    subprocess.Popen(['ffmpeg', '-i', AUDIO_FILE, AUDIO_FILE.replace('.mp3', '.ogg')])
    os.rename(AUDIO_FILE.replace('.mp3', '.ogg'), AUDIO_FILE)

    # Enviar el archivo de audio al chat
    context.bot.send_audio(chat_id=CHAT_ID, audio=open(AUDIO_FILE, 'rb'))

# Agregar los manejadores de comandos al dispatcher
start_handler = CommandHandler('iniciargrabacion', start_recording)
dispatcher.add_handler(start_handler)

stop_handler = CommandHandler('detenergrabacion', stop_recording)
dispatcher.add_handler(stop_handler)

# Iniciar el bot
updater.start_polling()