# coding: utf-8
# Find the best implementation available on this platform
import os
import platform
import json
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
from ConfigParser import SafeConfigParser
from message import warning
from config import PATH
from compatible import wrapper_lines


class Setting(object):
    default = """[Framework]
; axios bootstrap d3 font-awesome jquery knockout lodash vue vue-router vuex
; libs = bootstrap
libs     =
user_js  =
user_css =

[Setting]
; yes or no - should normalize.css be loaded before any CSS declarations?
normalize_css = no
dtd           = HTML 5
; Body tag
body          = <body>
; Head
head          =
; wrap
; set the JS code wrap:
; 1 - onLoad
; 2 - domReady
; 3 - No wrap - in <head>
; 4 - No wrap - in <body>
wrap          = 1
; css language
style         = css
"""
    libs = {
        'axios': {
            'js': ['node_modules/axios/dist/axios.js'],
            'css': [],
            'dependencies': [],
        },
        'bootstrap': {
            'js': ['node_modules/bootstrap/dist/js/bootstrap.js'],
            'css': ['node_modules/bootstrap/dist/css/bootstrap.css',
                    'node_modules/bootstrap/dist/css/bootstrap-theme.css'],
            'dependencies': ['jquery'],
        },
        'd3': {
            'js': ['node_modules/d3/d3.js'],
            'css': [],
            'dependencies': [],
        },
        'font-awesome': {
            'js': [],
            'css': ['node_modules/font-awesome/css/font-awesome.css'],
            'dependencies': [],
        },
        'jquery': {
            'js': ['node_modules/jquery/dist/jquery.js'],
            'css': [],
            'dependencies': [],
        },
        'knockout': {
            'js': ['node_modules/knockout/build/output/knockout-latest.js'],
            'css': [],
            'dependencies': [],
        },
        'lodash': {
            'js': ['node_modules/lodash/lodash.js'],
            'css': [],
            'dependencies': [],
        },
        'vue': {
            'js': ['node_modules/vue/dist/vue.js'],
            'css': [],
            'dependencies': [],
        },
        'vue-router': {
            'js': ['node_modules/vue-router/dist/vue-router.js'],
            'css': [],
            'dependencies': ['vue'],
        },
        'vuex': {
            'js': ['node_modules/vuex/dist/vuex.js'],
            'css': [],
            'dependencies': ['vue'],
        },
    }

    def __init__(self, observable):
        self._parser = None
        self._observable = observable
        self._observable.addObserver(self)

    def _get_parser(self):
        if not self._parser:
            self._parser = SafeConfigParser(allow_no_value=True)
            config = self._get_default_fp()
            self._parser.readfp(config)
            config.close()
        return self._parser

    def _get_fp(self, content):
        config = StringIO(content)
        return config

    def _get_config_path(self):
        special = "_" if platform.system() == "Windows" else "."
        return os.path.expanduser("~/%svim_fiddle.conf" % special)

    def _get_default_fp(self):
        path = self._get_config_path()
        if os.path.exists(path):
            return open(path, 'rw')
        fp = StringIO(self.default)
        return fp

    def setBuffer(self, buffer):
        self.buffer = buffer

    def write(self):
        self.buffer.append(wrapper_lines(self._get_default_fp().readlines()), 0)
        while len(self.buffer) > 1 and not self.buffer[-1]:
            del self.buffer[-1]
        for nr, line in enumerate(self.buffer):
            self.buffer[nr] = line.strip()

    def update(self, observable):
        default_config = self._get_default_fp()
        user_config = self._get_fp("\n".join(self.buffer[:]))
        self._parser = SafeConfigParser(allow_no_value=True)
        self._parser.readfp(default_config)
        self._parser.readfp(user_config)

        default_config.close()
        user_config.close()

        with open(self._get_config_path(), 'w') as fp:
            fp.write("\n".join(self.buffer[:]))
        self.ternSupport()

    def ternSupport(self):
        _, js_list = self.get_all_assets()
        config = {
            'libs': ['browser', ],
            'loadEagerly': list(js_list),
        }
        with open(os.path.join(PATH, ".tern-project"), "w") as fp:
            fp.write(json.dumps(config))

    def render_output(self):
        css_list, js_list = self.get_all_assets()
        return (self._render_libs('css', css_list),
                self._render_libs('js', js_list))

    def get_all_assets(self):
        (css_list, js_list) = ([], [])
        strip = lambda _: _.strip()
        parser = self._get_parser()
        section = 'Framework'
        if parser.has_option(section, 'user_css'):
            value = parser.get(section, 'user_css')
            css_list = value.split(' ') if value else []

        if parser.has_option(section, 'user_js'):
            value = parser.get(section, 'user_js')
            js_list = value.split(' ') if value else []

        if parser.has_option(section, 'libs'):
            value = parser.get(section, 'libs')
            if value:
                libs = set(filter(bool, map(strip, value.split(' '))))
                dependencies = set()
                for lib in libs:
                    self.get_all_dependencies(lib, dependencies)
                for name in dependencies:
                    if name not in self.libs:
                        warning("%s lib doesn't exist!" % name)
                        continue
                    group = self.libs[name]
                    if 'js' in group:
                        js_list += group['js']
                    if 'css' in group:
                        css_list += group['css']
        js_list = set(filter(bool, map(strip, js_list)))
        css_list = set(filter(bool, map(strip, css_list)))
        return (css_list, js_list)

    def get_all_dependencies(self, framework, dependencies):
        group = self.libs[framework]
        for dependency in group['dependencies']:
            if dependency in dependencies:
                continue
            dependencies.add(dependency)
            self.get_all_dependencies(dependency, dependencies)
        dependencies.add(framework)


    def getStyle(self):
        parser = self._get_parser()
        section = 'Setting'
        if parser.has_option(section, 'style'):
            return parser.get(section, 'style')
        return 'css'


    def _render_libs(self, tag, libs):
        libs = filter(bool, libs)
        if tag == 'css':
            pattern = ('<link href="%s" rel="stylesheet" type="text/css" '
                       'media="all">')
        elif tag == 'js':
            pattern = '<script type="text/javascript" src="%s"></script>'
        else:
            raise Exception("unknown tag")
        tag_func = lambda _: pattern % _

        return "\n".join(map(tag_func, libs))
