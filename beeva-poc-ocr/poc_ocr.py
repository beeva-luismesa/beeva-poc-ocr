import argparse
import importlib.machinery
import logging
import os
import fnmatch
import re
import types
from datetime import datetime

from controller.youtube_dl_controller import YoutubeDLController


class PoCOCR:
    def __init__(self, settings_path):
        loader = importlib.machinery.SourceFileLoader(settings_path, settings_path)
        self.__settings = types.ModuleType(loader.name)
        loader.exec_module(self.__settings)
        self.__youtube_dl_controller = YoutubeDLController(self.__settings.YDL_OPTS)

    def run_poc_ocr(self, video, output_path):
        try:
            if is_youtube_url(video):
                video_info = self.__youtube_dl_controller.get_info_from_youtube(video)
                self.__youtube_dl_controller.download_from_youtube(video)
                youtube_local_files = find_local_file("*{}.{}".format(video_info['id'], video_info['ext']),"./")
                os.remove(youtube_local_files[0])
            else:
                "TODO copy file to /tmp/"
        except Exception as ex:
            logging.exception("[PoC OCR] Exception: {}".format(ex.message))
            exit(-1)


def main():
    loader = importlib.machinery.SourceFileLoader("config/settings.py", "config/settings.py")
    settings = types.ModuleType(loader.name)
    loader.exec_module(settings)
    logging.basicConfig(filename=settings.LOG_PATH + str(datetime.today()), level=logging.INFO, format=settings.LOG_FORMAT)

    parser = argparse.ArgumentParser(description='PoC OCR')
    parser.add_argument('--video', type=valid_video, help='Local path or Youtube URL fof he video.', required=True)
    parser.add_argument('--output_path', type=valid_local_path, help='Local path to store output.', required=True)

    args = parser.parse_args()
    logging.info("Params <{}>".format(args))
    logging.info("Starting download process from TMDB")
    try:
        poc_ocr = PoCOCR("config/settings.py")
        poc_ocr.run_poc_ocr(args.video, args.output_path)
    except Exception as ex_main:
        logging.error("ERROR: An error raised and the process ended: {}".format(str(ex_main)))
        exit(-1)

    logging.info("Download process finished!")


def valid_video(path):
    try:
        if is_youtube_url(path):
            return path
        elif valid_local_path(path):
            return path
        else:
            msg = "Not a valid local video path or Youtube URL provided"
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Video path or Youtube URL validation error"
        raise argparse.ArgumentTypeError(msg)


def valid_local_path(path):
    if os.path.exists(os.path.dirname(path)):
        return path
    else:
        return None


def is_youtube_url(url):
    pattern = re.compile('^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$')
    return pattern.match(url)

def find_local_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


if __name__ == '__main__':
    main()
