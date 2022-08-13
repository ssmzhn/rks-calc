import decrypt
import json
import re
from copy import deepcopy
def rplc(s):
    return s.replace('ࠈ','').replace('؆','').replace('Ȃ','').replace('Є','')
from bs4 import BeautifulSoup as bs
def get_score(score_source_file):
    f=open(score_source_file,encoding='utf8')
    d={}
    s=f.read()
    xml=bs(s,'lxml-xml')
    for x in xml.map.findAll('string'):
        # print("a="+x.attrs['name'])
        try:
            a=rplc(decrypt.replace(x.attrs['name']))
        except ValueError:
            a=decrypt.parse(x.attrs['name'])
        # print("b="+x.string)
        try:
            b=rplc(decrypt.replace(x.string))
        except ValueError:
            b=decrypt.parse(x.string)
        d[a]=b
    score_dict={}
    for x in d:
        if re.search('^{.*}$',d[x]) != None:
            score_dict[x]=d[x]
    #f=open('score.json','w')
    score_dict_2 = deepcopy(score_dict)
    for x in score_dict:
        score_dict_2[x]=json.loads(score_dict[x])
    """
    s=json.dumps(score_dict_2,indent=4,ensure_ascii=False)
    f.write(s)
    f.close()
    """
    return score_dict_2
