import sys

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import input_info
import line


def drive_upload_image(f_path, f_type="bmp", f_id=None):
    title = f_path + "." + f_type
    m = {"title": title, "mimeType": "image/" + f_type}
    if f_id is not None:
        m["parents"] = [{"kind": "drive#fileLink", "id": f_id}]

    f = drive.CreateFile(m)
    f.SetContentFile(title)
    f.Upload()


def drive_upload_text(f_path, f_type="csv", f_id=None):
    title = f_path + "." + f_type
    m = {"title": title, "mimeType": "text/" + f_type}
    if f_id is not None:
        m["parents"] = [{"kind": "drive#fileLink", "id": f_id}]

    f = drive.CreateFile(m)
    f.SetContentFile(title)
    f.Upload()


if __name__ == '__main__':
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    drive = GoogleDrive(gauth)

    dir_path = ""
    file_name = ""
    s = 0
    e = 0

    if not input_info.input_info():
        sys.exit()

    file_id = input()

    for i in range(s, e):
        path = dir_path + "/" + file_name + f"{i:08}"
        drive_upload_image(path, "bmp", f_id=file_id)

    print("fin.")
    line.send_message_to_line("program fin.")
