# BEEVA PoC OCR

This module is built in order to evaluate the capability of several OCR software for reading the text from a set of video frames extracted from a local or youtube video.

We have tested `Tesseract`, as a local choice, and `Google Cloud Vision` and `OCR.Space`, as API choices.

## Configuration

Before using this module you may need setting up your OS, get an API key for `Google Cloud Vision` or `OCR.Space` and configure a settings file.

### OS and system requirements

In this section, we are going to describe the environment used for this experiment. You must have the following requirements in your OS:

* A `Debian` based OS (`Debian` itself, any flavour of `Ubuntu` or `Linux Mint`, etc.)
* `python3` (tested with 3.5.3 version)
* `python3-pip` (tested with 9.0.1 version)
* `ffmpeg` (tested with 3.2.7 version)
* `tesseract-ocr` and languages files for English and Spanish (tested with 3.04 version)

You can install it from terminal typing the following command:

```bash
apt-get install -y python3 python3-pip ffmpeg tesseract-ocr tesseract-ocr-eng tesseract-ocr-spa libtesseract-dev
```
Don't forget to install the external python dependencies by using pip:

```bash
pip3 install -r requirements.txt
```

### API Keys

You must have an account in `Google Cloud` and `OCR.Space` in order to use their APIs. In this section, it's explained how to get an API Key for this services.

#### OCR.Space

By registering in [OCR.Space](https://ocr.space/ocrapi) website, you can get a free API Key for using their service with the following restrictions:

* 25.000 maximum requests per month
* 1 MB file size limit
* 500 calls by day

The registration process is very easy. You only have to fill up [this form](http://space.us11.list-manage1.com/subscribe?u=ce17e59f5b68a2fd3542801fd&id=252aee70a1) and they will send you your key to the registration e-mail.

#### Google Cloud Vision

You should register in [Google Cloud Platform](https://cloud.google.com/) before using Google Cloud Vision API. It's a process a little bit tedious because we need to link a credit card to the account. In our case, we use a virtual prepaid credit card. For our purpose, if we don't exceed the free tier use of the APIs or services in GCP, we won't be charged at all. [These are the prices](https://cloud.google.com/vision/pricing) of the Text Detection feature of [Google Cloud Vision API](https://cloud.google.com/vision/). For our experiment, we only have to keep in mind that the first 1.000 units per month are free. Then, it will be $1.5 per each 1.000 units. By the way, [these](https://cloud.google.com/vision/quotas) are the quota restrictions for using this service:

* 4 MB image file size limit
* 16 images per request
* 8 MB request total size limit
* Maximin 600 requests per minute

Once registered in GCP, we must go to the [console view](https://console.cloud.google.com/start) and click on "Create empty project". Then, when created, we must select our project in the top left dropdown. After that, you should see a menu on the left. Select the "Credentials" options. In the middle of the screen, you must see a button labeled "Create credentials". Choose the "API key" option and close the window.

Finally, you have to enable Google Cloud Vision API. To do that, select the option "Library" on the left menu and find the "Google Cloud Vision API" on the "Machine Learning" section and push "Enable" button on the [subsequent page](https://console.cloud.google.com/apis/library/vision.googleapis.com/). 

### Settings file

In this repository, under beeva-poc-ocr/config, you can find a [settings.py](https://github.com/beeva-luismesa/beeva-poc-ocr/blob/master/beeva-poc-ocr/config/settings.py) example file. You can configure any option, but these are the most relevant:

```python
LOG_PATH = '/local/path/to/save/logfiles/'
FRAME_NAME_PATTERN = 'prefix_of_output_files_%06d.png'

IMAGES_SUBFOLDER = 'name_of_frames_subfolder'
TEXT_SUBFOLDER = 'name_of_extracted_text_subfolder'

OCR_SPACE_API_KEY='yoUrocR.SpaCeapiKeY'
GOOGLE_CREDENTIALS='YouRgoOgleCloudvisIonApIkEy'
```

## Usage

You can use this module in two ways: standalone mode and python package.

### Standalone

Once installed required dependencies, you can run the python module with these parameters (optional parameters between brackets):

```bash
Usage
	poc_ocr.py [-h] --video VIDEO --output_path OUTPUT_PATH --ocr {tesseract,google-cloud-vision,ocr-space} [--scene_threshold SCENE_THRESHOLD] [--lang {eng,spa}]

Arguments description	
	-h, --help          show this help message and exit
	--video VIDEO       Local path or Youtube URL fof he video.
	--output_path OUTPUT_PATH
	                    Local path to store output.
	--ocr {tesseract,google-cloud-vision,ocr-space}
	                    OCR choices. 'tesseract' as a local choice. 'google-cloud-vision' and 'ocr-space' as an external API choices.
	--scene_threshold SCENE_THRESHOLD
                        Threshold for scene change detection. A number between 0 and 100. Default: 10.
	--lang {eng,spa}    OCR language selected. 'spa' by default.

Example call
	python3 poc_ocr.py --video https://www.youtube.com/watch?v=SL-QtqfgqTI --output_path /home/luismesa/Escritorio/demo_ocr/ --ocr google-cloud-vision --scene_threshold 10 --lang spa

```

### Python package

Installed as a dependency, or requirement, in another python module, you only have to create a *PoCOCR* class with the settings file and call directly the *run* method with the proper parameters. This is an example (note in this case, *scene_threshold* is a float between 0.0 and 1.0):
 
```python
poc_ocr = PoCOCR("/path/to/settings.py")
poc_ocr.run('https://www.youtube.com/watch?v=nHc288IPFzk', '/home/my_user/desktop', 0.1, 'ocr-space', 'spa')
```
## Changelog

v1.0.0

Initial Release