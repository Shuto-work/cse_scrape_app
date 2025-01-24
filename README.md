# README Japanese
## Streamlitを使ったカスタム検索APIスクレイピング
Googleカスタム検索エンジンの検索結果から、電話番号と会社名のデータを取得できます。スクレイピング結果はCSVファイルとしてダウンロードできます。
GUIにはStreamlitを使用しており、Google Custom Search Engine（CSE）APIと連携しています。
CSVファイルが文字化けしている場合、[こちらのツール](<https://www.gas-laboratory.com/courses/take/csv-char-code-converter/texts/43893072-csv>)で変換可能です。

### What is Streamlit !?
PythonのGUIライブラリです。

https://docs.streamlit.io/

## 主な機能
検索機能: カスタムキーワードを使用してGoogle CSEから結果を取得します。
ページネーション: 取得する検索結果のページを指定できます。
並べ替え順序: 関連順または日付順から選択できます。
CSV出力: 検索結果をCSVファイルとしてエクスポートします。

## インストール
### 1, リポジトリをクローンする
```bash
git clone <repository-url>
```
### 2, 依存関係のインストール
```bash
pip install -r requirements.txt
```

## 設定
.streamlitフォルダーを作成。その中にsecrets.tomlファイルを作成。APIキー、CSE ID、ユーザー認証などを設定。この内容をsecretsに添付、
```toml
api_key = "YOUR_API_KEY"
cse_id = "YOUR_CSE_ID"

[authentication]
usernames = ["YOUR_USER_NAME"]
name = ["YOUR_NAME"]
passwords = [
	"YOUR_ PASSWORD", # hash_passwords.pyを実行して生成される、ハッシュ化されたパスワード
]

cookie_name = "some_cookie_name"
cookie_key = "some_cookie_key"
cookie_expiry_days = 30
pre_authorized_emails = ["some@gmail.com"]
```

### secretsについては公式ドキュメントを確認
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

### CSE_ID & API_keyの取得方法
https://www.system-exe.co.jp/kotohajime15/

### CSE
https://programmablesearchengine.google.com/intl/ja_jp/about/

## Usage
### 1, Streamlit appを起動。
```bash
streamlit run app.py
```
### 2, 検索パラメータを入力
- 検索キーワード: 検索したい用語やフレーズ。
- 開始ページ: 検索結果を取得し始めるページ番号。
- 終了ページ: 検索結果を取得し終わるページ番号。
  ※CSEの仕様上、取得範囲は1〜10ページ目です。
- 検索結果の表示順:「関連順」または「日付順」を選択。
- CSVファイル名:保存するCSVファイルの名前。
### 3, 検索が完了したらCSVファイルをダウンロード。

# README Englidh
## Custom Search API Scraping with Streamlit
This project provides a web interface using Streamlit for interacting with the Google Custom Search Engine (CSE) API. Users can input search queries and retrieve a list of phone numbers and company names from the search results, which are then output as a CSV file.

### What is Streamlit !?
It is Python library
https://docs.streamlit.io/

## Features
Search Functionality: Search using custom keywords and retrieve results from Google CSE.
Pagination: Specify which pages of search results to retrieve.
Sort Order: Choose between relevance-based and date-based sorting.
CSV Output: Export search results to a CSV file.

## Installation
Clone the repository:
```bash
git clone <repository-url>
```
## Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Create a secrets.toml file with your API key and CSE ID:
```toml
api_key = "YOUR_API_KEY"
cse_id = "YOUR_CSE_ID"
```

### How to get CSE_ID & API_key
For Japanese
https://www.system-exe.co.jp/kotohajime15/

### CSE
https://programmablesearchengine.google.com/intl/ja_jp/about/

## Usage
### 1, Run the Streamlit app:
```bash
streamlit run app.py
```
### 2, Input your search parameters:
- Search Keyword: The term you want to search for.
- Start Page: The starting page number for search results.
- End Page: The ending page number for search results.
- Sort Order: Choose between "Relevance" and "date".
- CSV Filename: The name of the output CSV file.
- Download the CSV file once the search is complete.
### 3, Download the CSV File 
Download the CSV File once the search is complete.
