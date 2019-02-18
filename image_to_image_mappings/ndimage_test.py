
from scipy import ndimage
import numpy as np
from PIL import Image
from pylab import figure, gray, imshow, show
import homography

def examples():
    """This file apply a n affine transformation matrix on image patches"""

    im = np.array(Image.open('/Users/taronegeorage/Desktop/information richness.png').convert('L'))
    H = np.array([[1.4,0.05,-100],[0.05,1.5,-100],[0,0,1]])
    im2 = ndimage.affine_transform(im,H[:2,:2],(H[0,2],H[1,2]))
    figure()
    gray()
    imshow(im2)
    show()




