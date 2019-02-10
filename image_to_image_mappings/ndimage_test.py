
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

def image_in_image(im1,im2,tp):
    """ Put im1 in im2 with an affine transformation
    such that corners are as close to tp as possible.
    tp are homogeneous and counter-clockwise from top left. """
    
    # points to warp from
    m,n = im1.shape[:2]
    fp = np.array([[0,m,m,0],[0,0,n,n],[1,1,1,1]])
    # compute affine transform and apply
    H = homography.Haffine_from_points(tp,fp)
    im1_t = ndimage.affine_transform(im1,H[:2,:2],(H[0,2],H[1,2]),im2.shape[:2])
    alpha = (im1_t > 0)
    return (1-alpha)*im2 + alpha*im1_t


