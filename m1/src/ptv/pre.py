import numpy as np
import pandas as pd
import cv2


class Pre(object):

    def __init__(self, in_dir, out_dir, filename, bg_img):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.filename = filename
        self.bg_img = bg_img
        self.img = None
        self.precessing()

    def precessing(self):
        self.read_img(filename=self.in_dir + "/" + self.filename)
        self.background_sub()
        self.binary_otsu()
        self.labeling()
        self.save_csv()

    def read_img(self, filename):
        self.img = cv2.imread(filename, 0)

    def background_sub(self):
        self.img -= self.bg_img
        self.img = np.maximum(self.img, np.zeros_like(self.img))

    def binary_otsu(self, l=0, h=255):
        _, self.img = cv2.threshold(self.img, l, h, cv2.THRESH_OTSU)

    def labeling(self):
        pass

    def save_csv(self):
        pass
