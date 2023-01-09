import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('circulos.jpg',0)
cv2.imshow('Original',img)
print img.shape
#ret,img2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
plt.hist(img.ravel(),256,[0,256]); plt.show()
