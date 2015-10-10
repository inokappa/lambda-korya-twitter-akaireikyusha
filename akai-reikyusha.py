#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys, json, urllib2, random, re
import ConfigParser
import BeautifulSoup
import twitter

if __name__ == "__main__":

    # config.ini から Twitter API の Credential 情報を取得
    c = ConfigParser.SafeConfigParser()
    c.read("./config.ini")

    # Twitter API を初期化
    api = twitter.Api(
        consumer_key        = c.get('tw','consumer_key'),
        consumer_secret     = c.get('tw','consumer_secret'),
        access_token_key    = c.get('tw','access_token_key'),
        access_token_secret = c.get('tw','access_token_secret'),
        )
    
    # wikipedia API から赤い霊柩車シリーズの情報を取得する(JSON 形式/コンテンツは HTML フォーマットで取得する)
    url = "https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=query&prop=revisions&titles=%E8%B5%A4%E3%81%84%E9%9C%8A%E6%9F%A9%E8%BB%8A%E3%82%B7%E3%83%AA%E3%83%BC%E3%82%BA&rvprop=content&rvparse"

    # API より JSON データを取得
    htmldata = urllib2.urlopen(url)
    # JSON を解析
    j = json.loads(htmldata.read())
    # JSON を解析して HTML のみ抽出
    query = j['query']['pages']['183090']['revisions'][0]['*']
    # HTML を解析
    soup = BeautifulSoup.BeautifulSoup(query)
    # リストの初期化
    episode = []
    # 作品名の取得 .+ => 一文字以上の文字に一致
    for i in soup.findAll(text=re.compile(u"^\ 第.+」$")):
        # strip() 前後の空白を削除
    	episode.append(i.strip())
	
    # ランダムに作品名と放映日時を出力
    print u"赤い霊柩車シリーズ: " + random.choice(episode)
    print api.PostUpdate(u"赤い霊柩車シリーズ: " + random.choice(episode)) 
