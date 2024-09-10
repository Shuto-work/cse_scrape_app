import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def load_config():
    # シークレットから設定を読み込む
    cookie_config = st.secrets["cookie"]
    credentials = st.secrets["credentials"]
    
    config = {
        'credentials': {
            'usernames': {
                username: {
                    'name': name,
                    'password': password
                } for username, name, password in zip(
                    credentials["usernames"],
                    credentials["names"],
                    credentials["passwords"]
                )
            }
        },
        'cookie': {
            'expiry_days': cookie_config["expiry_days"],
            'key': cookie_config["key"],
            'name': cookie_config["name"]
        }
    }
    return config

config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    None  # pre-authorized引数を削除
)

# セッションステートの初期化
if 'logout' not in st.session_state:
    st.session_state['logout'] = False

# def save_config():
#     # この関数は必要に応じて実装してください
#     pass