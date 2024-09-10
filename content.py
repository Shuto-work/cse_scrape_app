import json
import subprocess
import sys
from auth import authenticator,config
import streamlit as st

def content_page():
    st.title('Custom Search APIテスト')
    st.write(f'ようこそ *{st.session_state["name"]}* さん')
    authenticator.logout() 
    st.caption('検索キーワードを入力すると、検索結果から電話番号と社名のリストを取得できます')
  

    with st.form(key="key_word_form"):
        key_word = st.text_input("検索キーワード")
        search_start_page = st.number_input(
            "データ取得開始ページ", step=1, value=1, min_value=1, max_value=10)
        search_end_page = st.number_input(
            "データ取得終了ページ", step=1, value=1, min_value=1, max_value=10)
        sort_order = st.selectbox(
            "検索結果の表示順序（Relevance = 関連順, date = 日付順）", ["Relevance", "date"])
        output_csv = st.text_input("出力するCSVファイル名", "CSEスクレイピングリスト.csv")
        action_btn = st.form_submit_button("実行")

        if action_btn:
            st.subheader('以下の条件で実行しています...')
            st.text(f'検索キーワード：「{key_word}」')
            st.text(f'取得開始ページ：「{search_start_page}」')
            st.text(f'取得終了ページ：「{search_end_page}」')
            st.text(f'検索結果の表示順序：「{sort_order}」')
            st.text(f'出力CSVファイル名：「{output_csv}」')

            params = {
                "key_word": key_word,
                "search_start_page": search_start_page,
                "search_end_page": search_end_page,
                "sort_order": sort_order,
                "output_csv": output_csv
            }
            with open('params.json', 'w') as f:
                json.dump(params, f)

            # Pythonのフルパスを取得
            python_path = sys.executable

            # subprocess.runを使ってスクリプトを実行。Python実行環境を明示的に指定。
            result = subprocess.run([python_path, 'scraper.py'],
                                    capture_output=True,
                                    text=True
                                    )
            # CSVデータの準備
            if result.returncode == 0:
                csv_data = result.stdout
                st.session_state.csv_data = csv_data
                st.session_state.csv_file_name = output_csv
                st.success('実行完了')
            else:
                st.error('エラーが発生しました: ' + result.stderr)

    if 'csv_data' in st.session_state:
        st.download_button(
            label="CSVファイルをダウンロード",
            data=st.session_state.csv_data,
            file_name=st.session_state.csv_file_name,
            mime="text/csv"
        )