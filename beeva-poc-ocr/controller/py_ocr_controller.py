import logging
import os
from datetime import datetime

import pyocr
import pyocr.builders
from PIL import Image


class PyOCRController(object):
    def __init__(self, settings):
        self.__settings = settings
        self.__tool = self.get_ocr_tool()

    def perform_local_ocr(self, image_path, text_subfolder, file_name, lang):
        text = self.extract_text_from_image(lang, image_path)
        with open(os.path.join(text_subfolder, "{}{}".format(file_name, self.__settings.TXT_EXTENSION)), "w") as text_file:
            print(text, file=text_file)

    def extract_text_from_image(self, lang, image_path):
        logging.info("Calling tesseract text with image: {}".format(image_path))
        ocr_start = datetime.now()
        text = self.__tool.image_to_string(Image.open(image_path), lang=lang, builder=pyocr.builders.TextBuilder())
        ocr_end = datetime.now()
        ocr_time = ocr_end - ocr_start
        logging.info("Local OCR processing image time: {}s".format(ocr_time.total_seconds()))
        return text

    def get_ocr_tool(self):
        tool_found = None
        tools = pyocr.get_available_tools()
        if len(tools) > 0:
            for tool in tools:
                if tool.get_name() == self.__settings.TESSERACT_TOOL_NAME:
                    tool_found = tool
                    break
            if tool_found:
                for lang in self.__settings.TESSERACT_TOOL_DESIRED_LANGS:
                    if lang not in tool.get_available_languages():
                        return None
        return tool_found
