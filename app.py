import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
import os

st.set_page_config(page_title="ClassBoard", page_icon="📚")

# Firebase 설정
if not os.path.exists("serviceAccount.json"):
    st.error("🚨 Firebase 서비스 계정 파일이 없습니다.")
else:
    try:
        cred = credentials.Certificate("serviceAccount.json")
        initialize_app(cred)
    except:
        pass
    db = firestore.client()

    st.title("📚 ClassBoard")
    st.write("반 공지/과제 공유 플랫폼!")

    title = st.text_input("공지 제목")
    content = st.text_area("내용")

    if st.button("등록"):
        if title and content:
            db.collection("notices").add({
                "title": title,
                "content": content
            })
            st.success("등록 완료!")

    st.subheader("📌 등록된 공지")
    notices = db.collection("notices").stream()
    for n in notices:
        st.write(f"**{n.to_dict()['title']}**")
        st.write(n.to_dict()['content'])
        st.markdown("---")
