import json
import sys,os
res_path = None
if getattr(sys, 'frozen', False): #是否Bundle Resource
    res_path = sys._MEIPASS
else:
    res_path = os.path.abspath("./res")
chart_list = json.load(open(os.path.join(res_path,'chart.json'),encoding='utf8'))
song_name_list = json.load(open(os.path.join(res_path,'song_name.json'),encoding='utf8'))
#score_list = json.load(open('score.json'))
def get_phigros_info(score_list):
    used_score = {}
    for x in score_list:
        if x.split('.')[-1] in ('EZ','HD','IN','AT') and score_list[x]!={}:
            used_score[x]=score_list[x]
            #print(used_score[x])
    used_score_2 = {}

    for x in used_score:
        song_info = chart_list[song_name_list['.'.join(x.split('.')[:2])]]
        song = song_info['song']
        illustration = song_info['illustration']
        composer = song_info['composer']
        level = x.split('.')[-1]
        score = int(used_score[x]['s'])
        acc = float(used_score[x]['a'])
        try:
            difficulty = float(song_info['chart'][level]['difficulty'])
        except:
            continue
        is_full_combo = False
        if used_score[x]['c']==1:
            is_full_combo=True
        single_rks = 0
        if acc >= 70:
            single_rks = ((acc-55)/45)**2*difficulty
        is_phi = False
        if used_score[x]['s']==1000000:
            is_phi=True
        used_score_2[x]={}
        used_score_2[x]['song']=song
        used_score_2[x]['composer']=composer
        used_score_2[x]['illustration']=illustration
        used_score_2[x]['level']=level
        used_score_2[x]['difficulty']=difficulty
        used_score_2[x]['score']=score
        used_score_2[x]['acc']=acc
        used_score_2[x]['is_full_combo']=is_full_combo
        used_score_2[x]['is_phi']=is_phi
        used_score_2[x]['rks']=single_rks
        #print(used_score_2[x])
    best19=[]
    for x in used_score_2.keys():
        if len(best19)<19:
            best19.append(used_score_2[x])
            #print(used_score_2[x])
            if used_score_2[x]=={}:
                raise ValueError
        else:
            best19=sorted(best19,key=lambda x:x['rks'])
            for y in range(len(best19)):
                if used_score_2[x]['rks']>best19[y]['rks']:
                    best19.pop(y)
                    best19.append(used_score_2[x])
                    break
    sorted_b19=sorted(best19,key=lambda x:x['rks'],reverse=True)
    philist=[]
    for x in used_score_2.keys():
        if used_score_2[x]['is_phi']:
            philist.append(used_score_2[x])
    best_phi=None
    if len(philist)!=0:
        best_phi=sorted(philist,key=lambda x:x['rks'],reverse=True)[0]
    total_rks=0
    if best_phi!=None:
        total_rks+=best_phi['rks']
    for x in range(len(sorted_b19)):
        total_rks+=sorted_b19[x]['rks']
    if best_phi==None:
        total_rks/=19
    else:
        total_rks/=20
 
    ans = {}
    ans['b19']=sorted_b19
    ans['phi']=best_phi
    ans['rks']=total_rks
    return ans
"""
    total_rks=0.0
    if best_phi!=None:
        print('Best Phi: {} {} Score: {} ACC: {} RKS: {}'.format(best_phi['song'],best_phi['level'],best_phi['score'],best_phi['acc'],best_phi['rks']))
        total_rks+=best_phi['rks']
    print('---Best 19---')
    for x in range(len(sorted_b19)):
        print('{}) {} {} Score: {} ACC: {} RKS: {}'.format(x+1,sorted_b19[x]['song'],sorted_b19[x]['level'],sorted_b19[x]['score'],sorted_b19[x]['acc'],sorted_b19[x]['rks']))
    total_rks+=sorted_b19[x]['rks']

    print(total_rks)
    if best_phi==None:
        total_rks/=19
    else:
        total_rks/=20
        
    print('Total Ranking Score: {}'.format(total_rks))
"""
