# -*- coding: utf-8 -*-

"""
Discord Bot Plugin
Template class
"""

from utilities.plugin import Plugin
from utilities.command import command
from utilities import _requests
from operator import itemgetter
from utilities._timefunc import TimeCurrent,UnixTimeCurrent

class Ticker(Plugin):
    display_name = "価格表示"

    exchanges = dict(
    BitFlyerFX = "https://api.bitflyer.jp/v1/ticker?product_code=FX_BTC_JPY",
    BitFlyer = "https://api.bitflyer.jp/v1/ticker?product_code=BTC_JPY",
    Zaif = "https://api.zaif.jp/api/1/ticker/btc_jpy",
    CoinCheck = "https://coincheck.com/api/ticker"
    )

    another_name = {"cc":"CoinCheck","bf":"BitFlyer","bffx":"BitFlyerFX"}

    u_j = "https://www.gaitameonline.com/rateaj/getrate"
    usd_tm = 0
    usd_rate = 0
    data = []
    def _request(self, exchange):
        """リクエストを送り失敗したら0埋め"""
        try:
            j = _requests.get(self.exchanges[exchange])
        except:
            ex = [exchange,0,0,0,0,0]
        else:
            ex = self._parse(exchange,j)
        self.data.append(ex)

    def _parse(self, exchange, j):
        """取引所毎のデータ仕分け"""
        if exchange in ["Zaif","CoinCheck"]:
            price = int(j["last"])
            ask = int(j["ask"])
            bid = int(j["bid"])
            volume = j["volume"]

        elif exchange in ["BitFlyer","BitFlyerFX"]:
            price = int(j["ltp"])
            ask = int(j["best_ask"])
            bid = int(j["best_bid"])
            volume = j["volume_by_product"]
        else:
            price = ask = bid = volume = 0
        ex = [exchange,price,ask,ask-bid,bid,volume]
        return ex


    """
    以下関数
    Action:
        メッセージチェック & 処理
    Prameter:
        message: discord.message
        args : list
    """
    @command(pattern="^all")
    async def all(self, message, args):
        self.main(self.exchanges)
        await self.send_data(message.channel)
        await self.client.delete_message(message)

    @command(pattern="^bf\s(.*)|^bf|^bitflyer (.*)|^bitflyer")
    async def bitflyer(self, message, args):
        exchanges = ["BitFlyer"]
        if args != []:
            exchanges = exchanges + args
        self.main(exchanges)
        await self.send_data(message.channel)
        await self.client.delete_message(message)

    @command(pattern="^bffx\s(.*)|^bffx|^bitflyerfx (.*)|^bitflyer")
    async def bitflyerfx(self, message, args):
        exchanges = ["BitFlyerFX"]
        if args != []:
            exchanges = exchanges + args
        self.main(exchanges)
        await self.send_data(message.channel)
        await self.client.delete_message(message)

    @command(pattern="^zaif\s(.*)|^zaif")
    async def zaif(self, message, args):
        exchanges = ["Zaif"]
        if args != []:
            exchanges = exchanges + args
        self.main(exchanges)
        await self.send_data(message.channel)
        await self.client.delete_message(message)
    @command(pattern="^cc\s(.*)|^cc|^coincheck\s(.*)|^coincheck")
    async def coincheck(self, message, args):
        exchanges = ["CoinCheck"]
        if args != []:
            exchanges = exchanges + args
        self.main(exchanges)
        await self.send_data(message.channel)
        await self.client.delete_message(message)

    def main(self, exchanges):
        """
        Action:
            data変数初期化
            tickerデータ取得
        Parameter: list
        
        """
        self.data = []
        for exchange in exchanges:
            if exchange in self.another_name:
                exchange = self.another_name[exchange]
            self._request(exchange)
        

    async def send_data(self,channel):
        """
        Action:
            usd_jpyレート取得
            出来高の多い順にソートし送信    
        """
        self.usd_jpy()
        header = ["Name","Last","BestAsk","Diff","BestBid","Volume"]
        mes = "```python\n"
        mes += f"USD/JPY {self.usd_rate:>6}\n"
        mes += f"{header[0]:>12}{header[1]:>10}{header[2]:>10}{header[3]:>8}{header[4]:>10}{header[5]:>12}\n"

        self.data.sort(key=itemgetter(5), reverse=True)

        for tick in self.data:
            mes += f"{tick[0]:>12}{tick[1]:>10,d}{tick[2]:>10,d}{tick[3]:>8,d}{tick[4]:>10,d}{tick[5]:>12.3f}\n"
        mes += TimeCurrent().strftime("%Y-%m-%d %H:%M:%S")
        mes += "```"
        await self.client.send_message(channel, mes)

    def usd_jpy(self):
        if self.usd_tm <= UnixTimeCurrent()-60:
            self.usd_tm = UnixTimeCurrent()
            j = _requests.get(self.u_j)
            uj = [x["ask"] for x in j["quotes"] if x["currencyPairCode"] == "USDJPY"]
            self.usd_rate = uj[0]

