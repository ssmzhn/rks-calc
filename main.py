import unpack  # 解包 .ab 和 .tar
import replace # 解码存档
import calc    # 计算 rks
def main():
    print('欢迎使用 rks 计算器! ')
    file = input('请输入 adb 备份后的 .ab 文件绝对路径: ')
    data_dir = unpack.unpack(file)
    xml_file = "{data_dir}{separate}apps{separate}com.PigeonGames.Phigros{separate}sp{separate}com.PigeonGames.Phigros.v2.playerprefs.xml".format(data_dir=data_dir,separate=unpack.separate)
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
if __name__ == '__main__':
    main()
