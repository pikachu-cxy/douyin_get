import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
import json
import os
import re
from urllib import parse
from urllib.parse import urlparse

import requests
from tqdm import tqdm

class VideoDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("抖音视频下载器")

        self.label_url = tk.Label(master, text="请输入要下载的视频网址：")
        self.label_url.pack()

        self.entry_url = tk.Entry(master, width=50)
        self.entry_url.pack()

        self.label_path = tk.Label(master, text="请选择保存视频的路径：")
        self.label_path.pack()

        self.path_button = tk.Button(master, text="选择路径", command=self.choose_path)
        self.path_button.pack()

        self.button = tk.Button(master, text="开始下载", command=self.download_video)
        self.button.pack()

        self.save_path = ""

    def choose_path(self):
        # 弹出文件选择窗口
        self.save_path = filedialog.asksaveasfilename(defaultextension=".mp4")

    def download_video(self):
        # 获取用户输入的网址
        url_down = self.entry_url.get()

        request_url = requests.get(url=url_down)
        if not request_url.status_code == 200:
            print("ok")
        else:
            print("not ok")

        url = "https://www.wouldmissyou.com/api/parse/"
        response = requests.post(url=url, data={"link_text": url_down})
        if not response.status_code == 200:
            print("解析失败")
            return
        json_response = json.loads(response.text)
        json_response = json_response['data']
        if not json_response['code'] == 0:
            print(json_response['message'])
            return
        # 获取视频链接
        video_url = json_response['data']['videoUrls']


        # 发送HTTP请求
        r = requests.get(video_url, stream=True)


        # 保存视频到用户指定的路径
        with open(self.save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.close()

        # 提示下载完成
        tk.messagebox.showinfo("提示", "视频下载完成！")


root = tk.Tk()
gui = VideoDownloaderGUI(root)
root.mainloop()
