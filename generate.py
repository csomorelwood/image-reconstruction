'''

USE:
generate.py IMG_SIZE NUM_OF_CIRCLES MIN_RADIUS MAX_RADIUS MIN_INTENSITY MAX_INTENSITY NUMBER_OF_IMAGES SAVE?

example:
generate.py 500 20 10 15 120 255 2 True

'''

import random
import math
import sys

import cv2
import numpy as np

SIZE = int(500)
NOC = int(50)
RADIUS = [int(10), int(35)]
INTENSITY = [int(120), int(255)]
ITER = int(1)
SAVE = bool(True)
CS = []


def overlap(c1):
	for c2 in CS:
		dist = math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
		if dist < (c1[2] + c2[2]):
			print('overlap')
			return True
	return False


for i in range(0, ITER):
	CS = []
	img = np.zeros((SIZE, SIZE, 1), np.uint8)
	while len(CS) < NOC:
		radius = random.randint(RADIUS[0], RADIUS[1])
		intensity = random.randint(INTENSITY[0], INTENSITY[1])
		centerX = random.randint(radius, SIZE - radius)
		centerY = random.randint(radius, SIZE - radius)
		if not overlap([centerX, centerY, radius]):
			CS.append([centerX, centerY, radius])
			cv2.circle(img, (centerX, centerY), radius, intensity, cv2.FILLED)
	if SAVE:
		cv2.imwrite('images/imgrocks.jpg', img)
	else:
		cv2.imshow("img " + str(i), img)
		cv2.waitKey(0)
