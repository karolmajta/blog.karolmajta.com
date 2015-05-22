import flask


def article_list():
    blogposts = flask.current_app.blogposts
    for slug in blogposts.keys():
        yield ('article_detail', {'slug': slug})
