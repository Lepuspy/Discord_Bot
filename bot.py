# -*- coding: utf-8 -*-
"""
Discord BOT
機能をプラグインとしてすぐ追加しやすくすることを目標に

<機能一覧>
・BTC価格表示機能


"""
__author__ = "Lepus <lepuspy@gmail.com>"
__version__ = "1.0"
__date__    = "2018/08/03"

import discord
from configparser import ConfigParser
from utilities.plugin_manager import PluginManager
import asyncio


CFG_FILE = "config.ini"


class Kuritchi(discord.Client):

    def __init__(self, config):
        super().__init__()
        # iniファイルのコンフィグデータを取得
        self.config = config
        # プラグインを全て読み込む
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()
        self.loops = asyncio.get_event_loop()
        

    def defaults(self):
        self.server = discord.utils.get(self.servers, id=self.config["Discord"]["server_id"])
        self.role_channel = discord.utils.get(self.server.channels, id=self.config["plugin"]["role_channel"])
        self.user_role = discord.utils.get(self.server.roles, name="USER")

    async def on_ready(self):
        """接続準備完了時"""
        self.defaults()
        for plugin in self.plugins:
            self.loops.create_task(plugin._on_ready())
        print("BOT-NAME :", self.user.name)
        print('ログインしました')
        
            
    async def on_member_join(self,member):
        """サーバーメンバー入室時"""
        for plugin in self.plugins:
            self.loops.create_task(plugin._on_member_join(member))
        return
    async def on_message(self, message):
        """メッセージ受信時"""
        # 自分が送った or TEXTメッセージ以外はパス
        if self.user == message.author or message.type != discord.MessageType.default:
            return
        print(f"{message.author.name}: {message.content}")
        for plugin in self.plugins:
            self.loops.create_task(plugin._on_message(message))


    # 以下現在未使用
    async def on_message_delete(self, message):
        """メッセージ削除時"""
        return
    async def on_message_edit(self, before, after):
        """メッセージ編集時"""
        return

    async def on_reaction_add(self, reaction, user):
        """リアクション追加"""
        return
    async def on_reaction_remove(self, reaction, user):
        """リアクション削除"""
        return
    async def on_reaction_clear(self, message, reaction):
        """リアクション全削除"""
        return





if __name__ == '__main__':
    # コンフィグ読み込み
    cfg = ConfigParser()
    cfg.read(CFG_FILE, 'UTF-8')
    dis = Kuritchi(cfg)
    dis.run(cfg["Discord"]["token"])