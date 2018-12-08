# coding: utf-8
import vim


def wrapper_lines(lines):
    has_nvim = vim.eval('has("nvim")')
    if has_nvim:
        """neovim 设置 buffer 内容时，不能含有换行符"""
        return map(lambda _: _.rstrip(), lines)
    return lines
