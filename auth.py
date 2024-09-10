import streamlit as st
import streamlit_authenticator as stauth
import os

def load_config():
    config = {
        'credentials': {
            'usernames': {
                username: {
                    'name': name,
                    'password': password
                } for username, name, password in zip(
                    st.secrets.credentials.usernames,
                    st.secrets.credentials.names,
                    st.secrets.credentials.passwords
                )
            }
        },
        'cookie': {
            'expiry_days': st.secrets.cookie.expiry_days,
            'key': st.secrets.cookie.cookie_key,
            'name': st.secrets.cookie.cookie_name
        },
        'preauthorized': {
            'emails': st.secrets.get('pre-authorized', {}).get('emails', [])
        }
    }
    return config

config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']['emails']
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