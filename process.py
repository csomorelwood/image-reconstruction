import imutils as imutils
from skimage.measure import compare_ssim
from skimage.transform import radon, iradon
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

T = 1.5
BINARY = True

floor = math.floor


def reverseFBP(sinogram):
	reconstruction_fbp = np.rot90(sinogram, 3)
	reconstruction_fbp = iradon(reconstruction_fbp)
	reconstruction_fbp[reconstruction_fbp < 1] = 0
	reconstruction_fbp = cv2.normalize(reconstruction_fbp, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
	if BINARY:
		reconstruction_fbp[reconstruction_fbp > 1] = 255
	return reconstruction_fbp


def FBP(img, step=1.0):
	s = radon(img, theta=np.arange(0, 180, int(step)))
	s = cv2.normalize(s, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
	s = np.rot90(s)
	return s

def simScore(i1,i2):
	(score) = compare_ssim(i1, i2, full=False)
	#diff = (diff * 255).astype("uint8")
	return (f'{score:0.5}')

img = cv2.imread('images/imgrocksbw256cut.jpg', cv2.IMREAD_GRAYSCALE)
'''
ret,thresh1 = cv2.threshold(img,10,255,cv2.THRESH_BINARY)
cv2.imwrite('images/imgrocksbw.jpg', thresh1)
cv2.imshow('fes',thresh1)
'''
canvas = np.zeros((floor(img.shape[0] * T), floor(img.shape[1] * T)), np.uint8)
nrs = floor(img.shape[0] * ((T - 1) / 2))
ncs = floor(img.shape[1] * ((T - 1) / 2))

canvas[nrs:nrs + img.shape[0], ncs:ncs + img.shape[1]] = img

sinogram = FBP(canvas)

fig, axs = plt.subplots(2, 3)
fig.canvas.set_window_title('Keprekonstrukcio')
axs[0, 0].set_title('Original')
axs[0, 0].imshow(canvas)
cv2.imwrite('images/original.jpg', canvas)
print(canvas.mean())

axs[0, 1].set_title('FBP')
axs[0, 1].set_ylim([0, 360])

fbpimg = cv2.resize(sinogram, dsize=(canvas.shape[1], 360), interpolation=cv2.INTER_CUBIC)
axs[0, 1].imshow(fbpimg)
cv2.imwrite('images/fbp.jpg', fbpimg)

recon10 = reverseFBP(FBP(canvas, 180/10))
axs[0, 2].set_title('Reconstructed 10')
axs[0, 2].imshow(recon10)
cv2.imwrite('images/reconstructed10.jpg', recon10)

recon30 = reverseFBP(FBP(canvas, 180/30))
cv2.imwrite('images/reconstructed30.jpg', recon30)

recon75 = reverseFBP(FBP(canvas, 180/75))
cv2.imwrite('images/reconstructed75.jpg', recon75)

recon120 = reverseFBP(FBP(canvas, 180/120))
cv2.imwrite('images/reconstructed120.jpg', recon120)

axs[1, 0].set_title('Reconstructed 30')
axs[1, 0].imshow(recon30)

axs[1, 1].set_title('Reconstructed 180')
rfull = reverseFBP(sinogram)
axs[1, 1].imshow(rfull)
cv2.imwrite('images/reconstructed180.jpg', rfull)

scores = []
for a in range(0,180):
	ss = simScore(reverseFBP(FBP(canvas, 180/(a+1))),canvas)
	scores.append(round(float(ss),2)*100)

print(scores)
axs[1, 2].set_title('Results')
axs[1, 2].plot(range(1,181,1),scores)
fig.tight_layout()
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.show()

cv2.waitKey(0)
