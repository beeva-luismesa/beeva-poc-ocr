import logging
import os

from controller.ffmpeg_controller import FFmpegController
from controller.py_ocr_controller import PyOCR
from controller.youtube_dl_controller import YoutubeDLController
from util.poc_ocr_util import find_local_file
from util.poc_ocr_util import is_youtube_url


class PoCOCRController(object):
    def __init__(self, settings):
        self.__settings = settings
        self.__youtube_dl_controller = YoutubeDLController(self.__settings)
        self.__ffmpeg_controller = FFmpegController(self.__settings)
        self.__py_ocr_controller = PyOCR(self.__settings)

    def run_poc_ocr(self, video, output_path, threshold, ocr, lang):
        try:
            if is_youtube_url(video):
                video_info = self.__youtube_dl_controller.get_info_from_youtube(video)
                self.__youtube_dl_controller.download_from_youtube(video)
                youtube_local_files = find_local_file("*{}.{}".format(video_info['id'], video_info['ext']), "./")
                output_folder = self.generate_frames_from_video(youtube_local_files[0], output_path, threshold)
                if ocr == self.__settings.TESSERACT:
                    self.__py_ocr_controller.perform_local_ocr(output_folder, lang)
                elif ocr == self.__setings.OCR_SPACE:
                    "Do OCR Space"
                else:
                    "Do Google CloudVision"
                os.remove(youtube_local_files[0])
            else:
                output_folder = self.generate_frames_from_video(video, output_path, threshold)
        except Exception as ex:
            logging.exception("[PoC OCR] Exception: {}".format(ex))
            exit(-1)

    def generate_frames_from_video(self, video_file, output_path, threshold):
        output_folder = self.__ffmpeg_controller.generate_frames_from_video(video_file, output_path, threshold)
        if not output_folder:
            raise Exception("Failed while trying to generate frames from video")
        else:
            return output_folder
