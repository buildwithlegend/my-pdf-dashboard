import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from PyPDF2 import PdfReader

# 1. 頁面配置
st.set_page_config(page_title="PDF 智慧閱讀與自動化 Dashboard", layout="wide")
st.title("📊 PDF 智慧閱讀與自動化儀表板")

# 2. 安全讀取 API Key (部署時透過 Streamlit Secrets 設定)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("輸入 Gemini API Key", type="password")

# 3. 側邊欄：檔案上傳
with st.sidebar:
    st.header("文件設定")
    uploaded_file = st.file_uploader("上傳您的 PDF 檔案", type="pdf")

# 4. 主介面邏輯
col1, col2 = st.columns([1, 1])

if uploaded_file and api_key:
    # 讀取 PDF
    reader = PdfReader(uploaded_file)
    text = "".join([page.extract_text() for page in reader.pages])
    
    with col1:
        st.subheader("📄 PDF 內容預覽")
        st.text_area("文件文字", text[:2000] + "...", height=400)
        
    with col2:
        st.subheader("🤖 AI 對話與分析")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
        
        user_query = st.text_input("請輸入問題，例如：請分析這份文件的關鍵數據")
        if user_query:
            with st.spinner("AI 思考中..."):
                prompt = f"文件內容摘要：{text[:3000]}... \n\n問題：{user_query}"
                response = llm.invoke(prompt)
                st.write(response.content)
        
        # 你的「自動化計算」區域預留
        st.divider()
        st.subheader("⚙️ 自動化硬體計算 (測試)")
        if st.button("計算門片硬體規格"):
            st.info("這裡可以連結你之前的自動化公式邏輯，例如：根據上傳的 PDF 數據自動帶入 B3 值。")

elif not api_key:
    st.warning("請在側邊欄輸入 API Key 以開始使用")
else:
    st.info("請上傳 PDF 檔案以開始分析")