import json
import os

DATA_PATH = 'database/data.json'

def _load_data():
    if not os.path.exists(DATA_PATH):
        return {"users": []}
    with open(DATA_PATH, 'r') as f:
        try:
            return json.load(f)
        except:
            return {"users": []}

def _save_data(data):
    with open(DATA_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def add_user(user):
    data = _load_data()
    for u in data['users']:
        if u['telegram_id'] == user.id:
            return False
    data['users'].append({
        'telegram_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'playlist': [
            {'name': 'Home playlist', 'songs': []},
            {'name': 'On the street playlist', 'songs': []},
            {'name': 'party playlist', 'songs': []},
            {'name': 'favorites', 'songs': []}
        ]
    })
    _save_data(data)
    return True

def get_users(user):
    data = _load_data()
    for u in data['users']:
        if u['telegram_id'] == user.id:
            return u
    return None

def add_audio_to_playlist(user, playlist_name, file_id):
    data = _load_data()
    for u in data['users']:
        if u['telegram_id'] == user.id:
            for pl in u['playlist']:
                if pl['name'] == playlist_name:
                    pl['songs'].append({'file_id': file_id})
                    _save_data(data)
                    return True
    return False
