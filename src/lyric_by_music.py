"""
根据歌曲 ID 获得所有的歌曲所对应的热门评论和歌词
"""
import datetime
import json

import random
import re
import time


import requests


# from src import sql, redis_util
# from src.util.user_agents import agents
lyr=''
import sql
from util.user_agents import agents

def clearInf(lyr,n):
        n-=1
        if(re.search('.*:(.*)\n',lyr)):
            rs0=re.search('.*:(.*)\n',lyr).span()[0]
            rs1=re.search('.*:(.*)\n',lyr).span()[1]
            temp=lyr[rs0:rs1]
            lyr=lyr.replace(temp,'')
        elif(re.search('.*：(.*)\n',lyr)):
            rs0=re.search('.*：(.*)\n',lyr).span()[0]
            rs1=re.search('.*：(.*)\n',lyr).span()[1]
            temp=lyr[rs0:rs1]
            lyr=lyr.replace(temp,'')
        else:
            if(re.search(':',lyr)):
                if(re.search(':',lyr).span()[0]>len(lyr)/2):
                    rs=re.search('\n(.*):(.*)',lyr).span()[0]
                    temp=lyr[rs:]
                    lyr=lyr.replace(temp,'')
            if(re.search('：',lyr)):
                if(re.search('：',lyr).span()[0]>len(lyr)/2):
                    rs=re.search('\n(.*)：(.*)',lyr).span()[0]
                    temp=lyr[rs:]
                    lyr=lyr.replace(temp,'')
        #作曲 :  aaa/bbb\n
        if(n!=0):
            return clearInf(lyr,n)
        return lyr
    
class LyricComment(object):
    headers = {
        
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 获取数据多了之后，就会被禁用访问,可以使用代理
        'Cookie': 'MUSIC_U=f8b73ab123ddad32d44c37546522e06bb123363f4b813922a1902f2ds2ceb750c52sd32ccbb1ab2b9c23asd3a31522c7067cce3c7469;',
        'DNT': '1',
        'Host': 'music.163.com',
        'Pragma': 'no-cache',
        'Referer': 'http://music.163.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    
    }
    
    
    def saveLyric(self, music_id):
        # 获取歌手个人主页
        agent = random.choice(agents)
        self.headers["User-Agent"] = agent
        url = 'http://music.163.com/api/song/lyric?id=' + str(music_id) + '&lv=1&kv=1&tv=1'
        # 去redis验证是否爬取过
        r = requests.get(url, headers=self.headers)
        # 解析
        lyricJson = json.loads(r.text)
        # 保存redis去重缓存
        if ('lrc' in lyricJson):
            # 把歌词里的时间干掉
            regex = re.compile(r'\[.*\]')
            finalLyric = re.sub(regex, '', lyricJson['lrc']['lyric']).strip()
            #把歌词中的作词作曲等信息去掉
            n=finalLyric.count(":")
            if(n==0):
                n=finalLyric.count("：")
            print(n)
            global lyr
            lyr=finalLyric
            
            if(n!=0):
                finalLyric=clearInf(finalLyric,n)
            # 持久化数据库
            
            try:
                sql.insert_lyric(music_id, finalLyric)
            except Exception as e:
                print(music_id, "insert error", str(e))
        else:
            print(str(music_id), "has no lyric", lyricJson)
        # 请求完成后睡一秒 防作弊
        time.sleep(1)



def lyricSpider():
    print("======= 开始爬 歌词 信息 ===========")
    startTime = datetime.datetime.now()
    print(startTime.strftime('%Y-%m-%d %H:%M:%S'))
    # 所有歌手数量
    # 批次
    my_lyric_comment = LyricComment()
    offset = 0
    musics = sql.get_all_music2()
    print("offset:", offset, "artists :", len(musics), "start")
    for item in musics:
        try:
            my_lyric_comment.saveLyric(item['music_id'])
        except Exception as e:
            # 打印错误日志
            print(item['music_id'], ' internal  error : ' + str(e))
            # traceback.print_exc()
            time.sleep(1)
    print("======= 结束爬 歌词 信息 ===========")
    endTime = datetime.datetime.now()
    print(endTime.strftime('%Y-%m-%d %H:%M:%S'))
    print("耗时：", (endTime - startTime).seconds, "秒")


if __name__ == '__main__':
    lyricSpider()

