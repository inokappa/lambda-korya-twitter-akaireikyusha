#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os, sys, json, urllib2, random, re, httplib2, shutil
import ConfigParser
import BeautifulSoup
import twitter
from requests_oauthlib import OAuth1Session

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

# 参考：http://qiita.com/tukiyo3/items/96724a3ae7c90d3ae387
def get_img_urls(search_word, n):
    img_url=[]
    # 取得する画像 URL の数を指定
    images_per_request=8
    # https://developers.google.com/image-search/v1/jsondevguide
    url = "http://ajax.googleapis.com/ajax/services/search/images?q=%e8%b5%a4%e3%81%84%e9%9c%8a%e6%9f%a9%e8%bb%8a&v=1.0&imgsz=huge&rsz="+str(images_per_request)+"&start={0}"
    urlencoded = urllib2.quote(search_word)
    # search_word と一致する画像 URL を 8 個取得
    for i in range(n):
    	res = urllib2.urlopen(url.format(i*images_per_request))
    	data = json.load(res)
    	img_url += [result["url"] for result in data["responseData"]["results"]]
    # ランダムに 1 つの URL を返す
    return random.choice(img_url)

def download_img(url):
    opener = urllib2.build_opener()
    http = httplib2.Http(".cache")
    response, content = http.request(url)
    with open('image_file', 'wb') as f:
    	f.write(content)
    if os.path.exists('/tmp/image_file'):
    	os.remove('/tmp/image_file')
    shutil.move('image_file', '/tmp/')

# 参考：http://qiita.com/yubais/items/864eedc8dccd7adaea5d
# def upload_img():
 
def reikyusha():
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

    return random.choice(episode)

if __name__ == "__main__":
    # 赤い霊柩車シリーズの画像 URL を取得
    image_url = get_img_urls("赤い霊柩車", 3)
    print image_url
    download_img(image_url)
    # ランダムに作品名と放映日時を出力
    # episode = reikyusha()
    # print u"赤い霊柩車シリーズ: " + episode + image_url
    # print api.PostUpdate(u"赤い霊柩車シリーズ: " + episode + image_url) 
