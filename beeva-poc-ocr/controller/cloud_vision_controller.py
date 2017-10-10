import base64
import logging
import os

from googleapiclient.discovery import build


class CloudVisionController(object):
    def __init__(self, settings):
        self.__settings = settings
        self.__google_service = build('vision', 'v1', developerKey=self.__settings.GOOGLE_CREDENTIALS, cache_discovery=False)

    def perform_cloud_vision(self, image_path, text_subfolder, file_name):
        text = self.call_cloud_vision_with_local_file(image_path)
        with open(os.path.join(text_subfolder, "{}{}".format(file_name, self.__settings.TXT_EXTENSION)), "w") as text_file:
            print(text, file=text_file)

    def call_cloud_vision_with_local_file(self, image_path):
        logging.info("Calling Google cloud vision with image: {}".format(image_path))
        text_result = str()
        try:
            with open(image_path, "rb") as imageFile:
                image_file = imageFile.read()
                image_bytes = bytearray(image_file)

                image_b64 = base64.b64encode(image_bytes).decode()
                r = self.__google_service.images().annotate(body={
                    'requests': [{
                        'image': {
                            'content': image_b64
                        },
                        'features': [{
                            'type': 'DOCUMENT_TEXT_DETECTION',
                            'maxResults': 5,
                        }]
                    }]
                }).execute()

                if r and r['responses'] and r['responses'][0] and r['responses'][0]['fullTextAnnotation'] and r['responses'][0]['fullTextAnnotation'][
                    'text']:
                    text_result = r['responses'][0]['fullTextAnnotation']['text']
        except Exception as ex:
            logging.error("ERROR reading text from Google Cloud Vision: {}".format(ex))

        return text_result
