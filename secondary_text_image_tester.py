from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# base clip
test_clip = VideoFileClip("basic_assets/minecraft_parkour.mp4").subclip(0, 1)

# text clip
txt_clip = TextClip("This is tester Text", fontsize=70, color='white').set_position(540, 360).set_duration(1)

# put it all together
combined = CompositeVideoClip(test_clip, txt_clip)
combined.write_videofile("secondary_tester.mp4")
