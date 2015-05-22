import os
import glob


JS_DIR = os.environ['JS_DIR']
CSS_DIR = os.environ['CSS_DIR']


def js():
    abspaths = glob.glob(os.path.join(JS_DIR, '*'))
    relpaths = [os.path.relpath(p, JS_DIR) for p in abspaths]
    for path in relpaths:
        yield ('send_js', {'path': path})


def css():
    abspaths = glob.glob(os.path.join(CSS_DIR, '*'))
    relpaths = [os.path.relpath(p, CSS_DIR) for p in abspaths]
    for path in relpaths:
        yield ('send_css', {'path': path})
