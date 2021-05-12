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
