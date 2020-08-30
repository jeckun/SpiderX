# SpiderBook

### 说明：
这个爬虫专门实现图书的下载。

### 使用方法：
- 第一步：打开config，填写必要的参数。

        Header： 是Http请求头，可以通过一些网络工具获取到。
        
        THREAD_NUM： 是同时下载线程数，如果想下的快一些，可以适当加大线程数。
        
- 第二步：打开download.txt，这是下载脚本，对某个网站爬取数据，都需要指定下载脚本。

        脚本编写方法：
        
        1. 使用Chrome打开目标网站；
        2. 进入Chrome开发者模式，使用定位工具，找到需要爬取的信息，在Elements页签下，在目标标签上点鼠标右键，选择Copy->Copy Selector。
        3. 粘贴到脚本中；
        4. 脚本编写格式：行动命令 + 定位标志(Selector文本) + [to/in] + 目标对象
           含义是：用这个命令，找到目标网页的指定位置，获取响应信息，放入/从，变量
        5. 脚本编写好之后，就可以执行脚本。在命令行输入: python run.py
        
### 脚本解释

- 脚本
    
        - Load: 加载网页
        格式： load <url>
        
        - get_a_text: 获取指定位置的文本，放到Book对象的指定属性中
        格式： get_a_text <Selector> to title
        
        - get_a_href：获取a标签的网址，放到Book对象指定的属性中
        格式： get_a_href <Selector> to url
        
        - get_a_list: 获取网页在指定a标签的列表，列表内容包括：章节名称和获取网址，放到Book对象的指定属性(catalog_list)中
        格式： get_a_list <Selector> to catalog_list
        
        - download_list: 从刚才的章节列表(catalog_list)中，下载章节内容
        格式: download_list <Selector> in catalog_list
        
        - quit: 用于退出脚本，当然不放也行。

### 更新日志

- 日志

        2020-8-27 v1.03 之前已经使用Spider、Book、Page、Script这几个类实现了，图书网站某一本小说的下载。但遗留了小说信息没有保存，小说封面图片无法下载，以及脚本编写方式不合理等问题，有待改进！
        2020-8-29 v1.03 实现了多线程下载。
        2020-8-30 v1.04 代码复用，将spiderx、script放入Lib。
