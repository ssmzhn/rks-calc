import unpack  # 解包 .ab 和 .tar
import replace # 解码存档
import calc    # 计算 rks
import phicture
import os
import sys
from getch import getch
def pause():
    if os.name == 'nt':
        os.system('pause')
    else:
        print('请按任意键继续. . .')
        getch()
def adb_extract(filename):
    print('请事先安装 ADB 工具并添加至环境变量。若已安装，则继续。')
    pause()
    if os.system('adb version') != 0:
        return -1
    print('请连接手机，并进入开发者选项打开 USB 调试（部分手机 (如 vivo) 还需将下方的“选择 USB 配置”改成“MIDI”）。解锁手机，若手机上弹出“是否使用这台计算机进行调试”的弹框，请确认。若 Linux 系统提示输入密码，请输入。')
    pause()
    os.system('adb kill-server')
    if os.name == 'posix':
        os.system('sudo adb start-server')
    else:
        os.system('adb start-server')
    os.system('adb devices')
    print('准备备份。请解锁手机，如果您将 Phigros 放入类似“隐藏应用”中，请将其移出。现在打开 Phigros 进行下一步。')
    pause()
    print('当手机上有确认备份文件的页面弹出时，选择“备份所有文件”。')
    if os.system('adb backup -f {} com.PigeonGames.Phigros'.format(filename)) != 0:
        return -2
    return filename

def main(file,pswd):
    data_dir = unpack.unpack(file,pswd)
    if data_dir == False:
        sys.exit(-3)
    xml_file = "{data_dir}{separate}apps{separate}com.PigeonGames.Phigros{separate}sp{separate}com.PigeonGames.Phigros.v2.playerprefs.xml".format(data_dir=data_dir,separate=unpack.separate)
    if not os.path.exists(xml_file):
        print('未找到存档文件 {}，请确认您提供的 .ab 文件是否有效。（如果您备份时没有打开 Phigros 且没有将 Phigros 放在后台，请打开 Phigros 再次进行备份）'.format(xml_file))
        sys.exit(-3)
    score = replace.get_score(score_source_file=xml_file)
    info = calc.get_phigros_info(score_list=score)
    print('Ranking Score: {}'.format(info['rks']))
    phi=info['phi']
    if phi == None:
        print('没有 Phi 哦，多练！')
    else:
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
        choice = input('是否保存成图片 (y/n): ')
        if choice in ('y','n'):
            break
        print('输入有误，请重新输入。')
    if choice == 'y':
        path = input('请输入保存路径: (绝对路径，包含文件名): ')
        phicture.phicture(score,path)
if __name__ == '__main__':
    print('欢迎使用 Phicture! Coded by NameSetter (ssmzhn)')
    print('    (1) 已有 *.ab 备份文件，直接计算')
    print('    (2) 没有 *.ab 备份文件，备份后计算')
    choice = 0
    while True:
        choice = input('请选择 ( 1 或 2 ): ')
        if choice in ('1','2'):
            break
        print('输入有误，请重新输入。')
    if choice == '1':
        backupname = input('请输入 adb 备份后的 .ab 文件绝对路径: ')
        backuppassword = input('请输入存档密码 (无密码就直接按回车继续): ')
        main(backupname,backuppassword)
    elif choice == '2':
        file = input('请输入存档的保存位置 (绝对路径，包括文件名，扩展名为 .ab): ')
        adb_code = adb_extract(file)
        if adb_code==-1:
            print('未找到 ADB 程序! 请下载 ADB 软件包并配置环境变量。')
            if os.name=='nt':
                print('请使用下面的步骤配置 ADB: ')
                print('    (1) 下载 https://dl.google.com/android/repository/platform-tools-latest-windows.zip ')
                print('    (2) 解压该文件，解压出来的文件夹中应该有一个 platform-tools 文件夹。把这个 platform-tools 文件夹的绝对路径记好，后面要用;')
                print('    (3) 右键此电脑（或这台电脑、计算机、我的电脑等等），选择属性，单击左侧的高级系统设置，在弹出来的选项卡中选择“高级”，再单击环境变量;')
                print('    (4) 在“xx的用户变量”中选择“Path”，单击它，再单击“xx的用户变量”下方的编辑;')
                print('    (5) 在“编辑环境变量”对话框中点击“新建”，然后输入刚刚第二步得到的 platform-tools 文件夹绝对路径。点击确定配置成功，有可能需要重启生效;')
                print('        例如：假设第 2 步解压出来的文件夹是 D:\\adb_tools，该文件夹里有一个 platform-tools 文件夹，此时就应该填入 D:\\adb_tools\\platform-tools ')
            pause()
            sys.exit(-1)
        elif adb_code==-2:
            print('提取错误! 可能有下列原因: ')
            print('    1. 未安装 Phigros 或 Phigros 被隐藏;')
            print('    2. 驱动未安装、手机未连接或未打开 USB 调试;')
            print('    3. 无法写入文件，可能是因为保存位置的上级目录不存在、保存位置已存在文件或目录（若您填写成一个目录，请在最后加上文件名）。如果您确信您填写的文件确实存在，可能是因为没有扩展名。请手动在文件名后添加“.ab”，再次尝试;')
            print('    4. 未正确打开 ADB 服务，这可能是没有用管理员或 root 打开 adb;')
            print('    5. 其他杂七杂八的问题。')
            sys.exit(-2)
        else:
            main(file)


