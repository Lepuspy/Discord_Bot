# -*- coding: utf-8 -*-
import inspect
from discord.errors import Forbidden


class PluginMount(type):

    def __init__(cls, name, bases, attrs):
        """Pluginの派生クラス読み込まれた時に呼び出されます"""
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

"""
Plugin 作成継承クラス
"""

class Plugin(metaclass=PluginMount):
    def __init__(self, client):
        self.client = client
        self.commands = {}
        for name, member in inspect.getmembers(self):
            if hasattr(member, '_is_command'):
                self.commands[name] = member
        
    async def _on_message(self, message):
        
        for func in self.commands.values():
            try:
                if await func(message) != False:
                    return
            except Forbidden as e:
                msg = ":no_entry_sign: 権限を持っていない為実行出来ませんでした"
                await self.client.send_message(message.channel, msg)
        
        
    async def _on_ready(self):
        return
    async def _on_member_join(self, member):
        return
