from struct import *
import binascii
import os
import shutil
import json

import pck_crypt
import pck_struct
import yappy

def print_hex(binary):
    print(*["{:02X}".format(x) for x in binary])

def save_file(content, dir, name):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(os.path.join(dir, name), "wb") as file:
        file.write(content)
    return os.path.join(dir, name).replace("\\", "/")


def unpack_pck(path, lang=None):
    with open(path, "rb") as file:
        file.seek(0, 0)
        head = binascii.hexlify(file.read(8)).decode("utf-8")
        count = unpack('i', file.read(4))[0]
        pck = pck_struct.Pck(path, head, count, lang)

        print("Found {:d} files | {}".format(count, head.upper()))
        for i in range(count):
            hash = binascii.hexlify(file.read(8)).decode("utf-8")
            flag = unpack('b', file.read(1))[0]
            offset = unpack('i', file.read(4))[0]
            size_p = unpack('i', file.read(4))[0]
            size = unpack('i', file.read(4))[0]
            noidea = binascii.hexlify(file.read(4)).decode("utf-8")

            start = file.tell()

            file.seek(offset)
            ext = binascii.hexlify(file.read(4)).decode("utf-8")
            file.seek(-4, 1)

            print("File {:2d}/{:d}: [{:016X} | {:6d} bytes or {:6d}] {} {:02d} {}".format(i+1, count, offset, size, size_p, hash.upper(), flag, noidea))
            file_bytes = file.read(size)

            if flag == 1:
                file_path = save_file(yappy.yappy_uncompress(file_bytes, size), path[:path.rfind(".")], "{:08d}".format(i))
            elif flag == 2:
                file_path = save_file(pck_crypt.decrypt(file_bytes), path[:path.rfind(".")], "{:08d}".format(i))
            elif flag == 3:
                file_path = save_file(yappy.yappy_uncompress(pck_crypt.decrypt(file_bytes), size), path[:path.rfind(".")], "{:08d}".format(i))
            else:
                file_path = save_file(file_bytes, path[:path.rfind(".")], "{:08d}".format(i))

            pck.add_file(file_path, hash, flag, ext)
            file.seek(start, 0)
        print()
        pck.write_header()

        return pck

def pack_pck(pck):
    packed = b""

    # make header
    offset = 8 + 4 + pck.count*(8 + 1 + 4 + 4 + 8)
    packed += binascii.unhexlify(pck.head)
    packed += pack('i', pck.count)
    for file in pck.get_files():
        packed += binascii.unhexlify(file.hash)
        packed += pack('b', 00)
        packed += pack('i', offset)
        file_size = os.path.getsize(file.path)
        packed += pack('i', file_size)
        packed += pack('q', file_size)
        offset += file_size

    # add files
    for file in pck.get_files():
        packed += file.read_bin()

    return packed

def merge_pck(kr_file, en_file, fl_file):
    kr_pck = unpack_pck(kr_file, "kr")
    en_pck = unpack_pck(en_file, "en")
    fl_pck = pck_struct.Pck(fl_file, kr_pck.head, kr_pck.count, "fl")

    for kr in kr_pck.get_files():
        # korean files
        kr_dict = kr.to_dict()

        # english files
        en = en_pck.get_file(hash=kr.hash)
        if en:
            en_dict = en.to_dict()
            fl_dict = merge_dict(kr_dict, en_dict)
            content = form_dict(fl_dict, kr.line_type, kr.hash)
            save_file(content, fl_file[:fl_file.rfind(".")], kr.path[kr.path.rfind("/")+1:])
        else:
            shutil.copy(kr.path, fl_file[:fl_file.rfind(".")])

        # final files
        fl_path = os.path.join(fl_file[:fl_file.rfind(".")], kr.path[kr.path.rfind("/")+1:]).replace("\\", "/")
        fl_pck.add_file(fl_path, kr.hash, 00, kr.ext)

    return fl_pck


def from_header(path):
    folder = path[:path.rfind("/")]
    with open(path, "r") as file:
        _header = json.load(file)
        pck = pck_struct.Pck(folder, "50434B00CDCCCC3E", len(_header), None)
        for key in _header:
            pck.add_file(folder+"/"+key, _header[key], 00, 00)
            print(pck.get_file(hash=_header[key]))
        return pck



def form_dict(dict, line_type, comment):
    content = b"\xef\xbb\xbf"+b"\x2f\x2f"+comment.encode("utf-8")+b"\x0d\x0a"
    for key, value in dict.items():
        new_line = None
        if line_type == pck_struct.PckFile.SPACE:
            new_line = key.encode("utf-8")+b"\x09"+value.encode("utf-8")
        elif line_type == pck_struct.PckFile.EQUALS:
            new_line = "{} = \"{}\"".format(key, value).encode("utf-8")
        if new_line:
            content += new_line+b"\x0d\x0a"
    return content

def merge_dict(base, add):
    merge = base.copy()
    for key in merge:
        if key in add:
            merge[key] = add[key]
    for key in add:
        if key not in merge:
            merge[key] = add[key]
    return merge


def clean_up(*args):
    for arg in args:
        shutil.rmtree(arg[:arg.rfind(".")], True)
