from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import database


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if database.add_user(user):
        update.message.reply_text("✅ Welcome! You have been added to the database.")
    else:
        update.message.reply_text("🔄 You are already registered in the database.")


def handle_audio(update: Update, context: CallbackContext):
    audio_file_id = update.message.audio.file_id

    
    if 'audio_file_ids' not in context.user_data:
        context.user_data['audio_file_ids'] = []

    context.user_data['audio_file_ids'].append(audio_file_id)

    update.message.reply_text(
        "🎶 Audio received! Now select a playlist to add this (or these) audio(s):",
        reply_markup=ReplyKeyboardMarkup(
            [
                ['Home playlist', 'On the street playlist'],
                ['party playlist', 'favorites']
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )


def add_audio_to_playlist(update: Update, context: CallbackContext):
    user = update.message.from_user
    playlist_name = update.message.text

    valid_playlists = ['Home playlist', 'On the street playlist', 'party playlist', 'favorites']

    if playlist_name not in valid_playlists:
        update.message.reply_text(" Invalid playlist. Please use the keyboard.")
        return

    audio_file_ids = context.user_data.get('audio_file_ids', [])

    if not audio_file_ids:
        update.message.reply_text(" No audio found to add. Please send some music first.")
        return

    success_count = 0
    for file_id in audio_file_ids:
        if database.add_audio_to_playlist(user, playlist_name, file_id):
            success_count += 1

    update.message.reply_text(f" {success_count} audio(s) added to '{playlist_name}'!")

    
    context.user_data['audio_file_ids'] = []


def list_playlists(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_data = database.get_users(user)

    if not user_data:
        update.message.reply_text("🚫 You are not registered. Use /start first.")
        return

    playlists = user_data.get('playlist', [])
    if not playlists:
        update.message.reply_text("📭 You have no playlists yet.")
        return

    keyboard = [
        [InlineKeyboardButton(playlist['name'], callback_data=playlist['name'])]
        for playlist in playlists
    ]
    update.message.reply_text("🎵 Your playlists:", reply_markup=InlineKeyboardMarkup(keyboard))


def send_songs(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    user = query.from_user
    playlist_name = query.data
    user_data = database.get_users(user)

    if not user_data:
        query.edit_message_text(" You are not registered. Use /start.")
        return

    playlists = user_data.get('playlist', [])
    for playlist in playlists:
        if playlist['name'] == playlist_name:
            songs = playlist.get('songs', [])
            if not songs:
                query.edit_message_text(f" No songs in '{playlist_name}'.")
                return

            query.edit_message_text(f"🎧 Sending songs from '{playlist_name}':")
            for song in songs:
                query.message.reply_audio(audio=song['file_id'])
            return
