import os
import tarfile
import ab_decrypt
from calc import res_path
srcdir=os.getcwd()
separate=""
if os.name=="nt":
    separate = "\\"
else:
    separate = "/"
def unpack(filename,password: str):
    # if os.system('java --version')!=0:
    #    print('未找到 Java 主程序！请安装最新 JDK 并配置好环境变量。')
    #    return -1
    filedir = os.path.split(filename)[0]
    unpacked_name='.'.join(os.path.split(filename)[1].split('.')[:-1])
    is_ab2tar_success = True
    if password == '':
        pswd = None
    else:
        pswd = password
    if not os.path.exists(filename):
        print('未找到备份文件 ({}) ;'.format(filename))
        is_ab2tar_success = False
        return False
    try:
        is_ab2tar_success=ab_decrypt.ab2tar(open(filename,'rb'),open(os.path.join(filedir,unpacked_name+'.tar'),'wb'),password=pswd)
        if not is_ab2tar_success:
            print('传入的文件不是 .ab 备份文件或已加密但未输入密码。')
    except:
        print('解包 .ab 文件出错！')
        print('可能有以下情况: ')
        print('    (*) 无法写入 {} ，可能是因为此处有文件且被某一程序占用、此处有文件夹或权限不够;'.format(os.path.join(filedir,unpacked_name+'.tar')))
        print('    (*) 密码错误;')
        print('    (*) 其他奇奇怪怪的情况。')
        is_ab2tar_success = False
    os.system('mkdir '+os.path.join(filedir,unpacked_name))
    try:
        file = tarfile.open(os.path.join(filedir,unpacked_name+'.tar'))
        file.extractall(path=os.path.join(filedir,unpacked_name))
    except:
        print('解包 {} 时出现错误！'.format(os.path.join(filedir,unpacked_name+'.tar')))
        print('可能有以下情况: ')
        if not is_ab2tar_success:
            print('    (*) 解包 .ab 文件时出错，见上述错误信息;')
        if not os.path.exists(os.path.join(filedir,unpacked_name+'.tar')):
            print('    (*) 未找到该文件;')
        print('    (*) 无权写入;')
        return False
    return os.path.join(filedir,unpacked_name)
