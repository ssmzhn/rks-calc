import unpack  # 解包 .ab 和 .tar
import replace # 解码存档
import calc    # 计算 rks
import phicture
import os
import sys
def pause():
    if os.name == 'nt':
        os.system('pause')
def adb_extract(filename):
    print('请事先安装 ADB 工具并添加至环境变量。若已安装，则继续。')
    pause()
    if os.system('adb version') != 0:
        return -1
    print('请连接手机，并进入开发者选项打开 USB 调试。解锁手机，若手机上弹出“是否使用这台计算机进行调试”的弹框，请确认。若 Linux 系统提示输入密码，请输入。')
    pause()
    if os.name == 'posix':
        os.system('sudo adb start-server')
    else:
        os.system('adb start-server')
    os.system('adb devices')
    print('准备备份。请解锁手机，当手机上有确认备份文件的页面弹出时，选择“备份所有文件”。注意：不要输入密码！！！')
    pause()
    if os.system('adb backup -f {} com.PigeonGames.Phigros'.format(filename)) != 0:
        return -2
    return filename

def main(file):
    data_dir = unpack.unpack(file)
    if data_dir == False:
        sys.exit(-3)
    xml_file = "{data_dir}{separate}apps{separate}com.PigeonGames.Phigros{separate}sp{separate}com.PigeonGames.Phigros.v2.playerprefs.xml".format(data_dir=data_dir,separate=unpack.separate)
    if not os.path.exists(xml_file):
        print('未找到存档文件 {}，请确认您提供的 .ab 文件是否有效。'.format(xml_file))
        sys.exit(-3)
    score = replace.get_score(score_source_file=xml_file)
    info = calc.get_phigros_info(score_list=score)
    print('Ranking Score: {}'.format(info['rks']))
    phi=info['phi']
    print('Best Phi: {} {} Lv.{} {}'.format(phi['song'],phi['level'],phi['difficulty'],phi['score']))
    print('          ACC: {} 单曲RKS: {}'.format(phi['acc'],phi['rks']))
    print('----Best 19----')
    i=0
    for x in info['b19']:
        print('({}) {} {} Lv.{} {}'.format(i+1,x['song'],x['level'],x['difficulty'],x['score']))
        print('     ACC: {} 单曲RKS: {}'.format(x['acc'],x['rks']))
        i+=1
    choice = None
    while True:
        choice = input('是否使用 Phicture 保存成图片 (y/n): ')
        if choice in ('y','n'):
            break
        print('输入有误，请重新输入。')
    if choice == 'y':
        path = input('请输入保存路径: (绝对路径，包含文件名): ')
        phicture.phicture(score,path)
if __name__ == '__main__':
    print('欢迎使用 rks 计算器! ')
    print('    (1) 已有 *.ab 备份文件，直接计算')
    print('    (2) 没有 *.ab 备份文件，备份后计算')
    choice = 0
    while True:
        choice = input('请选择 ( 1 或 2 ): ')
        if choice in ('1','2'):
            break
        print('输入有误，请重新输入。')
    if choice == '1':
        main(input('请输入 adb 备份后的 .ab 文件绝对路径: '))
    elif choice == '2':
        file = input('请输入存档的保存位置 (绝对路径，包括文件名，扩展名为 .ab): ')
        adb_code = adb_extract(file)
        if adb_code==-1:
            print('未找到 ADB 程序! 请下载 ADB 软件包并配置环境变量。')
            sys.exit(-1)
        elif adb_code==-2:
            print('提取错误! 可能有下列原因: ')
            print('    1. 未安装 Phigros;')
            print('    2. 驱动未安装、手机未连接或未打开 USB 调试;')
            print('    3. 无法写入文件，可能是因为保存位置的上级目录不存在、保存位置已存在文件或目录（若您填写成一个目录，请在最后加上文件名）。如果您确信您填写的文件确实存在，可能是因为没有扩展名。请手动在文件名后添加“.ab”，再次尝试;')
            print('    4. 未正确打开 ADB 服务，这可能是没有用管理员或 root 打开 adb;')
            print('    5. 其他杂七杂八的问题。')
            sys.exit(-2)
        else:
            main(file)


