from PIL import Image, ImageDraw, ImageFont,ImageOps

strip_width, strip_height = 200, 200


img = Image.new('L', (200, 200), color= 'white')

fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 80)
d = ImageDraw.Draw(img)
text = "ž"
text_width, text_height = d.textsize(text,fnt)
position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
d.text(position,text, font=fnt, fill=(0,0,0))

img.save('/Users/user/Desktop/images/image.png')
