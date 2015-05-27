import flask
from flask import render_template


def index():
    blogpost = flask.current_app.blogposts.latest()
    blogposts = flask.current_app.blogposts.all()[1:6]
    return render_template(
        'common/index.html',
        blogpost=blogpost,
        blogposts=blogposts,
    )

def about():
    return render_template('common/about.html')
