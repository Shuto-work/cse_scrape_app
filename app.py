import streamlit as st
import streamlit_authenticator as stauth
import yaml
import json
import subprocess
import sys
from yaml.loader import SafeLoader
import os

def save_config():
    with open('./.streamlit/config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    st.success("設定が正常に保存されました。")


def load_config():
    if os.path.exists('config.yaml'):
        # ローカル環境
        with open('config.yaml') as file:
            return yaml.load(file, Loader=SafeLoader)
    else:
        # デプロイ環境 (Streamlit Secrets を使用)
        return {
            'credentials': {
                'usernames': {
                    username: {
                        'name': name,
                        'password': password
                    } for username, name, password in zip(
                        st.secrets["credentials"]["usernames"],
                        st.secrets["credentials"]["names"],
                        st.secrets["credentials"]["passwords"]
                    )
                }
            },
            'cookie': {
                'expiry_days': st.secrets["cookie"]["expiry_days"],
                'key': st.secrets["cookie"]["cookie_key"],
                'name': st.secrets["cookie"]["cookie_name"]
            },
            'pre-authorized': {
                'emails': st.secrets.get("pre-authorized", {}).get("emails", [])
            }
        }

# 設定を読み込む
config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

print(config)

def login_and_register_page():

    # Check if user is already logged in
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None

    if st.session_state['authentication_status']:
        content_page()
        return

    st.title("ログイン")
    name, authentication_status, username = authenticator.login()

    if authentication_status:
        st.session_state["name"] = name
        st.session_state['authentication_status'] = True
        st.rerun()  # Using st.rerun() instead of st.experimental_rerun()
    elif authentication_status == False:
        st.error('ユーザー名/パスワードが間違っています')
    elif authentication_status == None:
        st.warning('ユーザー名とパスワードを入力してください')

    # Registration section
    # st.write("---")
    # st.subheader("新規登録")
    # try:
    #     if authenticator.register_user(pre_authorization=False):
    #         st.success('ユーザー登録が完了しました')
    #         save_config()
    # except Exception as e:
    #     st.error(f"登録エラー: {str(e)}")


def content_page():
    st.title('Custom Search APIテスト')
    st.write(f'ようこそ *{st.session_state["name"]}* さん')

    if authenticator.logout():
        st.session_state['authentication_status'] = None
        st.success('ログアウトしました')
        st.rerun()  # Using st.rerun() instead of st.experimental_rerun()

    st.caption('検索キーワードを入力すると、検索結果から電話番号と社名のリストを取得できます')

    with st.form(key="key_word_form"):
        key_word = st.text_input("検索キーワード")
        search_start_page = st.number_input(
            "データ取得開始ページ", step=1, value=1, min_value=1, max_value=10)
        search_end_page = st.number_input(
            "データ取得終了ページ", step=1, value=1, min_value=1, max_value=1)
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
            result = subprocess.run([python_path, 'cse_scraper.py'],
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

    # ダウンロードボタンをフォーム外に配置
    if 'csv_data' in st.session_state:
        st.download_button(
            label="CSVファイルをダウンロード",
            data=st.session_state.csv_data,
            file_name=st.session_state.csv_file_name,
            mime="text/csv"
        )


if __name__ == "__main__":
    login_and_register_page()