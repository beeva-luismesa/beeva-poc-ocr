#!/usr/bin/env python
from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages

install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

config = {
    "description": "PoC OCR over video frames",
    "author": "beeva-luismesa",
    "url": "",
    "download_url": "",
    "version": "1.0.0",
    "install_requires": reqs,
    "packages": find_packages(exclude=['tests*']),
    "name": "beeva-poc-ocr"
}

setup(**config)
