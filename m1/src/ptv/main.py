import sys
import time

import numpy as np
import cv2

import post
import pre
import ptv

from utils.line import send_message_to_line as line


if __name__ == '__main__':
    print("Hello!")

    p_start = time.time()

    # input argument
    argv = sys.argv

    in_dir = argv[1]         # str: input directory
    out_dir = argv[2]        # str: output directory
    f_n = argv[3]            # str: filename
    method = int(argv[4])    # int: ptv method: 3 or 4 (tracking)
    start = int(argv[5])     # int: start image index
    end = int(argv[6])       # int: end image index
    step = int(argv[7])      # int: step (interval)

    print("Params: ")
    print(f"\tin_dir: {in_dir}")
    print(f"\tout_dir: {out_dir}")
    print(f"\tf_n: {f_n}")
    print(f"\tmethod: {method}")
    print(f"\tstart: {start}")
    print(f"\tend: {end}")
    print(f"\tstep: {step}")

    # option: px/# to mm/s
    if len(argv) > 8:
        diff = int(argv[8])  # int: difference between p1 and p2
        x1 = int(argv[9])    # int: coordinate x of p1
        y1 = int(argv[10])   # int: coordinate y of p1
        x2 = int(argv[11])   # int: coordinate x of p2
        y2 = int(argv[12])   # int: coordinate y of p2
        fps = int(argv[13])  # int: fps

        print(f"\tdiff: {diff}")
        print(f"\tx1: {x1}")
        print(f"\ty1: {y1}")
        print(f"\tx2: {x2}")
        print(f"\ty2: {y2}")
        print(f"\tfps: {fps}")

    # pre-process
    print("pre-process start!")

    # calibration and make background img
    mtx = np.loadtxt("./cali/mtx.csv", delimiter=',', dtype=np.float32)
    dist = np.loadtxt("./cali/dist.csv", delimiter=',', dtype=np.float32)
    bg_img = None

    for i in range(start, end, step):
        f_n_tmp = f_n + f"{i:08}.bmp"
        tmp_img = cv2.imread(in_dir + "/" + f_n_tmp, 0)
        tmp_img = cv2.undistort(tmp_img, mtx, dist, None)
        if i == 0:
            bg_img = tmp_img
        else:
            bg_img = np.minimum(bg_img, tmp_img)
    cv2.imwrite(out_dir + "/img/" + "bg_img.bmp", bg_img)

    print("background img fin.")

    for i in range(start, end, step):
        f_n_tmp = f_n + f"{i:08}.bmp"
        pre_process = pre.Pre(in_dir=in_dir, out_dir=out_dir, filename=f_n_tmp, bg_img=bg_img, process=True)

    print("pre-process fin.")

    # ptv process
    print("ptv start!")

    ptv_process = ptv.PTV()

    print("ptv fin.")

    # post-process
    print("post-process start!")

    post_process = post.Post()

    print("post-process fin.")

    # send message to line
    elapsed_time = time.time() - p_start
    line(message=f"\nProgram fin.\nTime: {elapsed_time/1000:.1f} [sec]")

    print("Bye!!")
