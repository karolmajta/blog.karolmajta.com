CONTENT_DIR:=$(CURDIR)/content
TEMPLATE_DIR:=$(CURDIR)/src/html
JS_DIR:=$(CURDIR)/build/js
CSS_DIR:=$(CURDIR)/build/css

prod-http-server:
	gunicorn \
--pythonpath=src/py \
--env CONTENT_DIR=$(CONTENT_DIR) \
--env TEMPLATE_DIR=$(TEMPLATE_DIR) \
--env JS_DIR=$(JS_DIR) \
--env CSS_DIR=$(CSS_DIR) \
wsgi:app

dev-http-server:
	CONTENT_DIR=$(CONTENT_DIR) \
TEMPLATE_DIR=$(TEMPLATE_DIR) \
JS_DIR=$(JS_DIR) \
CSS_DIR=$(CSS_DIR) \
JS_DIR=$(JS_DIR) \
python src/py/wsgi.py

develop:
	node_modules/.bin/gulp develop
