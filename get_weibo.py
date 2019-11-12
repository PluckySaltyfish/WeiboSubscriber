# -*- coding:utf-8 -*-

import requests
import pics_saver
import send_mail
import re
import config
import os

uid = config.uid
user_name = config.user_name
containerid = config.containerid
url = 'https://m.weibo.cn/api/container/getIndex?uid=' + uid + \
      '&luicode=10000011&lfid=100103type%3D1%26q%3D' + user_name + \
      '&type=uid&value=' + uid + \
      '&containerid=' + containerid

from_addr = config.from_addr
to_addr = config.to_addr
password = config.password
from_name = config.from_name
to_name = config.to_name
subject = config.subject


class Card():
    def __init__(self, json):
        self.time = json['created_at']
        self.id = json['id']
        self.isLong = json['isLongText']
        self.text = json['text']
        self.pics = 0
        self.rpics = 0
        self.isRetweet = 0
        self.video = 0
        if 'page_info' in json.keys():
            if 'media_info' in json['page_info'].keys():
                self.video = 1
                self.video_url = json['page_info']['media_info']['mp4_sd_url']
                self.video_name = json['page_info']['media_info']['name']
        if 'pics' in json.keys():
            self.pics = json['pics']
        if 'retweeted_status' in json.keys():
            self.isRetweet = 1
            self.rname = json['retweeted_status']['user']['screen_name']
            self.rtxt = self.rname + ':' + json['retweeted_status']['text']
            self.risLong = json['retweeted_status']['isLongText']
            self.rpics = 0
            self.rvideo = 0
            if 'pics' in json['retweeted_status'].keys():
                self.rpics = json['retweeted_status']['pics']
            if 'page_info' in json['retweeted_status'].keys():
                if 'media_info' in json['retweeted_status']['page_info'].keys():
                    self.rvideo = 1
                    self.rvideo_url = json['retweeted_status']['page_info']['media_info']['mp4_sd_url']
                    self.rvideo_name = json['retweeted_status']['page_info']['media_info']['name']

        if self.isLong == True:
            rep = requests.get('https://m.weibo.cn/statuses/extend?id=' + self.id)
            self.text = rep.json()['data']['longTextContent']

    def download_pics(self):
        pic_names = []
        if self.pics != 0:
            for i in self.pics:
                pics_saver.save_pic(i['url'], i['pid'])
                pic_names.append(i['pid'] + '.jpg')
        if self.rpics != 0:
            for i in self.rpics:
                pics_saver.save_pic(i['url'], i['pid'])
                pic_names.append(i['pid'] + '.jpg')
        return pic_names


def get_cards(response):
    cards = []
    for i in response['data']['cards']:
        if i['card_type'] == 9:
            if 'title' in i['mblog'].keys() and i['mblog']['title']['text'] == '置顶':
                continue
            c = Card(i['mblog'])
            cards.append(c)
    return cards


def refine_card_text(card):
    card.text = '<p>' + card.time + '</p>' + card.text
    if card.video == 1:
        card.text += '<br><a href = "' + card.video_url + '">点击观看视频</a><br>'
    if card.isRetweet == 1:
        card.text += '<p>--------转发内容--------</p>'
        card.text += card.rtxt
        if card.rvideo == 1:
            card.text += '<br><a href = "' + card.rvideo_url + '">点击观看视频</a><br>'
    card.text = re.sub(r'<br />\s*<br />', '<br /> <br />', card.text)
    return card


def check_update():
    res = []
    with open('last_id', 'r') as f:
        last_id = str(f.readline())

    r = requests.get(url)
    cards = get_cards(r.json())

    with open('last_id','w') as f:
        f.write(cards[0].id)

    # first use
    if last_id == '0':
        return [cards[0]]

    flag = 0
    cnt = 1
    while True:
        for i in cards:
            if i.id > last_id:
                res.append(i)
            else:
                flag = 1
                break
        if flag == 1:
            break
        cnt += 1
        next_url = url + '&page=' + str(cnt)
        r = requests.get(next_url)
        cards = get_cards(r.json())

    return res

def delete_pics():
    path = 'pics/'
    ls = os.listdir(path)
    for i in ls:
        f_path = os.path.join(path, i)
        os.remove(f_path)


def send():
    cards = check_update()
    mail_sender = send_mail.MailSender(from_addr, to_addr, password, from_name, to_name, subject)
    if len(cards) == 0:
        mail_txt = user_name + '没有发微博'
        mail_sender.add_text(mail_txt)
    else:
        for card in cards:
            card = refine_card_text(card)
            pic_names = card.download_pics()
            mail_sender.add_text(card.text)
            mail_sender.add_pics(pic_names)
    mail_sender.send()
    delete_pics()


if __name__ == '__main__':
    delete_pics()
