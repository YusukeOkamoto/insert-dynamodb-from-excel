# 概要

Excelの表をAWS DynamoDBにインサートするためのjsonファイルに変換するスクリプトです

# 注意事項

パーティションキーがidという列名でかつ型がstring型という前提になっています。
適宜変更をお願いします。

# インストール

python, pip

```
pip3 install openpyxl
pip3 install pandas
```

## 実行方法

1度に25件までしか一括挿入できないため、25レコード以上ある場合はファイルが分割されます

```
$ python convert_excel_to_dynamodb_batchwriteitem.py [Inser先のDynamoDBテーブル名] [Excelファイル名]
```

ex.

```
$ python3 convert_excel_to_dynamodb_batchwriteitem.py adminSettings example.xlsx

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
