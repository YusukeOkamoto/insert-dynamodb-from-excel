import sys
import pandas as pd
import json

# コマンドライン引数からテーブル名とExcelファイル名を取得する
table_name = sys.argv[1]
excel_file = sys.argv[2]

# Excelファイルを読み込む
df = pd.read_excel(excel_file)

# レコードをリストに変換する
records = df.to_dict('records')

# リクエストアイテムのリストを生成する
request_items = []
for record in records:
    item = {}
    for key, value in record.items():
        if pd.isna(value):
            item[key] = {"NULL": True}
        elif key == 'id': # 'id'キーの場合、型をstringに変更
            item[key] = {"S": str(value)}
        elif isinstance(value, int):
            item[key] = {"N": str(value)}
        else:
            item[key] = {"S": str(value)}
    request_items.append({"PutRequest": {"Item": item}})


# DynamoDB BatchWriteItem APIで使用できる形式に変換する
request = {table_name: request_items}

# 最大書き込み件数に合わせて複数のリクエストに分割する
max_items_per_request = 25
request_list = [request[list(request.keys())[0]][i:i + max_items_per_request] for i in range(0, len(request[table_name]), max_items_per_request)]

# JSONファイルに出力する
for i, r in enumerate(request_list):
    with open(f'output_{i}.json', 'w', encoding='utf-8') as f:
        json.dump({"RequestItems": {table_name: r}}, f, ensure_ascii=False)
