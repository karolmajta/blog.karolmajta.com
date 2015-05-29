import subprocess
import signal
import time
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from livereload import Server, shell

import flask
from flask import Flask, render_template
from flask.ext.frozen import Freezer

import url_generators.static
import url_generators.blog
import context_processors.environment
from routes import routes
from models.blog import BlogPostCollection

dirname = os.path.dirname
ROOT_PATH = dirname(dirname(dirname(os.path.abspath(__file__))))

class ReloadingEventsHandler(PatternMatchingEventHandler):

    def __init__(self, *args, **kwargs):
        self.freezer = kwargs.pop('freezer')
        self.throttle_seconds = kwargs.pop('throttle_seconds')
        PatternMatchingEventHandler.__init__(self, *args, **kwargs)
        self.last_event_time = 0

    def on_any_event(self, event):
        current_time = time.time() #
        if current_time - self.last_event_time < self.throttle_seconds:
            return
        else:
            self.last_event_time = current_time
            print "{f} changed, waiting freezer to complete...".format(
                f=event.src_path
            )
            self.freezer()
            print "Done."

def freezer(app):
    blogposts = BlogPostCollection(os.path.join(os.environ['CONTENT_DIR'], 'blog'))
    blogposts.build()
    app.blogposts = blogposts
    freezer = Freezer(app)
    freezer.register_generator(url_generators.static.js)
    freezer.register_generator(url_generators.static.css)
    freezer.register_generator(url_generators.static.img)
    freezer.register_generator(url_generators.blog.article_list)
    freezer.freeze()


def make_app(routes):
    app = Flask(
        __name__, template_folder=os.environ['TEMPLATE_DIR']
    )
    app.config['FREEZER_DESTINATION'] = os.path.join(ROOT_PATH, 'output')
    app.config['FREEZER_DESTINATION_IGNORE'] = [
        os.path.join(ROOT_PATH, 'build/css/*'),
        os.path.join(ROOT_PATH, 'build/js/*')
    ]
    app.context_processor(context_processors.environment.inject_environment)

    for route in routes:
        app.add_url_rule(*route)

    return app

if __name__ == "__main__":
    GULP_BIN = os.environ['GULP_BIN']
    JS_REL_DIR = os.environ['JS_REL_DIR']
    CSS_REL_DIR = os.environ['CSS_REL_DIR']
    IMG_REL_DIR = os.environ['IMG_REL_DIR']
    subprocess.Popen([
        GULP_BIN,
        'build',
        '--js-dir=' + JS_REL_DIR,
        '--css-dir=' + CSS_REL_DIR,
        '--img-dir=' + IMG_REL_DIR
    ]).wait()

    app = make_app(routes)
    freezer(app)

    handler = ReloadingEventsHandler(
        freezer=lambda: freezer(app),
        throttle_seconds=0.3,
        patterns=[
            './src/py/*.py',
            './src/html/*.html',
            './content/*',
            './build/*'
        ]
    )

    gulp = subprocess.Popen([
        GULP_BIN,
        'develop',
        '--js-dir=' + JS_REL_DIR,
        '--css-dir=' + CSS_REL_DIR,
        '--img-dir=' + IMG_REL_DIR
    ])

    observer = Observer()
    observer.schedule(handler, './src', recursive=True)
    observer.schedule(handler, './content', recursive=True)
    observer.schedule(handler, './build', recursive=True)
    observer.start()

    server = Server()
    server.watch('output/*')
    server.watch('output/*/*')
    server.watch('output/*/*/*')
    server.serve(root='output')
