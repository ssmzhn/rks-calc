import os
import tarfile
srcdir=os.getcwd()
separate=""
if os.name=="nt":
    separate = "\\"
else:
    separate = "/"
def unpack(filename):
    if os.system('java --version')!=0:
        print('未找到 Java 主程序！请安装最新 JDK 并配置好环境变量。')
        return -1
    filedir = os.path.split(filename)[0]
    unpacked_name='.'.join(os.path.split(filename)[1].split('.')[:-1])
    print('java -jar {} unpack {} {}'.format(os.path.join(srcdir,'abe.jar'),filename,os.path.join(filedir,unpacked_name+'.tar')))
    is_ab2tar_success = os.system('java -jar {} unpack {} {}'.format(os.path.join(srcdir,'abe.jar'),filename,os.path.join(filedir,unpacked_name+'.tar')))
    if is_ab2tar_success != 0:
        print('解包 .ab 文件出错！')
        print('可能有以下情况: ')
        print('    (*) JDK 版本过低，请更新至最高版本;')
        if not os.path.exists(os.path.join(srcdir,'abe.jar')):
            print('    (*) 未找到解包程序 ({})'.format(os.path.join(srcdir,'abe.jar')))
        if not os.path.exists(filename):
            print('    (*) 未找到备份文件 ({}) 或备份文件已损坏;'.format(filename))
        print('    (*) 无权写入 {} ;'.format(os.path.join(filedir,unpacked_name+'.tar')))
        print('    (*) 其他奇奇怪怪的情况。')
    os.system('mkdir '+os.path.join(filedir,unpacked_name))
    try:
        file = tarfile.open(os.path.join(filedir,unpacked_name+'.tar'))
        file.extractall(path=os.path.join(filedir,unpacked_name))
    except:
        print('解包 {} 时出现错误！'.format(os.path.join(filedir,unpacked_name+'.tar')))
        print('可能有以下情况: ')
        if is_ab2tar_success!=0:
            print('    (*) 解包 .ab 文件时出错，见上述错误信息;')
        if not os.path.exists(os.path.join(filedir,unpacked_name+'.tar')):
            print('    (*) 未找到该文件;')
        print('    (*) 无权写入;')
        return -2
    return os.path.join(filedir,unpacked_name)
