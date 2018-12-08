# coding: utf-8
import vim


def warning(string):
    vim.command('echohl ErrorMsg | echomsg "%s" | echohl None' % string)
# vim: cursorcolumn tabstop=4 expandtab shiftwidth=4 softtabstop=4 textwidth=79
