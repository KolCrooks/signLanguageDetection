from PIL import Image


background = Image.open("C:/Users/Sean McHale/Pictures/Camera Roll/one.jpg")
overlay = Image.open("C:/Users/Sean McHale/Pictures/Camera Roll/two.jpg")

background = background.convert("RGBA")
overlay = overlay.convert("RGBA")

new_img = Image.blend(background, overlay, .5)
new_img.save("new.png", "PNG")
