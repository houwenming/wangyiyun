import re
import base64
import random
import json
import string
import urllib.parse
import urllib.request
from aes import AESCipher
import csv
import os
import time
def gettimebymils(mils):
    # 使用time
    timeArray = time.localtime(mils/1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime   # 2013--10--10 23:40:11
def generate_random_str(randomlength=16):
    """
        生成一个指定长度的随机字符串，其中
        string.digits=0123456789
        string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str
def aesEncrypt(text, secKey):
    aescipher=AESCipher(secKey)
    return aescipher.encrypt(text).decode()

def downloadsong(id,path):
    try:
        songjson='{"ids":"['+id+']","level":"standard","encodeType":"aac","csrf_token":""}';
        key=generate_random_str()
        key='aScoJVPrM01yDLUf'
        g='0CoJUm6Qyw8W8jud'
        encText=aesEncrypt(songjson,g);
        encText=aesEncrypt(encText,key);
        encSecKey='31f5eea784f90a2b6670656557eb1c77bf1c2fab7f6a0b4b3fab0bbd1be9dc3da74f4ff0f0a3e75dd6c926e92af030cb5b45e0e79f71b45cfdb306eaaafaa5aefd966ca9783445adfef9181b8b078a6cae4ea7d67657315b7a8c24d012eefe5f83f4f263d845ed293f260b3d680c85c5357ec1adf654e92c085777add7a4ebd6';
        params='params='+urllib.parse.quote(encText)+'&encSecKey='+encSecKey
        #print(params)
        headers={
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://music.163.com/song?id='+id,
            'Host': 'music.163.com'
            }
        req=urllib.request.Request('https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=', data=params.encode('utf-8'), headers=headers)
        page = urllib.request.urlopen(req).read()
        page = page.decode('utf-8')
        #req = urllib.request.urlopen('https://music.163.com/weapi/v3/song/detail?csrf_token=', headers=headers, data=params)
        #print(page)
        url=json.loads(page)['data'][0]['url']
        urllib.request.urlretrieve(url,path)
        return True;
    except Exception as e:
        print('Err:{}'.format(e));
        return False;
def getsonglist(url):
    url=url.replace('/#/','/')
    headers={
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Host': 'music.163.com'
        }
    req=urllib.request.Request(url,headers=headers)
    page = urllib.request.urlopen(req).read()
    page = page.decode('utf-8')
    pagetitle=re.search(r'<title>(.*?)</title>',page).group(1).split('-')[0]
    pattern = '<textarea.*?song-list-pre-data.*?>([\s\S]*?)</textarea>'
    res=re.search(pattern,page);
    list=json.loads(res.group(1))
    songitems=[['id','歌名','发布时间','时长','作者','评分']]
    if os.path.exists('./mp3file')==False:
        os.makedirs('./mp3file') 
    print('{},歌曲数量:{}'.format(pagetitle,len(list)))
    for song in list:
        pubtime=gettimebymils(song['publishTime'])
        duration=song['duration'];
        duration='{}分{}秒'.format(int(duration/60000),int((duration%60000)/1000))
        if duration[0]=='0':
            duration=duration.split('分')[1]
        author=''
        for a in song['artists']:
            author=author+','+a['name'] if author!='' else a['name'];
        songid=song['id'];
        name=song['name']
        score=song['score']
        songitems.append([songid,name,pubtime,duration,author,score])
        #print("歌曲《{}》下载中……".format(name));
        for rt in range(0,3):
            dr=downloadsong(str(songid),'./mp3file/'+str(songid)+'.mp3');
            if dr==False:
                print("歌曲《{}》失败,重试".format(name));
                continue;
            break;
        print("歌曲《{}》下载结果:{}".format(name,dr));
        #break;
    with open('res.csv','w',newline='') as of:
        spanwriter=csv.writer(of,dialect='excel')
        spanwriter.writerows(songitems)
    print('歌曲信息保存到res.csv中，mp3文件保存在mp3file目录内。')
getsonglist('https://music.163.com/#/discover/toplist?id=3778678');
#getsonglist('https://music.163.com/#/discover/toplist?id=2884035');
#downloadsong('1313354324','./1.mp4')
