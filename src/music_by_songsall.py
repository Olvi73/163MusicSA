# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 21:16:12 2020

@author: Oliver
"""

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import sql

uid = '381212571'#随时可替换用户id
url_recd = 'https://music.163.com/#/user/songs/rank?id='+uid#构建爬取url
unknown = '未知'#特殊情况下错误提示用
asingerlist = []#储存所有时间排行中所有歌手的列表
start = time.time()#设置计时器
samaritan =webdriver.Chrome()#webdriver实例化
song={}
def get_record():#创建获取歌手信息的方法
    samaritan.get(url_recd)
    #实例化对象访问url
    samaritan.switch_to.frame('g_iframe')
    #找到指定iframe标签（这里是g_iframe）然后跳入
    samaritan.implicitly_wait(10)#隐式等待
    samaritan.maximize_window()
    time.sleep(0.5)
    # if samaritan.find_element_by_id("songsall").is_displayed() == True:
    #     print ('可见')
    # else:
    #     print ('不可见')
    # if samaritan.find_element_by_id("songsall").is_enabled() == True:
    #     print ('可点击')
    # else:
    #     print ('不可点击')
    # samaritan.find_element_by_id("songsall").click()
    # #定位到切换到所有时间的按钮标签
    #模拟鼠标点击查看所有时间下的听歌排行
    samaritan.implicitly_wait(10)#隐式等待
    time.sleep(0.5)#这里还需要强制等待加载时间，一般一秒内就可以了
    htmlrec = samaritan.page_source
    #此时网页成为静态页面，获取所有页面信息
    pagerec = BeautifulSoup(htmlrec, 'html.parser')#使用bs4解析静态网页
    allrec = pagerec.find(class_="g-wrap p-prf").find(class_="m-record").find(class_="j-flag").find_all('li')
    #定位该位置下所有<li>的标签
    # try:#使用try except结构防止意外报错中断运行
    #     for music in allrec:
    #         music = music.find('a')
    #         music_id = music['href'].replace('/song?id=', '')
    #         music_name = music.getText()
    #         song[music_name]=music_id
    #定位该位置下所有<li>的标签
    try:#使用try except结构防止意外报错中断运行
        for i in allrec:
        #遍历刚才位置下每一个<li>标签内信息
            asinger = i.find(class_="s-fc8").text.replace('-', '')
            #定位并获取歌手文本信息，再用replace方法清洗文本去掉歌名和各种之间连结的'-'
            asingerlist.append(asinger)
            #将干净的歌手文本加入列表
            music = i.find(class_="txt").find('a')
            music_name = music.getText()
            music_id = music['href'].replace('/song?id=', '')
            song[music_name]=music_id
            try:
                sql.insert_music2(music_id, music_name,asinger)
            except Exception as e:
                # 打印错误日志
                print(' inset db error: ', str(e))
                # traceback.print_exc()
                time.sleep(1)
    except:
        print(unknown)
        #如遇到意外，提示'未知'。
    return pagerec
        
p=get_record()#调用爬取方法
samaritan.close()#关闭浏览器
end = time.time()#结束计时
print(asingerlist)#打印所有歌手列表
print(f'总共用时:{end-start}秒')#打印程序用时