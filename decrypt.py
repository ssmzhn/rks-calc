import base64

import pyDes

key = b'P\0G\0R\0S\0'
iv = key


def parse(s: str) -> str:
    return s.replace("%2B", "+").replace("%3D", "=").replace("%2F", "/")


def replace(s):
    des = pyDes.des(key=key, mode=pyDes.CBC, IV=iv)
    bs = parse(s)
    s = base64.b64decode(bs)
    result: bytes = des.decrypt(s)
    return result.decode("utf-16")


#if __name__ == '__main__':
#    replace()
