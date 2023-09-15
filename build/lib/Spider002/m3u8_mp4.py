# -*0- coding: utf-8 -*-

import os
import sys
import requests
import threading
import queue
import time
import hashlib

# 参数配置

MX_WORKER_COUNT = 10
FFMPEG_PATH = '/Users/yangfangpeng/App/ffmpeg'
CACHE_PATH = os.path.join(os.getcwd(), "video")

DOWNLOAD_LIST = [
    # ['色情男女', 'https://bp1.dkkomo.com/stream/full/three/100/three-000064.m3u8'],
    # ['一路向西', 'https://s1.mimivodplay.com/mimi4/20211012/三级剧情/亚洲剧情-一路向西/SD/playlist.m3u8'],
    # ['一夜情深', 'https://bp1.dkkomo.com/stream/full/three/100/three-000044.m3u8'],
    # ['香蕉成熟时II初恋情人', 'https://s1.mimivodplay.com/mimi4/20210917/三级剧情/亚洲剧情-香蕉成熟时II初恋情人/SD/playlist.m3u8'],
    # ['香蕉成熟时III为你钟情', 'https://s1.mimivodplay.com/mimi4/20210917/三级剧情/亚洲剧情-香蕉成熟时II初恋情人/SD/playlist.m3u8'],
    # ['官人我要', 'https://s1.mimivodplay.com/mimi4/20210414/三级剧情/亚洲剧情-香蕉成熟时III为你钟情/SD/playlist.m3u8'],
    # ['赤裸羔羊', 'https://s1.mimivodplay.com/mimi4/20210928/三级剧情/亚洲剧情-赤裸羔羊/SD/playlist.m3u8'],
    # ['晚娘钟丽缇版', 'https://s1.mimivodplay.com/mimi4/20210720/三级剧情/亚洲剧情-晚娘钟丽缇版/SD/playlist.m3u8'],
    # ['青楼十二房', 'https://s1.mimivodplay.com/mimi4/20210730/三级剧情/亚洲剧情-青楼十二房/SD/playlist.m3u8'],
    # ['西厢艳谈', 'https://s1.mimivodplay.com/mimi4/20210803/三级剧情/亚洲剧情-西厢艳谈/SD/playlist.m3u8'],
    # ['聊斋艳谭续集五通神', 'https://s1.mimivodplay.com/mimi4/20210708/三级剧情/亚洲剧情-聊斋艳谭续集五通神/SD/playlist.m3u8'],
    # ['蜜桃成熟时II同居关系', 'https://s1.mimivodplay.com/mimi4/20210626/三级剧情/亚洲剧情-蜜桃成熟时II同居关系/SD/playlist.m3u8'],
    # ['足本玉蒲团', 'https://s1.mimivodplay.com/mimi4/20210619/三级剧情/亚洲剧情-足本玉蒲团/SD/playlist.m3u8'],
    # ['玉蒲团之云雨山庄', 'https://s1.mimivodplay.com/mimi4/20210502/三级剧情/亚洲剧情-玉蒲团之云雨山庄/SD/playlist.m3u8'],
    # ['素女真經', 'https://s1.mimivodplay.com/mimi4/20210615/三级剧情/亚洲剧情-素女真經The/SD/playlist.m3u8'],
    # ['都巿情緣之豔舞女郎', 'https://s1.mimivodplay.com/mimi4/20210612/三级剧情/亚洲剧情-都巿情緣之豔舞女郎/SD/playlist.m3u8'],
    # ['蔷薇之恋', 'https://s1.mimivodplay.com/mimi4/20210514/三级剧情/亚洲剧情-三级蔷薇之恋/SD/playlist.m3u8'],
    # ['杨乃武与小白菜', 'https://s1.mimivodplay.com/mimi4/20210420/三级剧情/亚洲剧情-杨乃武与小白菜/SD/playlist.m3u8'],
    ['韩国美妙的邂逅', 'https://vip5.3sybf.com/20210515/yZzvA8LE/index.m3u8'],
]


# 实现代码

def get_ts_file(ts_name):
    try:
        i = ts_name.index("/")
        tl = ts_name.split("/")
        for item in tl:
            if 'ts' in item:
                return item
    except Exception as e:
        return ts_name

class download_worker(threading.Thread):
    def __init__(self, threadId, name, download_path, taskQueue, queueLock):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.download_path = download_path
        self.taskQueue = taskQueue
        self.queueLock = queueLock
        self.worker_stop = False

    def do_download(self, task):
        pd_url = task["url"]
        c_fule_name = get_ts_file(task["name"])
        ts_index = task["index"]
        download_path = self.download_path

        if os.path.exists(os.path.join(download_path, c_fule_name)):
            print('exists : %s' % c_fule_name)
            return

        # download ts
        res = requests.get(pd_url)
        with open(os.path.join(download_path, c_fule_name), 'ab') as f:
            f.write(res.content)
            f.flush()

        print("worker[%d %s] download %d ts: %s finished ..." % (self.threadId, self.name, ts_index, c_fule_name))

    def stop(self):
        self.worker_stop = True
 
    def run(self):
        print("worker[%d %s] start ..." % (self.threadId, self.name))
        while not self.worker_stop:
            self.queueLock.acquire()
            if not self.taskQueue.empty():
                t = self.taskQueue.get()
                self.queueLock.release()
                # print("worker[%d %s] got task " % (self.threadId, self.name))
                self.do_download(t)
                self.taskQueue.task_done()
            else:
                self.queueLock.release()
            #time.sleep(1)

        print("worker[%d %s] exit ..." % (self.threadId, self.name))
        pass


class M3u8VideoDownloader():
    
    def __init__(self, m3u8_url, save_path, file_name):
        self.m3u8_url = m3u8_url
        self.save_path = save_path
        self.save_file_name = os.path.join(self.save_path, file_name) + '.mp4'
        self.m3u8_content = None
        self.video_directory = None
        self._download_ts_error = False
        self.type = ""

        if not os.path.exists(save_path):
            os.mkdir(save_path)

        if not os.path.exists(save_path):
            raise BaseException("save path invalid!")

    # m3u8 parser and downloader.
    def download(self):
        self.m3u8_content = self._download_hls_index(self.m3u8_url)
        if self.m3u8_content is None:
            print("下载m3u8文件出错!")
            return False
        self._download_hls_ts(self.m3u8_content)
        self._check_ts_list()
        return True

    def get_m3u8_url(self, url, ext_url):
        m3u8_url = url
        ul = url.split("/")
        exul = ext_url.split("/")
        for item in exul:
            if item == "":
                continue
            if item in ul:
                continue
            else:
                m3u8_url += '/' + item
        return m3u8_url

    # get m3u8 list
    def _download_hls_index(self, m3u8_url):
        # 创建一个以url的hash为名的文件夹，用来存储本视频的内容
        if self.video_directory is None:
            self.video_directory = os.path.join(self.save_path, hashlib.md5(m3u8_url.encode(encoding='UTF-8')).hexdigest())

        if not os.path.exists(self.video_directory):
            os.makedirs(self.video_directory)
        
        if not os.path.exists(self.video_directory):
            print("创建目标文件夹失败! %s" % (self.video_directory))
            return None

        #请求文件内容,并判断合法性，开始文件下载.
        print("download hls index file: %s" % (m3u8_url))
        res = requests.get(m3u8_url)
        text_content = res.text     # m3u8的文件内容
        text_content = text_content.replace("\r\n", "\n")   #统一换号符格式
        line_array = text_content.split("\n")
        if line_array[0] != "#EXTM3U":
            print("%s 不是一个合法的m3u8文件!" % (m3u8_url))
            return None

        #保存m3u8文件.
        with open(os.path.join(self.video_directory, hashlib.md5(m3u8_url.encode(encoding='UTF-8')).hexdigest() + ".m3u8"), 'ab') as f:
            f.write(res.content)
            f.flush()


        #这个m3u8文件是否为嵌套?
        if "EXT-X-STREAM-INF" in text_content:
            select_stream = None
            stream_list = []
            for index, line in enumerate(line_array):
                if "EXT-X-STREAM-INF" in line:
                    # stream_list.append(m3u8_url.rsplit("/", 1)[0] + "/" + line_array[index+1])
                    stream_list.append(self.get_m3u8_url(m3u8_url.rsplit("/", 1)[0], line_array[index+1]))
                pass

            stream_count = len(stream_list)
            if stream_count == 1:
                select_stream = stream_list[0]
            elif stream_count > 1:
                select_stream = stream_list[stream_count/2]

            if select_stream is None:
                print("没有合法的子m3u8地址!")
                return None

            return self._download_hls_index(select_stream)
        else:
            return line_array


    # download ts
    def _download_hls_ts(self, m3u8_content_lines):
        queueLock = threading.Lock()
        taskQueue = queue.Queue(10)
        threads = []
        threadId = 1
        threadName = "Worker_"
        ts_index = 0

        # 启动下载线程.....
        for i in range(0, MX_WORKER_COUNT):
            thread = download_worker(i, threadName + str(i), self.video_directory, taskQueue, queueLock)
            thread.start()

            threads.append(thread)

        # 生成任务列表
        for index, line in enumerate(m3u8_content_lines):
            t = None
            if "EXTINF" in line:
                # pd_url = url.rsplit("/", 1)[0] + "/" + m3u8_content_lines[index + 1]
                ts_url = self.get_m3u8_url(url.rsplit("/", 1)[0], m3u8_content_lines[index+1])
                c_fule_name = str(m3u8_content_lines[index + 1])

                t = {}
                t["url"] = ts_url
                t["name"] = c_fule_name
                t["index"] = ts_index
                t["type"] = 'ts'

                ts_index += 1
                pass

            elif "EXT-X-KEY" in line:
                segment_array = line.split(":")[1].split(",")
                for segment in segment_array:
                    if "URI" not in segment:
                        continue

                    kvs = segment.split("=")
                    key_name = kvs[1].replace("\"", "")
                    key_url = url.rsplit("/", 1)[0] + "/" + key_name

                    t = {}
                    t["url"] = key_url
                    t["name"] = key_name
                    t["index"] = -1
                    t["type"] = 'key'
                pass

            if t is not None:
                is_full = False
                queueLock.acquire()
                if not taskQueue.full():
                    is_full = False
                    taskQueue.put(t)
                else:
                    is_full = True
                queueLock.release()

                if is_full:
                    time.sleep(1)
    
        # 等待所有worker完成下载
        while True:
            queueLock.acquire()
            if taskQueue.empty():
                queueLock.release()
                break

            queueLock.release()
            time.sleep(1)

        for t in threads:
            t.stop()
    
        print("下载完成......")
        pass

    # 检查下载是否完整
    def _check_ts_list(self):
        file_list = []
        for index, line in enumerate(self.m3u8_content):
            if "EXTINF" in line:
                tsf = get_ts_file(str(self.m3u8_content[index + 1]))
                if os.path.exists(os.path.join(self.video_directory, tsf)):
                    file_list.append("file '%s'\n" % os.path.join(self.video_directory, tsf))
                else:
                    print("\n\n下载不完整，重新下载！\n\n")
                    self.download()

        with open(os.path.join(self.video_directory, 'filelist.txt'), 'w') as f:
            f.writelines(file_list)

    def merge_all_mp4(self):
        cmd = "%s/ffmpeg -y -f concat -safe 0 -i %s -c copy %s" % (FFMPEG_PATH, os.path.join(self.video_directory, 'filelist.txt'), self.save_file_name)
        os.popen(cmd)


if __name__ == '__main__':

    for title, url in DOWNLOAD_LIST:
        print('开始下载: %s' % title)
        downloader = M3u8VideoDownloader(url, os.path.join(CACHE_PATH, title), title)
        if not downloader.download():
            continue

        print('正在合并: %s' % title)
        downloader.merge_all_mp4()

        print('合并完成: %s' % downloader.save_file_name)
        
