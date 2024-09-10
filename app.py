import streamlit as st
from content import content_page
from auth import authenticator, config, save_config

def initialize_session_state():
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'name' not in st.session_state:
        st.session_state['name'] = None

def login_page():
    # 初期化処理
    initialize_session_state()
    
    authenticator.login(key='login_widget')

    # ログイン後の処理
    if st.session_state['authentication_status']:
        content_page()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

    # 新規登録フォームの表示
    st.subheader('新規登録')
    with st.form(key='register_form'):
        email = st.text_input("メールアドレス")
        username = st.text_input("ユーザー名")
        password = st.text_input("パスワード", type="password")
        repeat_password = st.text_input("パスワードを再入力", type="password")
        register_button = st.form_submit_button("登録")

        if register_button:
            if password != repeat_password:
                st.error('パスワードが一致しません')
            else:
                try:
                    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                        location='main',
                        pre_authorization=False,
                        fields={'Form name': 'Register user', 'Email': 'Email', 'Username': 'Username', 'Password': 'Password', 'Repeat password': 'Repeat password'},
                        captcha=True,
                        key='register_widget'
                    )
                    if email_of_registered_user:
                        st.success('User registered successfully')
                        save_config()
                except Exception as e:
                    st.error(f'エラー: {e}')
                    save_config()

if __name__ == "__main__":
    login_page()



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
