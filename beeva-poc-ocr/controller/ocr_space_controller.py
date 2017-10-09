import json
import logging
import os

import requests


class OCRSpaceController(object):
    def __init__(self, settings):
        self.__settings = settings

    def perform_ocr_space(self, image_path, text_subfolder, file_name, lang):
        text = self.call_ocr_space_with_local_file(image_path, lang)
        with open(os.path.join(text_subfolder, "{}{}".format(file_name, self.__settings.TXT_EXTENSION)), "w") as text_file:
            print(text, file=text_file)

    def call_ocr_space_with_local_file(self, filename, language, overlay=False):

        text_result = str()
        try:
            payload = {'isOverlayRequired': overlay,
                       'apikey': self.__settings.OCR_SPACE_API_KEY,
                       'language': language,
                       }
            with open(filename, 'rb') as f:
                r = requests.post('https://api.ocr.space/parse/image',
                                  files={filename: f},
                                  data=payload,
                                  )
                if r and r.status_code == 200:
                    decoded_content = r.content.decode()
                    json_content = json.loads(decoded_content)
                    if json_content and json_content['ParsedResults'] and json_content['ParsedResults'][0] and json_content['ParsedResults'][0][
                        'ParsedText']:
                        text_result = json_content['ParsedResults'][0]['ParsedText']
        except Exception as ex:
            logging.error("ERROR reading text from OCR Space: {}".format(ex))

        return text_result
