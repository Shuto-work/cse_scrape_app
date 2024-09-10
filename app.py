import streamlit as st
from content import content_page
from auth import authenticator, save_config

def login_page():
    # セッションステートの初期化
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None

    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        st.write(f'Welcome *{name}*')
        content_page()
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

def register_page():
    st.subheader("新規登録")
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
            save_config()
    except Exception as e:
        st.error(e)

def main():
    if st.session_state.get('authentication_status'):
        content_page()  # ログイン後はコンテンツページを表示
    else:
        login_page()
        register_page()

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
