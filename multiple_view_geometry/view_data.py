#import camera
import numpy as np
from PIL import Image
import pygame.camera
import pygame

# load images
im1 = np.array(Image.open('images/001.jpg'))
im2 = np.array(Image.open('images/002.jpg'))

# load 2D points
points2D = [np.loadtxt('2D/00'+str(i+1)+'.corners').T for i in range(3)]

# load 3D points
points3D = np.loadtxt('3D/p3d').T

# load correspondence
corr = np.genfromtxt('2D/nview-corners', dtype='int', missing_values='*')

# load cameras
pygame.init()
pygame.camera.init()
P = [pygame.camera.Camera(np.loadtxt('2D/00'+str(i+1)+'.P')) for i in range(3)]
# print(np.loadtxt('2D/001.P')[0])
#camera.Camera(a)
# pygame.camera.Camera(np.loadtxt('2D/001.P')[0])