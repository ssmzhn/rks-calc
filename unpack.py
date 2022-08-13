import os
import tarfile
filedir=os.getcwd()
separate=""
if os.name=="nt":
    separate = "\\"
else:
    separate = "/"
def unpack(filename):
    filedir = os.path.split(filename)[0]
    unpacked_name='.'.join(filename.split(separate)[-1].split('.')[:-1])
    print('java -jar abe.jar unpack {} {}'.format(filename,filedir+separate+unpacked_name+'.tar'))
    os.system('java -jar abe.jar unpack {} {}'.format(filename,filedir+separate+unpacked_name+'.tar'))
    os.system('mkdir '+filedir+separate+unpacked_name)
    file = tarfile.open(filedir+separate+unpacked_name+'.tar')
    file.extractall(path=filedir+separate+unpacked_name)
    return filedir+separate+unpacked_name
