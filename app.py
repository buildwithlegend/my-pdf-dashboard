import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader

# 1. 頁面配置
st.set_page_config(page_title="PDF 智慧閱讀與自動化 Dashboard", layout="wide")
st.title("📊 PDF 智慧閱讀與自動化儀表板")

# 2. 已設定的 API Key
API_KEY = "AQ.Ab8RN6J659uJkjOnk7VlP-04NiZwPu7SQrjoEgM8gIjJdh6o7Q"

# 3. 側邊欄：檔案上傳
uploaded_file = st.sidebar.file_uploader("上傳您的 PDF 檔案", type="pdf")

# 4. 主介面邏輯
col1, col2 = st.columns([1, 1])

if uploaded_file:
    # 讀取 PDF
    try:
        reader = PdfReader(uploaded_file)
        text = "".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        st.error(f"讀取 PDF 失敗: {e}")
        st.stop()
    
    with col1:
        st.subheader("📄 PDF 內容預覽")
        st.text_area("文件文字", text[:2000] + "...", height=400)
        
    with col2:
        st.subheader("🤖 AI 對話與分析")
        
        try:
            # 使用已寫入的 API Key 初始化
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=API_KEY
            )
            
            user_query = st.text_input("請輸入問題")
            if user_query:
                with st.spinner("AI 思考中..."):
                    prompt = f"文件內容：{text[:3000]}... \n\n問題：{user_query}"
                    response = llm.invoke(prompt)
                    st.write(response.content)
        except Exception as e:
            st.error(f"AI 連線失敗: {str(e)}")

elif not uploaded_file:
    st.info("請上傳 PDF 檔案以開始分析")
