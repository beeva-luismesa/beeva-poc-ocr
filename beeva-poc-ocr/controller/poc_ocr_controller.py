import logging
import os
from datetime import datetime

from controller.cloud_vision_controller import CloudVisionController
from controller.ffmpeg_controller import FFmpegController
from controller.ocr_space_controller import OCRSpaceController
from controller.py_ocr_controller import PyOCRController
from controller.youtube_dl_controller import YoutubeDLController
from util.poc_ocr_util import find_local_file
from util.poc_ocr_util import is_youtube_url


class PoCOCRController(object):
    def __init__(self, settings):
        self.__settings = settings
        self.__youtube_dl_controller = YoutubeDLController(self.__settings)
        self.__ffmpeg_controller = FFmpegController(self.__settings)
        self.__ocr_controller = None

    def run_poc_ocr(self, video, output_path, threshold, ocr, lang):
        try:
            if is_youtube_url(video):
                logging.info("It's a youtube video! Here we go!")
                video_info = self.__youtube_dl_controller.get_info_from_youtube(video)
                self.__youtube_dl_controller.download_from_youtube(video)
                youtube_local_files = find_local_file("*{}.{}".format(video_info['id'], video_info['ext']), "./")
                output_folder = self.generate_frames_from_video(youtube_local_files[0], output_path, threshold)
                self.perform_ocr_subprocess(ocr, output_folder, lang)
                os.remove(youtube_local_files[0])
            else:
                logging.info("It's a local video! Here we go!")
                output_folder = self.generate_frames_from_video(video, output_path, threshold)
                self.perform_ocr_subprocess(ocr, output_folder, lang)
        except Exception as ex:
            logging.exception("[PoC OCR] Exception: {}".format(ex))
            exit(-1)

    def perform_ocr_subprocess(self, ocr, output_folder, lang):
        logging.info("Performing OCR with {}".format(ocr))

        images_subfolder = os.path.join(output_folder, self.__settings.IMAGES_SUBFOLDER)
        text_subfolder = os.path.join(output_folder, self.__settings.TEXT_SUBFOLDER)

        if not os.path.exists(text_subfolder):
            os.makedirs(text_subfolder)

        logging.info("Images subfolder will be: {}".format(images_subfolder))
        logging.info("Text subfolder will be: {}".format(text_subfolder))
        if ocr == self.__settings.TESSERACT:
            self.__ocr_controller = PyOCRController(self.__settings)
        elif ocr == self.__settings.OCR_SPACE:
            self.__ocr_controller = OCRSpaceController(self.__settings)
        else:
            self.__ocr_controller = CloudVisionController(self.__settings)

        whole_images_start = datetime.now()
        for image in os.listdir(images_subfolder):
            image_path = os.path.abspath(
                os.path.join(output_folder, self.__settings.IMAGES_SUBFOLDER, image))
            file_name = os.path.splitext(os.path.basename(image_path))[0]

            logging.info("Processing image: {}".format(image_path))
            if ocr == self.__settings.TESSERACT:
                self.__ocr_controller.perform_local_ocr(image_path, text_subfolder, file_name, lang)
            elif ocr == self.__settings.OCR_SPACE:
                self.__ocr_controller.perform_ocr_space(image_path, text_subfolder, file_name, lang)
            else:
                self.__ocr_controller.perform_cloud_vision(image_path, text_subfolder, file_name)
        whole_images_end = datetime.now()
        total_ocr_time = whole_images_end - whole_images_start
        logging.info("Total OCR time: {}s".format(total_ocr_time.total_seconds()))

    def generate_frames_from_video(self, video_file, output_path, threshold):
        logging.info("Generating frames from video {}".format(video_file))
        output_folder = self.__ffmpeg_controller.generate_frames_from_video(video_file, output_path, threshold)
        if not output_folder:
            raise Exception("Failed while trying to generate frames from video")
        else:
            return output_folder
