import streamlit as st
import pyrebase
from firebase_config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

st.set_page_config(page_title="School Notice Board", page_icon="📚")

# 로그인 상태 유지
def login_session(email):
    st.session_state["email"] = email

def is_logged_in():
    return "email" in st.session_state

# 로그인 화면
def login():
    st.title("📚 School Notice Board")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            login_session(email)
            st.success("Logged in!")
            st.rerun()
        except:
            st.error("Failed to login")

    if st.button("Sign Up"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("Account created! Try login!")
        except:
            st.error("Failed to sign up")


# 공지 사항 페이지
def notice_page():
    st.header("📢 Class Notices")

    grade = st.selectbox("Grade", ["1", "2", "3"])
    classroom = st.selectbox("Class", [str(i) for i in range(1, 13)])

    key = f"{grade}-{classroom}"

    st.subheader("📌 Add New Notice")
    text = st.text_area("Notice Content")

    if st.button("Submit Notice"):
        data = {
            "user": st.session_state["email"],
            "text": text
        }
        db.child("notices").child(key).push(data)
        st.success("Uploaded!")

    st.subheader("📄 Notices List")
    notices = db.child("notices").child(key).get().val()

    if notices:
        for n in notices.values():
            st.write(f"📌 {n['text']}   — ✍ {n['user']}")
    else:
        st.info("No notices yet.")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()


# 앱 실행
if not is_logged_in():
    login()
else:
    notice_page()
