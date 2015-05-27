import os
import glob
import markdown
from collections import OrderedDict

import iso8601
from slugify import slugify


class InvalidBlogPost(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)


class BlogPost(object):

    required_meta = ['date', 'author', 'title', 'subtitle']

    def __init__(self, raw):
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.codehilite',
                'markdown.extensions.meta',
            ],
            extension_configs={
                'markdown.extensions.codehilite': {
                    'noclasses': True,
                    'pygments_style': 'tango',
                }
            }
        )
        self.raw = raw
        self.html = md.convert(raw.decode('utf-8'),)
        try:
            self.meta = md.Meta
            self.date = iso8601.parse_date(self.meta.get('date')[0])
            self.author = self.meta.get('author')[0]
            self.title = self.meta.get('title')[0]
            self.subtitle = self.meta.get('subtitle')[0]
            self.slug = self.meta.get('slug', slugify(self.title))
            self.tags = BlogPost._parse_tags(self.meta.get('tags', [''])[0])
        except Exception as e:
            raise InvalidBlogPost(e.message)

    @staticmethod
    def _parse_tags(tags_str):
        return filter(lambda x: x, [t.strip() for t in tags_str.split(',')])


class BlogPostCollection(object):

    def __init__(self, source_directory):
        self.dict = {}
        self.source_directory = source_directory
        self._tags = None
        self._categories = None

    def build(self):
        glob_pattern = os.path.join(self.source_directory, '*/*.markdown')
        filenames = glob.glob(glob_pattern)
        for i, content in enumerate(BlogPostCollection._contents(filenames)):
            try:
                blogpost = BlogPost(content)
                self.dict.update(**{blogpost.slug: blogpost})
            except InvalidBlogPost as e:
                print filenames[i], e, "IGNORED"

    def get(self, slug):
        return self.dict.get(slug, None)

    def latest(self):
        try:
            return sorted(self.dict.values(), key=lambda p: p.date, reverse=True)[0]
        except IndexError:
            return None

    def keys(self):
        return self.dict.keys()

    @staticmethod
    def _contents(filenames):
        for filename in filenames:
            with open(filename, 'r') as fp:
                yield fp.read()
