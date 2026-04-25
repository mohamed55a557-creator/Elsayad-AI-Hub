import streamlit as st
import requests
import json

st.set_page_config(page_title="El-Sayyad AI", page_icon="🏹")
st.title("🏹 El-Sayyad Chat Hub")

# المتغيرات الأساسية
API_KEY = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال السؤال
if prompt := st.chat_input("اسأل الصياد..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        # هنا بنختار الموديل المجاني من OpenRouter
        data = {
            "model": "google/gemma-4-31b-it:free", 
            "messages": st.session_state.messages
        }
        
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"خطأ في الاتصال: {response.status_code}")
