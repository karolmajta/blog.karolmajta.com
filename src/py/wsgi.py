import signal
import time
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import flask
from flask import Flask, render_template
from flask.ext.frozen import Freezer

import url_generators.static
import url_generators.blog
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

app = Flask(
    __name__, template_folder=os.environ['TEMPLATE_DIR']
)

app.config['FREEZER_DESTINATION'] = os.path.join(ROOT_PATH, 'output')
app.config['FREEZER_DESTINATION_IGNORE'] = [
    os.path.join(ROOT_PATH, 'build/css/*'),
    os.path.join(ROOT_PATH, 'build/js/*')
]

for route in routes:
    app.add_url_rule(*route)

def freezer():
    blogposts = BlogPostCollection(os.path.join(os.environ['CONTENT_DIR'], 'blog'))
    blogposts.build()
    app.blogposts = blogposts
    freezer = Freezer(app)
    freezer.register_generator(url_generators.static.js)
    freezer.register_generator(url_generators.static.css)
    freezer.register_generator(url_generators.blog.article_list)
    freezer.freeze()

def watch_files():
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    freezer()

    handler = ReloadingEventsHandler(
        freezer=freezer,
        throttle_seconds=0.3,
        patterns=[
            './src/py/*.py',
            './src/html/*.html',
            './content/*',
            './build/*'
        ]
    )
    observer = Observer()
    observer.schedule(handler, './src', recursive=True)
    observer.schedule(handler, './content', recursive=True)
    observer.schedule(handler, './build', recursive=True)
    observer.start()

    from livereload import Server, shell
    server = Server()
    server.watch('output/*')
    server.watch('output/*/*')
    server.watch('output/*/*/*')
    server.serve(root='output')
