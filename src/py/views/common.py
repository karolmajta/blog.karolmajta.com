from flask import render_template


def index():
    return render_template('common/index.html')


def about():
    return render_template('common/about.html')
