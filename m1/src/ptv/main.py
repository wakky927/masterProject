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

    program = argv[0]
    in_dir = argv[1]         # str: input directory
    out_dir = argv[2]        # str: output directory
    f_n = argv[3]            # str: filename
    method = int(argv[4])    # int: ptv method: 3 or 4 (tracking)
    start = int(argv[5])     # int: start image index
    end = int(argv[6])       # int: end image index
    step = int(argv[7])      # int: step (interval)

    # option: px/# to mm/s
    if len(argv) > 8:
        diff = int(argv[8])  # int: difference between p1 and p2
        x1 = int(argv[9])    # int: coordinate x of p1
        y1 = int(argv[10])   # int: coordinate y of p1
        x2 = int(argv[11])   # int: coordinate x of p2
        y2 = int(argv[12])   # int: coordinate y of p2
        fps = int(argv[13])  # int: fps

    # pre-process
    # make background img
    bg_img = None
    for i in range(start, end, step):
        f_n_tmp = f_n + f"{i:08}.bmp"
        tmp_img = cv2.imread(in_dir + "/" + f_n_tmp)
        if i == 0:
            bg_img = tmp_img
        else:
            bg_img = np.minimum(bg_img, tmp_img)
    cv2.imwrite(out_dir + "/" + "bg_img.bmp", bg_img)

    for i in range(start, end, step):
        f_n_tmp = f_n + f"{i:08}.bmp"
        pre_process = pre.Pre(in_dir=in_dir, out_dir=out_dir, filename=f_n_tmp, bg_img=bg_img)

    # ptv process
    ptv_process = ptv.PTV()

    # post process
    post_process = post.Post()

    # send message to line
    elapsed_time = time.time() - p_start
    line(message=f"[{program}]Program fin.\nTime: {elapsed_time/1000:d} [sec]")

    print("Bye!")
