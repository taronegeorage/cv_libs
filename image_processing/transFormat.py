from PIL import Image
import os

filelist = ['/Users/taronegeorage/Desktop/111.jpg']

for infile in filelist:
    outfile = os.path.splitext(infile)[0] + '.jpg'
    if infile != outfile: 
        try:
            Image.open(infile).save(outfile)
        except IOError:
            print 'cannot convert', infile