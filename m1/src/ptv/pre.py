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

        if process:
            self.precessing(process=process)

    def precessing(self, process):
        self.read_img(filename=self.in_dir + "/" + self.filename)
        self.cali()
        self.background_sub(p=process)
        self.binary_otsu(l=0, h=255, p=process)
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

    def labeling(self, p=False):
        ret, markers, data, center = cv2.connectedComponentsWithStats(self.img)

        if not p:
            # color_src = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
            # height, width = self.img.shape[:2]
            # colors = []
            #
            # for i in range(1, ret + 1):
            #     colors.append(np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))
            #
            # for y in range(0, height):
            #     for x in range(0, width):
            #         if markers[y, x] > 0:
            #             m = markers[y, x]
            #             color_src[y, x] = colors[markers[y, x]]
            #         else:
            #             color_src[y, x] = [0, 0, 0]
            #
            # cv2.putText(color_src, str(ret - 1), (20, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))

            # graph visualization
            f = data[1:, -1]
            fig = plt.figure(figsize=(6, 4))
            ax = fig.add_subplot(1, 1, 1)
            ax.hist(f, bins=100)
            ax.set_xlabel('size')
            ax.set_ylabel('freq')
            ax.set_xlim([0, np.max(data[1:, -1])])
            # fig.show()

            # by visualization, tracer size < 30 px
            f = np.append(np.expand_dims(np.arange(1, ret), 1), np.expand_dims(f, 1), axis=1)
            df = pd.DataFrame(data=f, columns=['label', 'size'])
            df_remain = df[df['size'] < 30]
            df_replace = df[df['size'] >= 30]

            for i in range(len(df_replace)):
                label = df_replace.iloc[i, 0]
                markers[markers == label] = 0

            color_src = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
            height, width = self.img.shape[:2]
            colors = []

            for i in range(1, ret + 1):
                colors.append(np.array([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))

            for y in range(0, height):
                for x in range(0, width):
                    if markers[y, x] > 0:
                        m = markers[y, x]
                        color_src[y, x] = colors[markers[y, x]]
                    else:
                        color_src[y, x] = [0, 0, 0]

            cv2.putText(color_src, str(ret - 1), (20, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))

            cv2.imshow("color_src", color_src)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def save_csv(self):
        pass


if __name__ == '__main__':
    in_d = '/media/takuya/ボリューム/M1/original/2021_05_19/fps_200_ss_600'
    out_d = '/media/takuya/ボリューム/M1/result/2021_05_19'
    f_n_tmp = '_00000000.bmp'
    bg_img = cv2.imread(out_d + "/img/" + "bg_img.bmp", 0)

    pre = Pre(in_dir=in_d, out_dir=out_d, filename=f_n_tmp, bg_img=bg_img)
    pre.read_img(filename=pre.in_dir + "/" + pre.filename)
    pre.cali()
    pre.background_sub()
    pre.binary_otsu(l=0, h=255)
    pre.labeling()
