import streamlit as st
import streamlit_authenticator as stauth
import os
import yaml
from yaml.loader import SafeLoader
from content import content_page


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
                'emails': auth_config.get("pre_authorized_emails", [])
            }
        }

config = load_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']['emails']
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


def main():
    
    authenticator.login()

    if st.session_state['authentication_status']:
        content_page()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

if __name__ == "__main__":
    main()



# import streamlit as st
# from content import content_page
# from auth import authenticator, config, save_config


# def login_page():
#     authenticator.login()

#     if st.session_state['authentication_status']:
#         content_page()
#     elif st.session_state['authentication_status'] is False:
#         st.error('Username/password is incorrect')
#     elif st.session_state['authentication_status'] is None:
#         st.warning('Please enter your username and password')


# def register_page():
#     st.subheader("新規登録")
#     try:
#         email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
#             pre_authorization=False)
#         if email_of_registered_user:
#             st.success('User registered successfully')
#             save_config()
#             st.button('ログインページに戻る',onclick=login_page)
#     except Exception as e:
#         st.error(e)
#         save_config()

# if __name__ == "__main__":
#     if 'authentication_status' in st.session_state and st.session_state['authentication_status']:
#         login_page()
#     else:
#         register_page()
