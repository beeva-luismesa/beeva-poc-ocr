LOG_PATH = '/tmp/'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

YDL_OPTS = {}

FRAME_NAME_PATTERN = 'frame_%06d.png'

FFMPEG_CMD = 'ffmpeg -i {} -vf "select=gt(scene\,{})" -vsync vfr {} -qscale 0'
IMAGES_SUBFOLDER = 'images'
TEXT_SUBFOLDER = 'text'

TESSERACT = 'tesseract'
GOOGLE_CLOUD_VISION = 'google-cloud-vision'
OCR_SPACE = 'ocr-space'

TESSERACT_TOOL_NAME = 'Tesseract (sh)'
TESSERACT_TOOL_DESIRED_LANGS = ['eng', 'spa']
PREFERRED_LANG = 'spa'

TXT_EXTENSION = '.txt'

OCR_SPACE_API_KEY=''
