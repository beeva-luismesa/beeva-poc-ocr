import io
import logging
import os

from google.cloud import vision
from google.cloud.vision import types


class CloudVisionController(object):
    def __init__(self, settings):
        self.__settings = settings
        self.__client = vision.ImageAnnotatorClient(credentials=self.__settings.GOOGLE_CREDENTIALS)

    def perform_cloud_vision(self, image_path, text_subfolder, file_name):
        text = self.call_cloud_vision_with_local_file(image_path)
        with open(os.path.join(text_subfolder, "{}{}".format(file_name, self.__settings.TXT_EXTENSION)), "w") as text_file:
            print(text, file=text_file)

    def call_cloud_vision_with_local_file(self, image_path):

        text_result = str()
        try:
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            response = self.__client.text_detection(image=image)
            texts = response.text_annotations

            for text in texts:
                text_result += '\n"{}"'.format(text.description)

        except Exception as ex:
            logging.error("ERROR reading text from Cloud Vision: {}".format(ex))

        return text_result
