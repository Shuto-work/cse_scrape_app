import streamlit as st
import streamlit_authenticator as stauth

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

# セッションステートの初期化
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'logout' not in st.session_state:
    st.session_state['logout'] = False