import pyocr
import pyocr.builders
from PIL import Image


class PyOCR(object):
    def __init__(self, settings):
        self.__settings = settings

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

    def extract_text_from_image(self, tool, lang, image_path):
        return tool.image_to_string(Image.open(image_path), lang=lang, builder=pyocr.builders.TextBuilder())
