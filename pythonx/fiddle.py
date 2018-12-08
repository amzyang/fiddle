# coding: utf-8
""" TODO
* 支持在 buffer 显示当前编辑文件类型，用颜色填充色块来绘出背景文字，可能参考
ctrl-v
* 支持常用 js 库
* 常用 js 库 可以下载到本地
* 支持 sass less scss coffeescript javascript 1.7 markdown haml
* figlet -f banner HTML | vim -
    HTML CSS JavaScript Setting
"""
import vim
import os
import shutil

from setting import Setting
from SettingObservable import SettingObservable
from panel import (
    HtmlPanel,
    JsPanel,
    StylePanel,
    SettingPanel,
)
from config import (
    PATH,
    ASSETS_PATH,
)

# I don't know why "cd PATH" doesn't work.
if not os.path.exists(PATH):
    os.mkdir(PATH)
vim.chdir(PATH)

class Storage:
    _changed = False
    panels = []

    def addPanel(self, panel):
        if not self.getPanelByBuffer(panel.getBuffer()):
            self.panels.append(panel)

    def build(self):
        target_assets_path = os.path.join(PATH, "node_modules")
        if not os.path.exists(PATH):
            os.mkdir(PATH)
        else:
            if os.path.exists(target_assets_path):
                if os.path.islink(target_assets_path):
                    os.unlink(target_assets_path)
                else:
                    shutil.rmtree(target_assets_path)
        os.symlink(ASSETS_PATH, target_assets_path)

    def addHtmlPanel(self, panel):
        self._html_panel = panel
        self.addPanel(panel)

    def getHtmlPanel(self):
        return self._html_panel

    def getPanelByBuffer(self, buffer):
        for panel in self.panels:
            if panel.getBuffer().valid and \
                    buffer.number == panel.getBuffer().number and \
                    panel.getBuffer().vars['is_fiddle']:
                return panel
        return None

    def getActivePanel(self):
        buffer = vim.current.buffer
        return self.getPanelByBuffer(buffer)

    def fillAllBuffer(self):
        for panel in self.panels:
            panel.fillBuffer()

    def wipeOutAll(self):
        """Remove all buffers."""
        for panel in self.panels:
            if panel.getBuffer().vars['is_fiddle']:
                vim.command("bwipeout %d" % panel.getBuffer().number)
        self.panels = []

    def setChanged(self):
        self._changed = True

    def setUnChanged(self):
        self._changed = False

    def isChanged(self):
        return self._changed


storage = Storage()
fired = False
observable = SettingObservable()
setting = Setting(observable)


def bootstrap():
    global fired

    ctrl_w = ""
    if not fired:
        vim.command("augroup fiddle")
        vim.command("autocmd!")
        vim.command("autocmd TextChangedI * py fiddle.text_changed_i()")
        vim.command("autocmd TextChanged * py fiddle.text_changed()")
        vim.command("autocmd InsertLeave * py fiddle.insert_leave()")
        vim.command("autocmd VimResized * :normal %s=" % ctrl_w)
        vim.command("autocmd VimEnter,WinEnter,BufWinEnter * "
                    "py fiddle.enable_cursorline()")
        vim.command("autocmd WinLeave * py fiddle.disable_cursorline()")
        vim.command("augroup END")
        storage.build()
        fired = True
    storage.wipeOutAll()

    if not isBlankTab(vim.current.tabpage):
        vim.command('tabnew')
    panel = HtmlPanel(latestBuffer())
    storage.addHtmlPanel(panel)

    vim.command('rightbelow vnew')
    style_panel = StylePanel(latestBuffer())
    style_panel.setFiletype(setting.getStyle())
    storage.addPanel(style_panel)

    vim.command('botright new')
    setting_panel = SettingPanel(latestBuffer(), setting)
    storage.addPanel(setting_panel)

    vim.command('vnew')
    js_panel = JsPanel(latestBuffer())
    storage.addPanel(js_panel)

    html_panel = storage.getHtmlPanel()
    storage.fillAllBuffer()
    html_panel.afterBootstrap(js_panel, style_panel, setting_panel)
    vim.command("normal %s=" % ctrl_w)
    vim.command("normal %st" % ctrl_w)


def enable_cursorline():
    if storage.getActivePanel():
        vim.command("setlocal cursorline")


def disable_cursorline():
    if storage.getActivePanel():
        vim.command("setlocal nocursorline")


def init():
    vim.command("command Fiddle py fiddle.bootstrap()")
    vim.command("command -nargs=1 -complete=file FiddleExport py fiddle.export(<f-args>)")


def text_changed_i():
    if not storage.getActivePanel():
        return
    storage.setChanged()


def text_changed():
    panel = storage.getActivePanel()
    if panel:
        update(panel)


def insert_leave():
    if not storage.isChanged():
        return
    panel = storage.getActivePanel()
    if panel:
        update(panel)


def update(panel):
    target_panel = panel
    if isinstance(panel, SettingPanel):
        observable.settingUpdated()
        target_panel = storage.getHtmlPanel()
    target_panel.writeToFile()
    storage.setUnChanged()


def export(path):
    text = storage.getHtmlPanel().embed()
    with open(path, 'w') as fp:
        fp.write(text)


def isBlankTab(tab):
    """检测标签页是否为空
    空标签页判定条件如下：

    * 标签页内窗口数为1
    * 窗口内当前 buffer 名为空
    * buffer 内容为空
    """
    if len(tab.windows) != 1:
        return False
    buffer = tab.window.buffer
    if buffer.name or len(buffer) > 1 or buffer[0]:
        return False
    return True


def latestBuffer():
    return vim.current.buffer
