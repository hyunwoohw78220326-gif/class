import streamlit as st
from firebase_admin import credentials, firestore, initialize_app

st.set_page_config(page_title="ClassBoard", page_icon="📚")

# Firebase 초기화
try:
    initialize_app()
except:
    pass
db = firestore.client()

st.title("📚 ClassBoard")
st.write("반 공지/과제 공유 플랫폼!")

# 입력창
title = st.text_input("공지 제목")
content = st.text_area("내용")

if st.button("등록"):
    if title and content:
        db.collection("notices").add({
            "title": title,
            "content": content
        })
        st.success("등록 완료!")
    else:
        st.error("빈칸 없이 입력하세요!")

st.subheader("📌 등록된 공지")
notices = db.collection("notices").stream()
for n in notices:
    data = n.to_dict()
    st.write(f"**{data['title']}**")
    st.write(data['content'])
    st.markdown("---")
