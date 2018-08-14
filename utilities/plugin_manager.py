# -*- coding: utf-8 -*-


from .plugin import Plugin
#from plugin.temp import Temp testプラグイン
from plugin._ticker import Ticker

class PluginManager:
    
    def __init__(self, client):
        self.client = client
        self.client.plugins = []

    def plugin_load(self,plugin):
        """
        Action:
            プラグインを個別にインスタンス生成
            Kuritchi.pluginsリストに追加
        """
        #print(f"{plugin.display_name} プラグイン読み込み中...")
        instance = plugin(self.client)
        self.client.plugins.append(instance)
        print(f"{plugin.display_name} プラグイン読み込み完了...")

    def load_all(self):
        """プラグインを全て読み込み"""
        for plugin in Plugin.plugins:
            self.plugin_load(plugin)

