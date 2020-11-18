# tsung-copier

Tsungの結果をマークダウン形式でクリップボードにコピーします。
Pythonのスクリプトと、chrome拡張を提供しています。

# JS

## Usage

1. `js/tsung-copier` を [拡張機能](chrome://extensions) の、 `パッケージ化されていない拡張機能を読み込む` から読み込みます。

2. Tsungの測定結果を表示するreport.htmlにブラウザでアクセスすると、copyボタンがページ下部に追加されます。そのボタンをクリックすれば、表示しているページ中のテーブルをマークダウン形式に変換し、クリップボードにコピーします。

# Python

## Requirements

- python >= 3.8
- requests
- beautifulsoup4

## Usage

1. Tsungの測定結果を表示するreport.htmlのurlを取得しておきます。

2. 以下のコマンドを実行すると、標準出力に、マークダウン形式で出力されるので、パイプでpbcopyに渡せばクリップボードにコピーできます。 `-w` は、リクエストの成功率を計算するかどうかのフラグで、指定した場合、全リクエストに対する、ステータスコードが2XXのリクエスト数を計算します。

```shell
python tsung.py -w -u http://localshot:8000/report.html | pbcopy
```
