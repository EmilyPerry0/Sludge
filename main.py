# reddit API things
import requests.auth
# tts things
from gtts import gTTS
# video editor
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
import random
from mutagen.mp3 import MP3

with open('secrets_secrets.txt', 'r') as f:
    pw = f.readline().strip()
    CLIENT_ID = f.readline().strip()
    SECRET_KEY = f.readline().strip()

# Authenticate App
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
user_agent = 'Sludge/0.0.1'
data = {
    'grant_type': 'password',
    'username': 'Background-Setting-5',
    'password': pw
}
headers = {'User-Agent': user_agent}

# Getting Token Access ID
response = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=data, headers=headers)
token_id = " "
if response.status_code == 200:
    token_id = response.json()['access_token']

# Grab a post
OAUTH_ENDPOINT = 'https://oauth.reddit.com'
params_get = {
    'limit': 1
}
headers_get = {
    'User-Agent': user_agent,
    'Authorization': 'Bearer ' + token_id
}
response2 = requests.get(OAUTH_ENDPOINT + '/r/AmItheAsshole/top/', headers=headers_get, params=params_get)
json_data = response2.json()

# setting up the TTS and saving the audio file
lang = "en"
tts_text = json_data['data']['children'][0]['data']['selftext']
speech = gTTS(text=tts_text, lang=lang, slow=False)
TTS_filename = "tts.mp3"
speech.save(TTS_filename)

# randomize which part of the background video is used
TTS_audio = MP3(TTS_filename)
TTS_audio_time = TTS_audio.info.length
video_filename = "minecraft_parkour.mp4"
full_unedited_video = VideoFileClip(video_filename)
background_video_length = full_unedited_video.duration
start_time = random.random() * (background_video_length - TTS_audio_time)

# putting the audio and video together
edited_clip = VideoFileClip(video_filename).subclip(start_time, start_time + TTS_audio_time)
audio = AudioFileClip(TTS_filename)
edited_clip = concatenate_videoclips([edited_clip])
edited_clip.audio = audio
final_clip_filename = "final.mp4"
edited_clip.write_videofile(final_clip_filename)
