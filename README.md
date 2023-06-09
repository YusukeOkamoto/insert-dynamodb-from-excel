# 概要

Excelの表をAWS DynamoDBにインサートするためのjsonファイルに変換するスクリプトです

# Excelの形式

1シート目に表を作成してください
また、1行目には列名を記載してください

# 注意事項

パーティションキーがidという列名でかつ型がstring型という前提になっています。
適宜変更をお願いします。

対応している型は以下の通り

- number
- string
- boolean
- List<string>

配列にしたい場合は、一つのセルに `要素1, 要素2` のようにカンマ区切りで入力してください

# インストール

python, pip

```
pip3 install openpyxl
pip3 install pandas
```

## 実行方法

1度に25件までしか一括挿入できないため、25レコード以上ある場合はファイルが分割されます。

```
$ python convert_excel_to_dynamodb_batchwriteitem.py [Inser先のDynamoDBテーブル名] [Excelファイル名]
```

ex.(ルートディレクトリにある `example.xlsx` に `exampleTable` というテーブルに挿入したいデータを表形式で記載している前提

```
$ python3 convert_excel_to_dynamodb_batchwriteitem.py exampleTable example.xlsx

# output_0.json〜output_2.jsonが成果物
$ ls
README.md                                   output_0.json
convert_excel_to_dynamodb_batchwriteitem.py output_1.json
example.xlsx                                output_2.json

# DynamoDBへのInsert(出力ファイル数分行う)
$ aws dynamodb batch-write-item --cli-input-json file://output_0.json
$ aws dynamodb batch-write-item --cli-input-json file://output_1.json
$ aws dynamodb batch-write-item --cli-input-json file://output_2.json
```
