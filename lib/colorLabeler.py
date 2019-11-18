import cv2
import numpy as np
from collections import OrderedDict
from scipy.spatial import distance as dist

class ColorLabeler:
	def __init__(self):
		self.colorsToIgnore = ['darkgray', 'darkblue', 'black', 'white']

		colors = OrderedDict({
			"red": (255, 0, 0),
			"green": (0, 255, 0),
			"blue": (0, 0, 255),
            "black": (0, 0, 0),
            "yellow": (255, 255, 0),
            "darkblue": (0, 0, 71),
            "gray": (96, 96, 96),
            "darkgray": (70, 70, 70),
            "white": (255, 255, 255),
			"lightblue": (135,206,250),
            })

		self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
		self.colorNames = []

		for (i, (name, rgb)) in enumerate(colors.items()):
			self.lab[i] = rgb
			self.colorNames.append(name)

		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

	def label(self, img, c):
		mask = np.zeros(img.shape[:2], dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.erode(mask, None, iterations=2)
		mean = cv2.mean(img, mask=mask)[:3]

		minDist = (np.inf, None)

		for (i, row) in enumerate(self.lab):
			d = dist.euclidean(row[0], mean)

			if d < minDist[0]:
				minDist = (d, i)

		return self.colorNames[minDist[1]]