from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# set up the text list
all_text = ('hello', 'guys', 'welccome', 'to', 'a', 'a', 'new', 'video')

# filename setup
assets_root = 'basic_assets/'
base_image_filename = assets_root + "transparent square.png"

# open the font
myFont = ImageFont.truetype(assets_root + 'BRLNSDB.TTF', 50)

# add the text in a for loop for each word in the list
for word in all_text:
    # open the image
    text_img = Image.open(base_image_filename)
    curr_img = ImageDraw.Draw(text_img)
    curr_img.text((0, 0), word, font=myFont, fill=(255, 255, 255))

    # save the new image
    to_save_filename = 'TTS_text_image_files/' + word + '.png'
    text_img.save(to_save_filename)
