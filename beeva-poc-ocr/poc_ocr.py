import argparse
import importlib.machinery
import logging
import os
import types
from datetime import datetime

from controller.poc_ocr_controller import PoCOCRController
from util.poc_ocr_util import is_youtube_url


class PoCOCR:
    def __init__(self, settings_path):
        loader = importlib.machinery.SourceFileLoader(settings_path, settings_path)
        self.__settings = types.ModuleType(loader.name)
        loader.exec_module(self.__settings)
        self.__poc_ocr_controller = PoCOCRController(self.__settings)

    def run(self, video, output_path, threshold, ocr, lang):
        try:
            self.__poc_ocr_controller.run_poc_ocr(video, output_path, threshold, ocr, lang)
        except Exception as ex:
            logging.exception("[PoC OCR] Exception: {}".format(ex))
            exit(-1)


def main():
    loader = importlib.machinery.SourceFileLoader("config/settings.py", "config/settings.py")
    settings = types.ModuleType(loader.name)
    loader.exec_module(settings)
    logging.basicConfig(filename=settings.LOG_PATH + str(datetime.today()), level=logging.INFO, format=settings.LOG_FORMAT)

    parser = argparse.ArgumentParser(description='PoC OCR')
    parser.add_argument('--video', type=valid_video, help='Local path or Youtube URL fof he video.', required=True)
    parser.add_argument('--output_path', type=valid_local_path, help='Local path to store output.', required=True)
    parser.add_argument('--scene_threshold', type=valid_threshold,
                        help='Threshold for scene change detection. A number between 0 and 100. Default: 50.', required=False, default=0.5)
    parser.add_argument('--ocr', choices=[settings.TESSERACT, settings.GOOGLE_CLOUD_VISION, settings.OCR_SPACE],
                        help="OCR choices. '{}' as a local choice. '{}' and '{}' as an external API choices.".format(settings.TESSERACT,
                                                                                                                     settings.GOOGLE_CLOUD_VISION,
                                                                                                                     settings.OCR_SPACE),
                        required=True)
    parser.add_argument('--lang', choices=settings.TESSERACT_TOOL_DESIRED_LANGS,
                        help="OCR language selected. '{}' by default".format(settings.PREFERRED_LANG), required=False,
                        default=settings.PREFERRED_LANG)

    args = parser.parse_args()
    logging.info("Params <{}>".format(args))
    logging.info("Starting process")
    ocr_start = datetime.now()
    try:
        poc_ocr = PoCOCR("config/settings.py")
        poc_ocr.run(args.video, args.output_path, args.scene_threshold, args.ocr, args.lang)
    except Exception as ex_main:
        logging.error("ERROR: An error raised and the process ended: {}".format(ex_main))
        exit(-1)

    ocr_end = datetime.now()
    total_time = ocr_end - ocr_start
    logging.info("Process finished!")
    logging.info("Total process time: {}s".format(total_time.total_seconds()))


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


def valid_threshold(i):
    try:
        val = int(i)
        if 0 < val <= 100:
            return float(val / 100)
        else:
            msg = "Not a valid integer: '{0}'. Value must be between 1 and 100.".format(i)
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        msg = "Not a valid integer: '{0}'. Value must be between 1 and 100.".format(i)
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    main()
