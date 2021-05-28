import os
import random

import cv2
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


random.seed(1)

mtx = np.loadtxt("./cali/mtx.csv", delimiter=',', dtype=np.float32)
dist = np.loadtxt("./cali/dist.csv", delimiter=',', dtype=np.float32)


class Pre(object):

    def __init__(self, in_dir, out_dir, filename, bg_img, process=False):
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.filename = filename
        self.bg_img = bg_img
        self.img = None
        self.pp = None

        if process:
            self.precessing(process=process)

    def precessing(self, process):
        self.read_img(filename=self.in_dir + "/" + self.filename)
        self.cali()
        self.background_sub(p=process)
        self.binary_otsu(l=0, h=255, p=process)
        self.trimming(upper_left=[25, 902], lower_right=[1279, 83])
        self.labeling()
        self.save_csv()

    def read_img(self, filename):
        self.img = cv2.imread(filename, 0)

    def cali(self):
        self.img = cv2.undistort(self.img, mtx, dist, None)

    def background_sub(self, p=False):
        self.img -= self.bg_img
        self.img = np.maximum(self.img, np.zeros_like(self.img))

        if p:
            out_dir = self.out_dir + "/img/bg_sub"
            os.makedirs(out_dir, exist_ok=True)
            cv2.imwrite(out_dir + "/" + self.filename, self.img)

    def binary_otsu(self, l=0, h=255, p=False):
        _, self.img = cv2.threshold(self.img, l, h, cv2.THRESH_OTSU)

        if p:
            out_dir = self.out_dir + "/img/binary"
            os.makedirs(out_dir, exist_ok=True)
            cv2.imwrite(out_dir + "/" + self.filename, self.img)

    def trimming(self, upper_left=None, lower_right=None):
        self.img = self.img[83:902, 25:1279]

    def labeling(self, p=False):
        ret, markers, data, center = cv2.connectedComponentsWithStats(self.img)

        if p:
            center[0, 0], center[0, 1] = np.nan, np.nan  # bg

            s = data[1:, -1]
            s = np.append(np.expand_dims(np.arange(1, ret), 1), np.expand_dims(s, 1), axis=1)
            df = pd.DataFrame(data=s, columns=['label', 'size'])
            df_replace = df[df['size'] >= 30]

            for i in range(len(df_replace)):
                label = df_replace.iloc[i, 0]
                center[label, 0], center[label, 1] = np.nan, np.nan

            self.pp = center[~np.isnan(center).any(axis=1), :]

        else:
            # visualize labeling
            out_dir = self.out_dir + "/img/label"
            os.makedirs(out_dir, exist_ok=True)

            color_src = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
            height, width = self.img.shape[:2]
            colors = []

            for i in range(1, ret + 1):
                colors.append(np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))

            for y in range(0, height):
                for x in range(0, width):
                    if markers[y, x] > 0:
                        color_src[y, x] = colors[markers[y, x]]
                    else:
                        color_src[y, x] = [0, 0, 0]

            cv2.imwrite(out_dir + "/labeled" + self.filename, color_src)

            # graph visualization
            s = data[1:, -1]
            fig = plt.figure(figsize=(6, 4))
            ax = fig.add_subplot(1, 1, 1)
            ax.hist(s, bins=100)
            ax.set_xlabel('size')
            ax.set_ylabel('freq')
            ax.set_xlim([0, np.max(data[1:, -1])])
            fig.savefig(out_dir + "/" + "hist.png", dpi=300)
            fig.show()

            # by visualization, tracer size < 30 px
            s = np.append(np.expand_dims(np.arange(1, ret), 1), np.expand_dims(s, 1), axis=1)
            df = pd.DataFrame(data=s, columns=['label', 'size'])
            df_replace = df[df['size'] >= 30]

            for i in range(len(df_replace)):
                label = df_replace.iloc[i, 0]
                markers[markers == label] = 0

            # re-visualize labeling
            color_src = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
            height, width = self.img.shape[:2]
            colors = []

            for i in range(1, ret + 1):
                colors.append(np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))

            for y in range(0, height):
                for x in range(0, width):
                    if markers[y, x] > 0:
                        color_src[y, x] = colors[markers[y, x]]
                    else:
                        color_src[y, x] = [0, 0, 0]

            cv2.imwrite(out_dir + "/clipped" + self.filename, color_src)

    def save_csv(self):
        out_dir = self.out_dir + "/csv/pp"
        os.makedirs(out_dir, exist_ok=True)
        filename = self.filename.replace('.bmp', '.csv')

        cols = ['x', 'y']
        df = pd.DataFrame(data=self.pp, columns=cols).astype('int64')
        df.to_csv(out_dir + '/' + filename)


if __name__ == '__main__':
    in_d = '../../../data/in'
    out_d = '../../../data/out'
    f_n_tmp = '_00000000.bmp'
    bg_img = cv2.imread(out_d + "/img/" + "bg_img.bmp", 0)

    pre = Pre(in_dir=in_d, out_dir=out_d, filename=f_n_tmp, bg_img=bg_img)
    pre.read_img(filename=pre.in_dir + "/" + pre.filename)
    pre.cali()
    pre.background_sub()
    pre.binary_otsu(l=0, h=255)
    pre.trimming(upper_left=[25, 902], lower_right=[1279, 83])
    pre.labeling(True)
    pre.save_csv()
