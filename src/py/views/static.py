import os

from flask import send_from_directory


def send_js(path):
    return send_from_directory(os.environ['JS_DIR'], path)

def send_css(path):
    return send_from_directory(os.environ['CSS_DIR'], path)
