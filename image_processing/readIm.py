from PIL import Image

im = Image.open('/Users/taronegeorage/Desktop/111.jpg')
#change into gray scale
im_gray = im.convert('L')
