import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader

# 設定 API 金鑰
API_KEY = "AQ.Ab8RN6J659uJkjOnk7VlP-04NiZwPu7SQrjoEgM8gIjJdh6o7Q"

# 強制清除可能衝突的環境變數
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

def get_pdf_text(pdf_file):
    """讀取並提取 PDF 文字內容"""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def analyze_pdf_with_gemini(pdf_text, question):
    """使用 Gemini 3.5 分析提取出的文字"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=API_KEY,
        temperature=0.3
    )
    
    prompt = f"請閱讀以下 PDF 內容並回答問題：\n\n內容：{pdf_text[:10000]}...\n\n問題：{question}"
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"發生錯誤: {str(e)}"

# Streamlit 介面
st.title("Gemini 3.5 PDF 分析助手")

uploaded_file = st.file_uploader("請上傳一個 PDF 檔案", type=["pdf"])
user_question = st.text_input("你想對這個 PDF 問什麼？")

if st.button("開始分析"):
    if not uploaded_file:
        st.warning("請先上傳 PDF 檔案")
    elif not user_question:
        st.warning("請輸入問題")
    else:
        with st.spinner("正在提取 PDF 內容並交給 Gemini 分析..."):
            # 1. 提取文字
            raw_text = get_pdf_text(uploaded_file)
            
            # 2. 呼叫 Gemini
            result = analyze_pdf_with_gemini(raw_text, user_question)
            
            st.subheader("分析結果")
            st.write(result)
