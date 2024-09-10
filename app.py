import streamlit as st
from content import content_page
from auth import authenticator, config, save_config

def initialize_session_state():
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'name' not in st.session_state:
        st.session_state['name'] = None

def login_page():
    authenticator.login(key='login_widget')
    
    if st.session_state['authentication_status']:
        st.rerun()  # ログイン後は自動的にページをリロードして新しい内容を表示

def register_page():
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            pre_authorization=False,
            key='register_widget'
        )
        
        if email_of_registered_user:
            st.success('User registered successfully')
            save_config()
            st.experimental_rerun()  # 新規登録後にページをリロードしてログインページを表示

    except Exception as e:
        st.error(f'エラー: {e}')
        save_config()

def main():
    initialize_session_state()
    
    if st.session_state['authentication_status']:
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
