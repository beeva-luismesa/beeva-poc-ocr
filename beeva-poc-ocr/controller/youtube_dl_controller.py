from __future__ import unicode_literals
from youtube_dl import YoutubeDL


class YoutubeDLController(object):
    def __init__(self, ydl_opts):
        self.__ydl = YoutubeDL(ydl_opts)

    def get_info_from_youtube(self, url):
        return self.__ydl.extract_info(url, download=False)

    def download_from_youtube(self, url):
        self.__ydl.download([url])
