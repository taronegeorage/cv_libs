import warp
from pylab import figure, gray, imshow, show, axis
import homography
import numpy as np
from PIL import Image
from scipy import ndimage

im1 = np.array(Image.open('cuhk.png').convert('L'))
im2 = np.array(Image.open('billboard1.jpg').convert('L'))
#tp = np.array([[938,1496,1259,601],[450,435,2845,2745],[1,1,1,1]])
tp = np.array([[31,194,205,53],[71,69,654,645],[1,1,1,1]])

def example():
    # example of affine warp of im1 onto im2
    
    # set to points
    im3 = warp.image_in_image(im1,im2,tp)
    figure()
    gray()
    imshow(im3)
    axis('equal')
    axis('off')
    show()

def affine_example():
    # set from points to corners of im1
    m,n = im1.shape[:2]
    fp = np.array([[0,m,m,0],[0,0,n,n],[1,1,1,1]])
    # first triangle
    tp2 = tp[:,:3]
    fp2 = fp[:,:3]
    # compute H
    H = homography.Haffine_from_points(tp2,fp2)
    im1_t = ndimage.affine_transform(im1,H[:2,:2],
    (H[0,2],H[1,2]),im2.shape[:2])
    # alpha for triangle
    alpha = warp.alpha_for_triangle(tp2,im2.shape[0],im2.shape[1])
    im3 = (1-alpha)*im2 + alpha*im1_t
    # second triangle
    tp2 = tp[:,[0,2,3]]
    fp2 = fp[:,[0,2,3]]
    # compute H
    H = homography.Haffine_from_points(tp2,fp2)
    im1_t = ndimage.affine_transform(im1,H[:2,:2],(H[0,2],H[1,2]),im2.shape[:2])
    # alpha for triangle
    alpha = warp.alpha_for_triangle(tp2,im2.shape[0],im2.shape[1])
    im4 = (1-alpha)*im3 + alpha*im1_t
    figure()
    gray()
    imshow(im4)
    axis('equal')
    axis('off')
    show()

affine_example()