import sys

import numpy as np
from PIL import Image

import line


def input_info():
    global dir_path
    global file_name
    global s
    global e

    print("DIRECTORY PATH: ")
    dir_path = input()
    if dir_path == "":
        print("Please input directory")
        return False

    print("FILE NAME: ")
    file_name = input()
    if file_name == "":
        print("Please input file name")
        return False

    print("FROM: ")
    s = int(input())
    print("TO: ")
    e = int(input())

    print("\n=======================\n")
    print("Are you okay with this?")
    print(f"\tDIR PATH: {dir_path}\n"
          f"\tFILE NAME: {file_name}\n"
          f"\tFROM: {s}, TO: {e}")
    print("\n=======================\n")

    print("Input Y/N [default: Y]")
    confirm = input()
    if confirm == "N" or confirm == "n" or confirm == "NO" or confirm == "no":
        print("Please start again")
        return False

    return True


if __name__ == '__main__':
    dir_path = ""
    file_name = ""
    s = 0
    e = 0

    if not input_info():
        sys.exit()

    for i in range(s, e):
        file_path = file_name + f"{i:08}"
        img = np.array(Image.open(dir_path + "/" + file_path + ".bmp").convert('L'))
        np.savetxt(dir_path + "/" + file_path + ".csv", img, delimiter=',', fmt='%d')

    print("fin.")
    line.send_message_to_line("program fin.")
