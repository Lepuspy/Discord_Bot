# -*- coding: utf-8 -*-

"""
Discord Bot Plugin
Template class
"""

from utilities.plugin import Plugin
from utilities.command import command,command_ja

class Temp(Plugin):
    #@command_ja(pattern="キー")     # in演算子
    @command(pattern="!key (.*)")   # 正規表現 match
    async def key(self, message, args):
        """
        Action:
            メッセージチェック & 処理
        Prameter:
            message: discord.message
            args : list or ()
        """

        mes = "送信メッセージ"
        await self.client.send_message(message.channel,mes)

