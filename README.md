# cit-cafe
## Description
千葉工業大学 CIT サービスが提供する現在の週の学食の献立画像を WEB サイトから取得して表示するスクリプト。

### メリット
わざわざブラウザを開いて「献立表どこだっけな〜」ってやらなくて済む。

### デメリット
画像を表示するのでそれができる環境が必要

## Preparation
- [ ] BeautifulSoup 4 のインストール
```
pip install beautifulsoup4
```
- [ ] lxml パーサーのインストール
```
pip install lxml
```
- [ ] Requests のインストール
```
pip install requests
```
- [ ] OpenCV のインストール
```
pip install opencv-python
```

<h6>他に予めインストールが必要なものがあったら教えてください...</h6>

## Instration
```
git clone htpps://github.com/yazawakenichi/cit-cafe
```

## Usuage
以下で実行可能。
```
./cit-cafe
```
### 使用可能なオプション
|オプション|説明
|---|---
|なし|津田沼の学食の画像を表示
|td|津田沼の学食の情報を表示
|sd1|新習志野の学食 1F の献立表を表示
|sd2|新習志野の学食 2F の献立表を表示
|-s *size*|画像の大きさを *size* 倍にする<br>デフォルトで 0.4

例えば、以下のようにすることで、新習志野キャンパスの学食の献立表の画像を 0.8 倍にして表示するようになる。
```
./cit-cafe sd1 -s 0.8
```


## Reference
- [How to open an image from an url with opencv using requests from python - stack overflow](https://stackoverflow.com/questions/57539233/how-to-open-an-image-from-an-url-with-opencv-using-requests-from-python)
- [OpenCV - resize で画像をリサイズする方法 - Pystyle](https://pystyle.info/opencv-resize/)
- [Python でコマンドラインを Parse しよう (OptParse) - のんびりしているエンジニアの日記](https://nonbiri-tereka.hatenablog.com/entry/2014/09/19/143728)
- [optparse - getopt に代わるコマンドラインオプションパーサ](https://ja.pymotw.com/2/optparse/)

## LICENSE

- This software may be redistributed and used in accordance with the terms of the MIT license.
- (C) 2022 Kenichi Yazawa

