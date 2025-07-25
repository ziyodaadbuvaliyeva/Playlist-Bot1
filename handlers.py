from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import database

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    added = database.add_user(user)
    if added:
        update.message.reply_text(" Welcome! You have been added to the database.")
    else:
        update.message.reply_text(" You are already registered.")

    keyboard = ReplyKeyboardMarkup(
        [['🎵 Send Music', '📂 View Playlists']],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    update.message.reply_text("Choose an option:", reply_markup=keyboard)

def ask_for_music(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please send me 3 or 4 audio files one by one.\nWhen done, send /done."
    )
    context.user_data['audio_file_ids'] = []

def handle_audio(update: Update, context: CallbackContext):
    audio = update.message.audio
    if not audio:
        update.message.reply_text("Please send a valid audio file.")
        return

    if 'audio_file_ids' not in context.user_data:
        context.user_data['audio_file_ids'] = []

    context.user_data['audio_file_ids'].append(audio.file_id)

    
    playlists = [
        ['Home playlist', 'On the street playlist'],
        ['Party playlist', 'Favorites']
    ]
    reply_markup = ReplyKeyboardMarkup(playlists, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        f"🎶 Received {len(context.user_data['audio_file_ids'])} audio(s).\n"
        "Send more or select playlist to add:",
        reply_markup=reply_markup
    )

def add_audio_to_playlist(update: Update, context: CallbackContext):
    playlist_name = update.message.text
    valid_playlists = ['Home playlist', 'On the street playlist', 'Party playlist', 'Favorites']

    if playlist_name not in valid_playlists:
        update.message.reply_text(" Invalid playlist name. Please use keyboard buttons.")
        return

    audio_file_ids = context.user_data.get('audio_file_ids', [])
    if not audio_file_ids:
        update.message.reply_text(" You have not sent any audio files yet.")
        return

    user = update.message.from_user
    added_count = 0
    for file_id in audio_file_ids:
        if database.add_audio_to_playlist(user, playlist_name, file_id):
            added_count += 1

    update.message.reply_text(f" Added {added_count} audio(s) to '{playlist_name}'!")

    context.user_data['audio_file_ids'] = []
    
    playlists = [
        ['Home playlist', 'On the street playlist'],
        ['Party playlist', 'Favorites']
    ]
    reply_markup = ReplyKeyboardMarkup(playlists, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("You can send more audio or /done to finish.", reply_markup=reply_markup)

def done_sending(update: Update, context: CallbackContext):
    if 'audio_file_ids' in context.user_data and context.user_data['audio_file_ids']:
        update.message.reply_text(" Your music has been saved! Use /playlists to see your playlists.", reply_markup=ReplyKeyboardMarkup([['🎵 Send Music', ' View Playlists']], resize_keyboard=True))
        context.user_data['audio_file_ids'] = []
    else:
        update.message.reply_text("You haven't sent any audio yet.")

def list_playlists(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_data = database.get_user_data(user)
    if not user_data:
        update.message.reply_text("🚫 You are not registered. Use /start.")
        return

    playlists = user_data.get('playlist', [])
    if not playlists:
        update.message.reply_text("📭 You have no playlists yet.")
        return

    keyboard = [
        [InlineKeyboardButton(pl['name'], callback_data=f"show_{pl['name']}")] for pl in playlists
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🎵 Your playlists:", reply_markup=reply_markup)

def show_playlist_songs(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data

    if not data.startswith("show_"):
        return

    playlist_name = data[5:]
    user_data = database.get_user_data(user)
    if not user_data:
        query.answer("You are not registered. Use /start.", show_alert=True)
        return

    for pl in user_data.get('playlist', []):
        if pl['name'] == playlist_name:
            songs = pl.get('songs', [])
            if not songs:
                query.edit_message_text(f"No songs in '{playlist_name}'.")
                return

            query.edit_message_text(f"🎧 Songs in '{playlist_name}':")
            for song in songs:
                context.bot.send_audio(chat_id=query.message.chat_id, audio=song['file_id'])
            return
