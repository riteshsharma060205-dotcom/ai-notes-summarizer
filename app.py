import streamlit as st
import fitz  # PyMuPDF
from groq import Groq
import os

st.set_page_config(page_title="AI Notes Summarizer", page_icon="📚")
st.title("📚 AI Notes Summarizer")
st.write("Apni BCA ki notes ka PDF upload karo, 10 sec me summary pao!")

# Groq Free API Key - https://console.groq.com se free me milta hai
api_key = st.text_input("Groq API Key daalo (free hai)", type="password")
uploaded_file = st.file_uploader("PDF upload karo", type="pdf")

if uploaded_file and api_key:
    if st.button("Summarize Karo"):
        with st.spinner("AI padh raha hai..."):
            # PDF se text nikalna
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            
            # AI ko bhejna
            client = Groq(api_key=api_key)
            prompt = f"Is text ko BCA student ke liye summarize karo. 1. Short summary (100 words) 2. 5 Important points 3. 3 Exam Questions. Text: {full_text[:8000]}"
            
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192"
            )
            st.success("Ho gaya!")
            st.write(chat.choices[0].message.content)
else:
    st.info("API Key kaise mile? console.groq.com pe jao, free signup, key copy karke yahan paste karo.")