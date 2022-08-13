import os
import tarfile
current_dir=os.getcwd()
separate=""
if os.name=="nt":
    separate = "\\"
else:
    separate = "/"
def unpack(filename):
    unpacked_name=filename.split(separate)[-1].split('.',1)[0]
    os.system('java -jar abe.jar unpack {} {}'.format(filename,current_dir+separate+unpacked_name+'.tar'))
    os.system('mkdir '+current_dir+separate+unpacked_name)
    file = tarfile.open(current_dir+separate+unpacked_name+'.tar')
    file.extractall(path=current_dir+separate+unpacked_name)
    return current_dir+separate+unpacked_name
