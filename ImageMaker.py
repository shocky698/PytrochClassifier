from PIL import Image, ImageDraw, ImageFont,ImageOps

strip_width, strip_height = 200, 200

def getImageFromLetterCombinations(letterComb):
    img = Image.new('RGB', (200, 200), color= 'white')

    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 80)
    d = ImageDraw.Draw(img)
    #text = "ž"
    text_width, text_height = d.textsize(letterComb,fnt)
    position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
    d.text(position,letterComb, font=fnt, fill=(0,0,0))

    return img

if __name__ == "__main__":
    img = getImageFromLetterCombinations("ž")
    img.save('/Users/user/Desktop/images/image.png')
