# 163MusicSA
163 Music Self Analysis-爬取个人听歌排行中歌曲信息，生成词云  
>参考地址  
[NacedWang/163MusicSpider](https://github.com/NacedWang/163MusicSpider) 基础代码部分  
[Samaritan·J](https://blog.csdn.net/u010890916/article/details/106879465/) 爬取个人排行界面  

![][python]  

**模块**:  

![][selenium-badge]  

安装指令：`pip install selenium`  

**外部浏览器支持**:  
![][chrome]  

[![chromedriver-badge]][chromedriver-link] 
[**ChromeDriver使用教程**](https://blog.csdn.net/weixin_41990913/article/details/90936149)

+ 目前能够生成的词云
  1. 歌手名
  2. 歌词

## 使用
+ 1. 创建数据库，修改`sql.py`内连接数据库相关信息  
+ 2. 修改`main.py`内的`user_id=''`，运行`main.py`  

[python]: https://img.shields.io/badge/python-3.8-blue?logo=python
[selenium-badge]: https://img.shields.io/badge/selenium-3.141.0-blue?logo=python
[chromedriver-badge]: https://img.shields.io/badge/ChromeDriver-86.0.4240.22-blue
[chromedriver-link]: http://npm.taobao.org/mirrors/chromedriver/86.0.4240.22/
[chrome]: https://img.shields.io/badge/Chrome-86.0.4240.75-blue
