import cv2
import numpy as np

img = cv2.imread('images/imgrocksbw256.jpg', cv2.IMREAD_GRAYSCALE)
noiseNormal = np.random.normal(0, 1, img.shape)
noiseCauchy = np.random.standard_cauchy(img.shape)
noisePareto = np.random.pareto(1, img.shape)
kernel = np.ones((6, 6), np.float32)/25
blurred = cv2.filter2D(img, -1, kernel)

#cv2.imshow('Normal noise', noiseNormal)
#cv2.imshow('Binomial noise', noiseCauchy)
#cv2.imshow('Pareto noise', noisePareto)
cv2.imshow('Blurred', blurred)

cv2.imwrite('images/imgnormalnoise.jpg', noiseNormal+img)
cv2.imwrite('images/imgbinomialnoise.jpg', noiseCauchy+img)
cv2.imwrite('images/imgparetonoise.jpg', noisePareto+img)
cv2.imwrite('images/blurred.jpg', blurred)
cv2.waitKey(0)
