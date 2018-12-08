# coding: utf-8
import os
import sass
import sys
import vim

from config import PATH
from compatible import wrapper_lines


class Panel(object):
    filetype = None

    def __init__(self, buffer):
        if self.filetype:
            vim.command('buffer %d|e %s|setlocal filetype=%s' %
                        (buffer.number, self._getSuffix().upper(), self.filetype))
        buffer.options['buftype'] = 'nowrite'
        buffer.options['bufhidden'] = 'hide'
        buffer.options['swapfile'] = False
        buffer.vars['is_fiddle'] = True
        self._buffer = buffer

    def getBuffer(self):
        return self._buffer

    def read(self):
        return "\n".join(self._buffer[:])

    def readRaw(self):
        return "\n".join(self._buffer[:])

    def writeToFile(self):
        with open(self.getPath(), 'w') as fd:
            fd.write(self.read())
        self.writeRawToFile()

    def writeRawToFile(self):
        with open(self.getRawPath(), 'w') as fd:
            fd.write(self.readRaw())

    def getPath(self):
        return self._getPathBySuffix()

    def getRawPath(self):
        return self._getPathBySuffix(".buffer")

    def getRelativePath(self):
        return "index.%s" % self._getSuffix()


    def _getPathBySuffix(self, suffix=""):
        path = os.path.realpath(
            os.path.join(PATH, "%s%s" % (self.getRelativePath(), suffix))
        )
        return path

    def _getSuffix(self):
        return self.filetype

    def fillBuffer(self):
        path = self.getRawPath()
        if path and os.path.exists(path):
            with open(path) as fd:
                self.getBuffer().append(wrapper_lines(fd.readlines()), 0)
        while len(self.getBuffer()) > 1 and not self.getBuffer()[-1]:
            del self.getBuffer()[-1]

    def getWindow(self):
        for window in vim.windows:
            if self.getBuffer().number == window.buffer.number:
                return window
        return None

    def cleanUp(self):
        path = self.getPath()
        if path and os.path.exists(path):
            os.remove(path)

    def getCharset(self):
        charset = self.getBuffer().options['fileencoding']
        if not charset:
            charset = vim.eval('&encoding')
        if not charset:
            charset = 'utf-8'
        return charset


class HtmlPanel(Panel):
    filetype = "html"

    def afterBootstrap(self, js_panel, style_panel, setting_panel):
        self.js = js_panel
        self.style = style_panel
        self.setting = setting_panel
        self.writeToFile()
        self.js.writeToFile()
        self.style.writeToFile()


    def read(self):
        csses, scripts = self.setting.read()
        css_link, js_link = ('', '')
        if os.path.exists(self.style.getPath()):
            css_link = ("""
        <link rel="stylesheet" href="%(path)s" charset="%(charset)s">
""" % {'path': self.style.getRelativePath(), 'charset': self.style.getCharset()})
        if os.path.exists(self.js.getPath()):
            js_link =("""
        <script src="%(path)s" charset="%(charset)s"></script>
""" % {'path': self.js.getRelativePath(), 'charset': self.js.getCharset()})
        vars = {
            'charset': self.getCharset(),
            'extra_csses': csses,
            'css_link': css_link,
            'html': super(HtmlPanel, self).read(),
            'extra_scripts': scripts,
            'js_link': js_link,
        }

        content = ("""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="%(charset)s">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        %(extra_csses)s
        %(css_link)s
    </head>
    <body>
        %(html)s
        %(extra_scripts)s
        %(js_link)s
    </body>
</html>""" % vars)
        return content

    def embed(self):
        return self.read()


class JsPanel(Panel):
    filetype = "javascript"

    def __init__(self, buffer):
        super(type(self), self).__init__(buffer)
        self.getBuffer().vars['ternProjectDir'] = PATH

    def _getSuffix(self):
        return "js"

class StylePanel(Panel):
    filetype = "css"

    def read(self):
        raw = "\n".join(self._buffer[:])
        if not raw:
            return raw
        if self.filetype == "scss":
            try:
                return sass.compile(string=raw)
            except Exception as e:
                print(str(e), sys.stderr)
        return raw;

    def setFiletype(self, filetype):
        self.filetype = filetype
        self._buffer.options['filetype'] = filetype
        vim.command("file %s" % self._getSuffix().upper())

    def getRelativePath(self):
        return "index.css"


class SettingPanel(Panel):
    filetype = "dosini"

    def __init__(self, buffer, setting):
        super(type(self), self).__init__(buffer)
        vim.command('set nospell textwidth&')
        setting.setBuffer(buffer)
        self.setting = setting

    def fillBuffer(self):
        self.setting.write()
        self.init_cursor_postion()

    def getPath(self):
        return None

    def getRawPath(self):
        return None

    def getRelativePath(self):
        return None

    def _getSuffix(self):
        return 'conf'

    def read(self):
        return self.setting.render_output()

    def init_cursor_postion(self):
        window = self.getWindow()
        if not window:
            return
        for idx, line in enumerate(self.getBuffer()):
            if not line.strip() or line.strip()[0] in ';#[':
                continue
            col = line.find('=')
            if col == -1:
                continue
            while col < len(line) - 1 and line[col + 1] == ' ':
                col = col + 1
                window.cursor = (idx + 1, col + 1)
                return
# vim: cursorcolumn tabstop=4 expandtab shiftwidth=4 softtabstop=4 textwidth=79
