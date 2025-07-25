from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from handlers import start, ask_for_music, handle_audio, add_audio_to_playlist, done_sending, list_playlists, show_playlist_songs
from config import TOKEN

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex('^ Send Music$'), ask_for_music))
    dp.add_handler(MessageHandler(Filters.audio, handle_audio))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, add_audio_to_playlist))
    dp.add_handler(CommandHandler("done", done_sending))
    dp.add_handler(CommandHandler("playlists", list_playlists))
    dp.add_handler(CallbackQueryHandler(show_playlist_songs, pattern='^show_'))

    updater.start_polling()
    print(" Bot ishga tushdi!")
    updater.idle()

if __name__ == "__main__":
    main()
