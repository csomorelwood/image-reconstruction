import cv2

img = cv2.imread('images/original.jpg', cv2.IMREAD_GRAYSCALE)
fbp = cv2.imread('images/reconstructed180.jpg', cv2.IMREAD_GRAYSCALE)
abserror = img - fbp
relerror = abserror % img
rme = relerror.mean()
print('RME: ', rme)

cv2.imshow('Absolute error', abserror)
cv2.imshow('Relative error', relerror)
cv2.waitKey(0)
