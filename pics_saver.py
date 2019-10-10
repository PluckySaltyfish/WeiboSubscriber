# -*- coding:utf-8 -*-

import requests

def download_content(url,dir):
    try:
        r = requests.get(url)
        fp = open(dir,'wb')
        fp.write(r.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print('无法下载')
    except Exception as e:
        print('存储错误 :' ,e )

def save_pic(url,name):
    download_content(url,'pics/' + name + '.jpg')




if __name__ == '__main__':
    pass
    # save_pic('https://wx1.sinaimg.cn/orj360/4cca97aaly1g6p4zsf4eoj20qo0zkjwn.jpg','4cca97aaly1g6p4zsf4eoj20qo0zkjwn')
    # save_video('https://multimedia.api.weibo.com/2/multimedia/redirect_tencent_video.json?vid=j0032italj7','4411805804496439')



