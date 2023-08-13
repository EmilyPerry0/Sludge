from gtts import gTTS

lang = "en"
text = "Hello world!"

speech = gTTS(text=text, lang=lang, slow=False)
speech.save("test_tts.mp3")
