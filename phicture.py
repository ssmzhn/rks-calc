from PIL import Image
from PIL import ImageDraw, ImageFont, ImageEnhance
import requests
import calc
import io
import os,sys
def phicture(score,output):
    rks_box = (3329,158,3329+739,158+204)
    info=calc.get_phigros_info(score) # replace.py返回的东西
    songs = info['b19']
    for x in range(19-len(songs)):
        songs.append(None)
    songs.insert(0,info['phi'])
    background = Image.open(os.path.join(calc.res_path,'phi_blur.png'))
    draw = ImageDraw.Draw(background)
    title_font = ImageFont.truetype(os.path.join(calc.res_path,'font.ttf'),size = 240)
    draw.text((130,130),'Phicture',fill=(255,255,255),font=title_font)
    level_font = ImageFont.truetype(os.path.join(calc.res_path,'font.ttf'),size = 28)
    song_font = ImageFont.truetype(os.path.join(calc.res_path,'font.ttf'),size = 50)
    composer_font = ImageFont.truetype(os.path.join(calc.res_path,'font.ttf'),size = 30)
    rks_font = ImageFont.truetype(os.path.join(calc.res_path,'font.ttf'),size = 70)
    rks_reg = ImageEnhance.Brightness(background.crop(rks_box)).enhance(0.5)
    background.paste(rks_reg,rks_box)
    
    draw.text((3329+100,158+70),'Total RKS: {:.3f}'.format(info['rks']),fill=(255,255,255),font=rks_font)
    phi_pic = Image.open(os.path.join(calc.res_path,'phi15phi.png'))
    v_pic = Image.open(os.path.join(calc.res_path,'V15V.png')).convert('RGBA')
    s_pic = Image.open(os.path.join(calc.res_path,'S15S.png')).convert('RGBA')
    a_pic = Image.open(os.path.join(calc.res_path,'A15A.png')).convert('RGBA')
    b_pic = Image.open(os.path.join(calc.res_path,'B15B.png')).convert('RGBA')
    c_pic = Image.open(os.path.join(calc.res_path,'C15C.png')).convert('RGBA')
    f_pic = Image.open(os.path.join(calc.res_path,'F15F.png')).convert('RGBA')
    fc_pic = Image.open(os.path.join(calc.res_path,'V15FC.png')).convert('RGBA')
    width = 512*4
    height = 170
    offset = 230*2
    blank = 10*2
    for x in range(2):
        for y in range(10):
            times = x*10+y
            box = (x*width+blank,y*height+offset+blank,(x+1)*width-blank,(y+1)*height+offset-blank)
            info_box = (x*width+blank+int((height-2*blank)/9*16), y*height+offset+blank)
            region = background.crop(box)
            brt=ImageEnhance.Brightness(region)
            region=brt.enhance(0.5)
            background.paste(region,box)
            queue_pic=None
            if songs[times]!=None:
                illu = None
                try:
                    illu = Image.open(io.BytesIO(requests.get(songs[times]['illustration']).content))
                except:
                    print('下载曲绘时出错！请检查网络。')
                    sys.exit(-4)
                    
                illu_resize = illu.resize(size=(int((height-2*blank)/9*16),height-2*blank))
                background.paste(illu_resize,box=(x*width+blank, y*height+offset+blank))
    
                level = songs[times]['level']
                level_pic=None
                if level == 'EZ':
                    level_pic = Image.new('RGB',(40,40),(82,180,69))
                elif level == 'HD':
                    level_pic = Image.new('RGB',(40,40),(52,117,181))
                elif level == 'IN':
                    level_pic = Image.new('RGB',(40,40),(184,46,36))
                elif level == 'AT':
                    level_pic = Image.new('RGB',(40,40),(56,56,56))
                else:
                    level_pic = Image.new('RGB',(40,40),(0,0,0))
                background.paste(level_pic,box=(x*width+blank+int((height-2*blank)/9*16)-40, y*height+offset+blank+height-2*blank-40))
                draw.text((x*width+blank+int((height-2*blank)/9*16)-40+4, y*height+offset+blank+height-2*blank-40+4),level,fill=(255,255,255),font=level_font)
                # raise ValueError

                song_name = songs[times]['song']
                draw.text((info_box[0]+20+height-2*blank,info_box[1]+15),song_name,fill=(255,255,255),font=song_font)
                composer = songs[times]['composer']
                draw.text((info_box[0]+20+height-2*blank,info_box[1]+80),composer,fill=(255,255,255),font=composer_font)

                score = songs[times]['score']
                rank = ""
                if score == 1000000:
                    rank = phi_pic
                elif songs[times]['is_full_combo']:
                    rank = fc_pic
                elif score >=960000:
                    rank=v_pic
                elif score >= 920000:
                    rank = s_pic
                elif score >=880000:
                    rank = a_pic
                elif score >= 820000:
                    rank = b_pic
                elif score >= 700000:
                    rank = c_pic
                else:
                    rank=f_pic
                background.paste(rank.resize(size=(height-2*blank,height-2*blank)),box=info_box,mask=rank.resize(size=(height-2*blank,height-2*blank)))
                draw.text(((x+1)*width-blank-250,y*height+offset+blank+15),str(songs[times]['score']),fill=(255,255,255),font=song_font)
                draw.text(((x+1)*width-blank-440,y*height+offset+blank+80),'ACC: {:.3f}'.format(songs[times]['acc'])+'%     RKS: {:.3f}'.format(songs[times]['rks']),fill=(255,255,255),font=composer_font)
            else:
                draw.text((info_box[0]+20+height-2*blank,info_box[1]+15),'虚位以待',fill=(255,255,255),font=song_font)
            queue_pic=None
            queue = None
            if times==0:
                queue_pic = Image.new('RGB',(120,40),'red')
                queue = 'Best Phi'
            else:
                queue_pic = Image.new('RGB',(40,40),'red')
                queue = str(times)
            background.paste(queue_pic,box=(x*width+blank, y*height+offset+blank))
            draw.text((x*width+blank+4, y*height+offset+blank+4),queue,fill=(255,255,255),font=level_font)
    #background.show()
    outputpng=None
    if os.path.split(output)[-1].split('.')[-1]!='png':
        outputpng = output+'.png'
    else:
        outputpng = output
    try:
        background.save(outputpng)
    except:
        print('图片无法写入 {} 。'.format(outputpng))
