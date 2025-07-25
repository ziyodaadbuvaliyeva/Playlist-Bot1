from config import TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import handlers

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", handlers.start))
    dp.add_handler(CommandHandler("list_playlists", handlers.list_playlists))

    dp.add_handler(MessageHandler(Filters.audio, handlers.handle_audio))
    dp.add_handler(MessageHandler(Filters.text, handlers.add_audio_to_playlist))

    dp.add_handler(CallbackQueryHandler(
        handlers.send_songs,
        pattern='^(Home playlist|On the street playlist|party playlist|favorites)$'
    ))

    updater.start_polling()
    updater.idle()

main()

