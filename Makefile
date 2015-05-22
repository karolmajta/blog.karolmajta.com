GULP_BIN = node_modules/.bin/gulp
CONTENT_DIR:=$(CURDIR)/content
TEMPLATE_DIR:=$(CURDIR)/src/html
JS_REL_DIR:=build/js
CSS_REL_DIR:=build/css
JS_DIR:=$(CURDIR)/$(JS_REL_DIR)
CSS_DIR:=$(CURDIR)/$(CSS_REL_DIR)

develop:
	GULP_BIN=$(GULP_BIN) \
CONTENT_DIR=$(CONTENT_DIR) \
TEMPLATE_DIR=$(TEMPLATE_DIR) \
JS_REL_DIR=$(JS_REL_DIR) \
CSS_REL_DIR=$(CSS_REL_DIR) \
CSS_DIR=$(CSS_DIR) \
JS_DIR=$(JS_DIR) \
python src/py/wsgi.py
