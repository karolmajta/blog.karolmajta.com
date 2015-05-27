import views.common
import views.blog
import views.static

routes = (
    ('/', 'index', views.common.index),
    ('/about/', 'about', views.common.about),

    ('/blog/', 'article_newest', views.blog.article_detail),
    ('/blog/<string:slug>/', 'article_detail', views.blog.article_detail),

    ('/js/<path:path>', 'send_js', views.static.send_js),
    ('/css/<path:path>', 'send_css', views.static.send_css),
    ('/img/<path:path>', 'send_img', views.static.send_img),
)
