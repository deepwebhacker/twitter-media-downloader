# twitter-media-downloader 推特媒体文件下载工具

用于下载推特页面中包含的媒体文件（支持文本, 图片, 视频, 动图）的脚本工具, 使用推特网页版的 api 获取数据

支持输入如下四种格式的链接:

1. https://<span></span>twitter.com/\*\*\*/status/\*\*\* (推文)
2. https://<span></span>twitter.com/\*\*\* (推主主页, 调用主页接口, \*\*\*为推主 id, 用于批量爬取)
3. https://<span></span>twitter.com/\*\*\*/media (推主media页, 调用media接口, \*\*\*为推主 id, 用于批量爬取)
4. @\*\*\* (\*\*\*为推主 id, 调用搜索接口, 用于批量爬取)

不同接口区别： [关于api接口](#关于api接口)

# donate 赞助

作者开发维护不易, 若喜欢本项目, 欢迎前往 [爱发电](https://afdian.net/@mengzonefire) 支持作者

# tips 提示

1. 获取到的媒体文件默认下载到程序同目录下的 **twitter_media_download** 文件夹
2. 设置年龄限制/锁定 的 推主/推文 必须设置 cookie 才能爬取, 设置完成后, cookie会保存到本地, 下次运行程序自动读取
3. 下载文件名格式: **{推主 id}\_{推文 id}\_{服务器文件名}**, 例如 memidesuyo_1441613758988574723_FAGkEkFVEAI8GSd.jpg
4. 默认使用系统代理, 无需配置 (仅 win 平台, 其余平台请手动设置)，但注意程序仅支持http代理
5. 爬取视频文件时, 会自动选择最高分辨率下载, 图片文件则自动选择原图画质
6. 支持爬取推文文本, 自动保存为 **{推主 id}\_{推文 id}.txt**
7. 若出现任何问题/提意见&需求, 请前往 [issue](https://github.com/mengzonefire/twitter-media-downloader/issues) 反馈
8. 程序的配置文件路径: * 配置文件内含proxy(代理)，download_path(下载路径)，UA和cookie四项配置
    * linux: ~/tw_media_downloader.conf
    * win: %userprofile%/tw_media_downloader.conf

# usage 使用方法

* 若使用python3环境运行py代码，注意先安装依赖：

    ```
    pip install -r requirements.txt
    ```

  1. 直接运行程序:  
  运行后根据提示输入 命令 或 推文/推主链接即可.
      ```
      python3 twitter-media-downloader.py
      ```
      <img src="https://pic.rmb.bdstatic.com/bjh/08934029f23df12817604a44d48fb01d.png">
      
      示例：
       * 下载单条推文 ```https://<span></span>twitter.com/user/status/0000000000000000000```
       * 下载用户主页 ```https://<span></span>twitter.com/user```
       * 下载用户媒体页 ```https://<span></span>twitter.com/user/media```
       * 下载用户[搜索页](#搜索接口用法) ```@user```  
       * 下载用户[搜索页](#搜索接口用法)并指定日期 ```@user&2022-12-1|2022-12-10```  
       * 高级搜索， 包含#tag1和#tag2，并指定推文来自用户user ```@&advanced=(#tag1 AND #tag2) (from:user)```  
         * 注：脚本搜索页默认不包含回复，如需爬取回复请使用高级搜索
  2. 命令行调用:
       ```
       usage: twitter-media-downloader.py [-h] [-c COOKIE] [-p PROXY] [-u USER_AGENT]
                                         [-d DIR] [-n] [-q] [-r] [-t] [-v]
                                         [url [url ...]]

       positional arguments:
         url                   tw url to gather media, must be like:
                                   1. https://twitter.com/***/status/***
                                   2. https://twitter.com/***(/media) (user page, *** is user_id)
                                   # 2. will gather all media files of user's tweets

       optional arguments:
         -h, --help            show this help message and exit
         -c COOKIE, --cookie COOKIE
                               set cookie to access locked users or tweets, input " " to clear
         -p PROXY, --proxy PROXY
                               set network proxy, must be http proxy, input " " to clear
         -u USER_AGENT, --user_agent USER_AGENT
                               set user-agent, input " " to clear
         -d DIR, --dir DIR     set download path
      
         -n NUM, --num NUM     set the number of concurrency
      
         -q QUOTED, --quoted QUOTED
                               set whether to include quoted tweets
         -r RETWEETED, --retweeted RETWEETED
                               set whether to include retweeted
         -t TYPE, --type TYPE  
                               set the desired media type, optional: photo&animated_gif&video&full_text
         -v, --version         show version
       ```
      示例：
       * 下载用户主页，并包含转推 `python twitter-media-downloader.py https://twitter.com/user`
       * 下载用户主页，不包含转推 `python twitter-media-downloader.py -r https://twitter.com/user`
       * 下载用户媒体页，不包含引用 `python twitter-media-downloader.py -q https://twitter.com/user/media`
       * 下载用户搜索页，不包含引用 `python twitter-media-downloader.py -q @user`
         * `-r` 和 `-q` 是开关，默认开启，不带为包含，带上为不包含
       * 下载用户搜索页，指定下载类型为图片和视频 `python twitter-media-downloader.py -t "photo&video" @user`
       * 下载用户搜索页，指定日期为2022-12-1到2022-12-20 `python twitter-media-downloader.py "@user&2022-12-1|2022-12-20"`
       * 高级搜索 [详情](#搜索接口用法)，搜索包含#tag1和#tag2，并指定推文来自用户user `python twitter-media-downloader.py "@&advanced=(#tag1 AND #tag2) (from:user)"`
   
   ## 搜索接口用法
   1. 构成： `@用户名&附加命令`
   2. 使用 `@` 开头
   3. 使用 `&` 连接用户名与附加命令
   4. 使用 `|` 连接日期 `2020-1-1|2021-1-1`
   5. 使用命令行传入参数运行时一定要使用双引号包住 `"@user&2020-1-1|2021-1-1"`
   6. 高级搜索： 前往 [推特高级搜索页](https://twitter.com/search-advanced?f=live) 填写并搜索，然后复制搜索框内容，将内容粘贴至 `@&advanced=` 后面
   7. 关于高级搜索的tag：推特默认使用 `#taga OR #tagb` 意为包含taga或者包含tagb，但是可以手动修改为 `#taga AND #tagb` ，意为含taga并且包含tagb
    

# 关于api接口
目前有四个不同的下载接口，分别是单条推文的下载接口、用户主页的下载接口、用户媒体页的下载接口、搜索页的下载接口。**只有搜索接口能查看用户所有推文。**  

|                     |  单条推文   |  用户主页   |  用户媒体页  |   搜索页   |
|:-------------------:|:-------:|:-------:|:-------:|:-------:|
|        推文数量         |  ★☆☆☆☆  |  ★★☆☆☆  |  ★★★☆☆  |  ★★★★★  |
|        包含引用         |    ✔    |    ✔    |    ✔    |    ✔    |
|        包含转推         |    ❌    |    ✔    |    ❌    |    ❌    |
|  高级用法<br/>（标签、日期等）  |    ❌    |    ❌    |    ❌    |    ✔    |



# dev note 开发记录

1. ~~发现有个同名的插件, 而且还更好用, 故本项目停止开发.~~ (发现自己的脚本还是有点优势的, 继续开发吧)

   (插件地址: [谷歌插件商店](https://chrome.google.com/webstore/detail/twitter-media-downloader/cblpjenafgeohmnjknfhpdbdljfkndig))

2. 废弃 TODO#9, 因为考虑到脚本的主要耗时是下载而非解析数据, 故用 TODO#22 作为替代

# TODO 待实现需求

1. ~~支持 cmd 传参调用~~ (完成)
2. ~~支持爬取视频/动图文件~~ (完成)
3. ~~支持批量爬取推主所有媒体~~ (完成)
4. ~~下载进度显示~~ (完成)
5. ~~分模块重构代码方便后续开发~~ (完成)
6. ~~支持手动设置 UA 和代理~~ (完成)
7. ~~支持设置 cookie 用于爬取锁推~~ (完成)
8. ~~完善程序错误 log 导出~~ (完成, 现会在崩溃后写入完整 log 到文件)
9. ~~批量爬取时输出进度记录, 并在程序异常退出重启后导入进度继续下载~~ (废弃)
10. ~~在文件名前添加推文 id, 方便定位推文~~ (完成)
11. ~~支持自定义下载路径~~ (完成)
12. ~~提供推文 id 转推文 url 功能~~ (完成)
13. 提供语言设置(中/英), 翻译text.py提示文本和readme 页面
14. ~~退出时保存 UA/代理/cookie 到配置文件, 下次运行程序自动读取设置~~ (完成)
15. ~~在直接运行程序的交互模式下加入 cookie,下载路径,代理的设置命令~~ (完成)
16. ~~添加自动更新功能&CI 自动编译~~ (完成)
17. ~~废弃推文 id 转 url 功能, 并将下载文件的格式设置为: {推主 id}\_{推文 id}\_{服务器文件名} (方便定位推文 url)~~ (完成)
18. ~~添加自定义关键字/正则表达式, 提取推文中的 url 链接~~ (废弃, 由 TODO#23 替代)
19. ~~添加媒体文件的筛选提取功能(例如 仅图片, 仅视频)~~ (完成)
20. ~~添加推主转载推文的媒体提取功能~~ (废弃, 转载推文没有独立的获取接口)
21. ~~优化启动逻辑, 启动时网络检查失败不再强制跳出程序~~ (完成)
22. ~~下载文件时跳过目标路径下已存在的文件, 避免重复下载~~ (完成)
23. ~~添加爬取推文文本内容的功能(可选参数)~~ (完成)
24. ~~使用多线程并发下载多个文件, 提高下载速度(可选线程并发数)~~ (完成)
25. ~~已知 UserMedia api 会把已删除的推文一起返回, 占用 count, 导致爬取内容不完整, 尝试修复~~ (完成)
26. ~~支持输入空配置项(例如cookie设置), 用于重置对应配置~~ (完成, cookie, proxy, ua均已支持)
27. ~~配置cookie时添加完整的cookie校验, 防止输错cookie导致接口返回403~~ (已修复, 其实是正则写错导致cookie解析错误)
28. ~~userMedia接口老是缺数据, 将批量爬取的逻辑改为从userMedia提取tw_id, 然后丢到singlePageTask去执行~~ (已修复, 实际问题为部分用户/推文有年龄限制, 需要设置cookie才能正常访问, 1.2.3版本已加入提示)
29. 目前版本的代理逻辑相当的蠢, 由于直接运行时优先使用配置文件内的代理设置, 且首次检测到系统代理会保存到配置文件, 导致系统代理修改时无法生效, 下版本优化
30. ~~直接运行模式下, 完善操作提示, 照顾小白~~ (完成)
31. GUI (可能要等很久才能写出来)

# preview 预览

批量下载:  
<img src="https://pic.rmb.bdstatic.com/bjh/e7bb8983c155712b6175e99f9f66ff35.png">
