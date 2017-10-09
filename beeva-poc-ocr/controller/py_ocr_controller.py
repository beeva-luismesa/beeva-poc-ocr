import os

import pyocr
import pyocr.builders
from PIL import Image


class PyOCR(object):
    def __init__(self, settings):
        self.__settings = settings

    def perform_local_ocr(self, output_folder, lang):
        tool = self.get_ocr_tool()
        if tool:
            images_subfolder = os.path.join(output_folder, self.__settings.IMAGES_SUBFOLDER)
            text_subfolder = os.path.join(output_folder, self.__settings.TEXT_SUBFOLDER)

            if not os.path.exists(text_subfolder):
                os.makedirs(text_subfolder)

            for image in os.listdir(images_subfolder):
                image_path = os.path.abspath(
                    os.path.join(output_folder, self.__settings.IMAGES_SUBFOLDER, image))
                text = self.extract_text_from_image(tool, lang, image_path)
                file_name = os.path.splitext(os.path.basename(image_path))[0]

                with open(os.path.join(text_subfolder, "{}{}".format(file_name, self.__settings.TXT_EXTENSION)), "w") as text_file:
                    print(text, file=text_file)

    def extract_text_from_image(self, tool, lang, image_path):
        return tool.image_to_string(Image.open(image_path), lang=lang, builder=pyocr.builders.TextBuilder())

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
