# reddit API things
import requests.auth

# tts things
from gtts import gTTS
from pydub import AudioSegment

# putting text onto an image
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# video editor
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
import random
from mutagen.mp3 import MP3


# runs the authentication processes to begin the proper interaction with the reddit API
# returns the access token granted by the authentication process (or raises an error if auth failed)
def app_auth(client_id, secret_key, user_agent):
    client_auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
    data = {
        'grant_type': 'password',
        'username': 'Background-Setting-5',
        'password': pw
    }
    headers = {'User-Agent': user_agent}

    # Getting Token Access ID
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=data,
                             headers=headers)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise ValueError('The authentication process failed')


# grabs a post from a specified subreddit
# returns the json data of the post that was grabbed
def grab_post(subreddit, user_agent, token_id):
    # getting ready for post grabbing
    oauth_endpoint = 'https://oauth.reddit.com'
    params_get = {
        'limit': 1
    }
    headers_get = {
        'User-Agent': user_agent,
        'Authorization': 'Bearer ' + token_id
    }
    # the actual post grabbing, then converting it into json format
    return requests.get(oauth_endpoint + '/r/' + subreddit + '/top/', headers=headers_get,
                        params=params_get).json()


# takes in some text and turns it into an audio file that speaks the text.
# the speech is also sped up by pydub because gTTS is insanely slow :/
def create_full_tts_audio(tts_filename, json_data):
    # making the base speech
    tts_text = json_data['data']['children'][0]['data']['selftext']
    speech = gTTS(text=tts_text, lang='en', slow=False)
    speech.save(tts_filename)

    # speeding up the base speech and re-saving it with the same name
    AudioSegment.from_mp3(tts_filename).speedup(1.35).export(tts_filename, format="mp3")


# main code
# setting up variables
USER_AGENT = 'Sludge/0.1.1'
TOKEN_ID = ''
SUBREDDIT = 'AmITheAsshole'
TTS_FILENAME = "tts.mp3"

# read in the secret info that should not be public on my GitHub :)
with open('secrets_secrets.txt', 'r') as f:
    pw = f.readline().strip()
    CLIENT_ID = f.readline().strip()
    SECRET_KEY = f.readline().strip()

# authenticate the session
try:
    TOKEN_ID = app_auth(CLIENT_ID, SECRET_KEY, USER_AGENT)
except ValueError as err:
    print(err.args)
    exit(1)

# if we're here then it was an auth success! Let's tell the user.
print('Authentication Successful!')

# Grab a post
json_data = grab_post(SUBREDDIT, USER_AGENT, TOKEN_ID)

# if we're here, then post grabbing was successful! Let's tell the user.
print('Post successfully grabbed from r/' + SUBREDDIT + '!')

# setting up the TTS and saving the audio file
create_full_tts_audio(TTS_FILENAME, json_data)

# creating the images that display the text on screen


# randomize which part of the background video is used
TTS_audio = MP3(TTS_FILENAME)
TTS_audio_time = TTS_audio.info.length
video_filename = "basic_assets/minecraft_parkour.mp4"
full_unedited_video = VideoFileClip(video_filename)
background_video_length = full_unedited_video.duration
start_time = random.random() * (background_video_length - TTS_audio_time)

# putting the audio and video together
edited_clip = VideoFileClip(video_filename).subclip(start_time, start_time + TTS_audio_time)
audio = AudioFileClip(TTS_FILENAME)
edited_clip = concatenate_videoclips([edited_clip])
edited_clip.audio = audio
final_clip_filename = "OUTPUT/final.mp4"
edited_clip.write_videofile(final_clip_filename)
