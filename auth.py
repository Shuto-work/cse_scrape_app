import streamlit_authenticator as stauth
import streamlit as st
import os
import yaml
from yaml.loader import SafeLoader


def load_config():
    if os.path.exists('./.streamlit/config.yaml'):
        # ローカル環境
        with open('./.streamlit/config.yaml') as file:
            return yaml.load(file, Loader=SafeLoader)
    else:
        # デプロイ環境 (Streamlit Secrets を使用)
        auth_config = st.secrets.get("authentication", {})
        return {
            'credentials': {
                'usernames': {
                    username: {
                        'name': name,
                        'password': password
                    } for username, name, password in zip(
                        auth_config.get("usernames", []),
                        auth_config.get("names", []),
                        auth_config.get("passwords", [])
                    )
                }
            },
            'cookie': {
                'expiry_days': auth_config.get("cookie_expiry_days", 30),
                'key': auth_config.get("cookie_key", "some_signature_key"),
                'name': auth_config.get("cookie_name", "some_cookie_name")
            },
            'pre-authorized': {
                'pre-authorized': auth_config.get("pre_authorized", [])
            }
        }

config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def save_config():
    if os.path.exists('./.streamlit/config.yaml'):
        # ローカル環境
        with open('./.streamlit/config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        st.success("設定が正常に保存されました。")
    else:
        # デプロイ環境
        st.warning("デプロイ環境では設定の自動更新はできません。管理者に連絡して手動で更新してください。")
