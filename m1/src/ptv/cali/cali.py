import cv2
import numpy as np
import pandas as pd


if __name__ == '__main__':
    img = cv2.imread("cali.bmp", 0)
    square_size = 5.0
    pattern_size = (21, 15)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points = []

    df = pd.read_csv("res.csv", dtype=np.float32)
    corner = np.expand_dims(df.drop('n', axis=1).values, 1)

    img_points.append(corner.reshape(-1, 2))
    obj_points.append(pattern_points)

    rms, K, d, r, t = cv2.calibrateCamera(obj_points, img_points, (img.shape[1], img.shape[0]), None, None)
    print("RMS = ", rms)
    print("K = \n", K)
    print("d = ", d.ravel())

    np.savetxt("mtx.csv", K, delimiter=',', fmt="%0.14f")
    np.savetxt("dist.csv", d, delimiter=',', fmt="%0.14f")

    resultImg = cv2.undistort(img, K, d, None)
    cv2.imwrite("ud.bmp", resultImg)
