from flask import render_template, current_app

def article_detail(slug=None):
    if slug is None:
        blogpost = current_app.blogposts.latest()
    else:
        blogpost = current_app.blogposts.get(slug)
    return render_template('blog/article_detail.html', blogpost=blogpost)
