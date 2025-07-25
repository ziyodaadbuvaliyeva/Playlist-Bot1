from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from handlers import start, handle_audio, add_audio_to_playlist, list_playlists, send_songs
from config import TOKEN

def main():
    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("playlists", list_playlists))

    
    dp.add_handler(MessageHandler(Filters.audio, handle_audio))

    
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, add_audio_to_playlist))

    
    dp.add_handler(CallbackQueryHandler(send_songs))


    updater.start_polling()
    print("🤖 Bot ishga tushdi!")
    updater.idle()

if __name__ == '__main__':
    main()
