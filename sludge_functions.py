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
def app_auth(client_id, secret_key, pw, user_agent):
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


# takes the text from a reddit post and splits it up into sections of 'section_length'
# returns a list of strings, where each string (sometimes except the last one) will have 'section_length' words
# fix issue withi newline characters
def split_post_text(json_data, section_length):
    word_list = []
    temp_string = ""
    temp_word_count = 0
    post_text = json_data['data']['children'][0]['data']['selftext']
    sectioned_text = post_text.split(" ")
    for word in sectioned_text:
        # add words to the temp string until its of section_length
        temp_string += word + " "
        temp_word_count += 1
        if temp_word_count == section_length:
            # once it is of section_length, add it to the word list and reset the temp_string
            word_list.append(temp_string)
            temp_string = ""
            temp_word_count = 0
    # add the leftover stuff still in the temp_string if the words are not a multiple of section_length
    word_list.append(temp_string)
    return word_list
