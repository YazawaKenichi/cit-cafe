#!/usr/bin/env python3
# coding:utf-8
# SPDX-FileCopyrightText: YAZAWA Kenichi (2022)
# SPDX-License-Identifier: MIT License

# urllib は標準で用意されている
# そのうちの request の利用
import urllib
from urllib import request
from optparse import OptionParser
import requests
# pip install chardet
import chardet
from bs4 import BeautifulSoup
# バイト型を画像型に変換するのに使用する
import base64
import numpy as np
import cv2
import time
import sys

DOMAIN = 'https://cit-s.com/'
ARTICLE = 'dining/'
ADDRESS = DOMAIN + ARTICLE
ANCHOR_CLASS = "c-table__image-link"

# アドレスの BeautifulSoup を返す
def get_soup(address, ui = True):
    try:
        # レスポンスの情報を管理するオブジェクトを返す
        # このオブジェクトからメソッドを呼び出して必要な情報を取り出す
        with request.urlopen(address) as response:
            time.sleep(0.5)
            # 取得した文字列をまとめて取り出す
            body = response.read()
            if ui:
                print("[open] " + address)
            try:
                # 文字コードの取得
                cs = chardet.detect(body)   # example) cs = {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
                data = body.decode(cs['encoding'])
                # BeautifulSoup オブジェクトの作成
                soup = BeautifulSoup(data, 'lxml')
                return soup
            except UnicodeDecodeError:
                data = body
                # BeautifulSoup オブジェクトの作成
                soup = BeautifulSoup(data, 'lxml')
                return soup
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui :
            print("\x1b[31m" + address + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        # 取得できなかったときは再帰
        get_soup(address, ui)

# <a class="anchor_class"> <img src="***"> </a> の *** の部分をリスト化して取り出す
def get_image_urls(soup, anchor_class, ui = True):
    anchors = soup.find_all(class_ = anchor_class)
    hrefs = []
    for anchor in anchors:
        img = anchor.find('img')
        hrefs.append(str(img['src']))
        if ui:
            print("[append] " + str(img['src']))
    return hrefs

# 食堂の場所を指定するとインデックスを返す
def place2index(string):
    res = -1
    if string == "td":
        res = 0
    if string == "sd1":
        res = 1
    if string == "sd2":
        res = 2
    # もし res が -1 のままで書き換わっていなかったら
    if res == -1:
        print("存在しないインデックス", file = sys.stderr)
        sys.exit(1)
    return int(res)

# url の画像を表示する
def show_image(url : str, title : str, scaling = 0.4, ui = True):
    try:
        with requests.get(url, stream = True).raw as resp:
            time.sleep(0.5)
            image = np.asarray(bytearray(resp.read()), dtype = "uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            rescale_size = scaling
            image = cv2.resize(image, dsize = None, fx = rescale_size, fy = rescale_size)
            cv2.imshow(title, image)
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        if ui:
            print("\x1b[31m" + url + " : Time Out!" + "\x1b[0m", file = sys.stderr)
        time.sleep(0.5)
        # 取得できなかったときは再帰
        show_image(url, title, ui)

# 引数の中に td sd1 sd2 がある時対応するインデックスを返す
def get_placename(args):
    res = "None"
    if "td" in args:
        res = "td"
    if "sd1" in args:
        res = "sd1"
    if "sd2" in args:
        res = "sd2"
    if len(args) == 0:
        res = "td"
    if res == "None":
        print("[error] 存在しない引数", file = sys.stderr)
        sys.exit(1)
    return res

# 引数を解析する
def get_args(ui = True):
    parser = OptionParser()

    # -s オプションで表示画像のサイズを指定できるようにする
    parser.add_option(
            "-s", "--scaling",
            default = "0.4",
            type = "float",
            dest = "scaling"
            )

    if ui:
        optdict, args = parser.parse_args()
        print(optdict)
    return parser.parse_args()

if __name__ == '__main__':
    address = ADDRESS
    soup = get_soup(address)
    image_urls = get_image_urls(soup, ANCHOR_CLASS)
    # コマンドライン引数を解析する
    optiondict, args = get_args()
    scaling = optiondict.scaling
    # 場所の名前を返す
    placename = get_placename(args)
    place_index = place2index(placename)
    url = image_urls[place_index]
    # url の画像を表示する ウィンドウ名は placename
    show_image(url, placename, scaling)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


