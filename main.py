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

# all the functions
import sludge_functions as sludge


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
    TOKEN_ID = sludge.app_auth(CLIENT_ID, SECRET_KEY, pw, USER_AGENT)
except ValueError as err:
    print(err.args)
    exit(1)

# if we're here then it was an auth success! Let's tell the user.
print('Authentication Successful!')

# Grab a post
json_data = sludge.grab_post(SUBREDDIT, USER_AGENT, TOKEN_ID)

# if we're here, then post grabbing was successful! Let's tell the user.
print('Post successfully grabbed from r/' + SUBREDDIT + '!')

# setting up the TTS and saving the audio file
# create_full_tts_audio(TTS_FILENAME, json_data)

# split the post text into sections of four words
word_list = sludge.split_post_text(json_data, 4)
# testing the function
for x in word_list:
    print(x)

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
