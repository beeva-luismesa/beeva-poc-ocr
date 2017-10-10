from __future__ import unicode_literals

import logging
from youtube_dl import YoutubeDL


class YoutubeDLController(object):
    def __init__(self, settings):
        self.__settings = settings
        self.__ydl = YoutubeDL(self.__settings.YDL_OPTS)

    def get_info_from_youtube(self, url):
        logging.info("Getting info from youtube...")
        return self.__ydl.extract_info(url, download=False)

    def download_from_youtube(self, url):
        logging.info("Downloading from youtube...")
        self.__ydl.download([url])
