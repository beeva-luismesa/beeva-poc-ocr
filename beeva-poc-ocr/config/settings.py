LOG_PATH = '/home/luismesa/demo_ocr/results/'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

YDL_OPTS = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'}

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
DEFAULT_THRESHOLD = 0.1

TXT_EXTENSION = '.txt'

PASSWORD_REGEXPS = [
    # Minimum eight characters, at least one letter and one number
    "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
    # Minimum eight characters, at least one letter, one number and one special character
    "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$",
    # Minimum eight characters, at least one uppercase letter, one lowercase letter and one number
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
    # Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
    # Minimum eight and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,10}"]

OCR_SPACE_API_KEY = ''
GOOGLE_CREDENTIALS = ''
