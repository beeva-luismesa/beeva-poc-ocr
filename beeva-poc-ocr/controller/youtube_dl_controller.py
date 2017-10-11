from __future__ import unicode_literals

import logging
from datetime import datetime

from youtube_dl import YoutubeDL


class YoutubeDLController(object):
    def __init__(self, settings):
        self.__settings = settings
        self.__ydl = YoutubeDL(self.__settings.YDL_OPTS)

    def get_info_from_youtube(self, url):
        logging.info("Getting info from youtube...")
        youtube_info_start = datetime.now()
        info = self.__ydl.extract_info(url, download=False)
        youtube_info_end = datetime.now()
        info_time = youtube_info_end - youtube_info_start
        logging.info("Total info time: {}s".format(info_time.total_seconds()))
        return info

    def download_from_youtube(self, url):
        logging.info("Downloading from youtube...")
        youtube_download_start = datetime.now()
        self.__ydl.download([url])
        youtube_download_end = datetime.now()
        download_time = youtube_download_end - youtube_download_start
        logging.info("Total download time: {}s".format(download_time.total_seconds()))
