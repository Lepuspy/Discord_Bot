# -*- coding: utf-8 -*-
import re
from functools import wraps


def command(pattern=None, sub=""):
    """
    正規表現バージョン
    @command(pattern="キー")
    でデコレートするとコマンドリストに追加され検索されます
    デコレート先関数の引数は(message, args)とする
    """
    def actual_decorator(func):
        prog = re.compile(pattern + sub)
        @wraps(func)
        async def wrapper(self, message):
            match = prog.match(message.content.lower())
            if not match:
                return False
            args = match.groups()

            if args != ():
                args = args[0].split()
            await func(self, message, args)

        wrapper._is_command = True
        return wrapper
    return actual_decorator

def command_ja(pattern=None, sub=None):
    """
    if文 バージョン
    @command(pattern="キー")
    でデコレートするとコマンドリストに追加され検索されます
    デコレート先関数の引数は(message, args)とする
    """
    def actual_decorator(func):
        @wraps(func)
        async def wrapper(self, message):
            mes = message.content.split()
            if not mes[0] in [pattern, sub]:
                return False
            args = mes[1:]
            await func(self, message, args)
        wrapper._is_command = True
        return wrapper
    return actual_decorator


