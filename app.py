import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader

# 1. 頁面配置
st.set_page_config(page_title="PDF 智慧閱讀與自動化 Dashboard", layout="wide")
st.title("📊 PDF 智慧閱讀與自動化儀表板")

# 2. API Key 取得邏輯
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("輸入 Gemini API Key", type="password")

# 3. 側邊欄：檔案上傳
uploaded_file = st.sidebar.file_uploader("上傳您的 PDF 檔案", type="pdf")

# 4. 主介面邏輯
col1, col2 = st.columns([1, 1])

if uploaded_file and api_key:
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
        
        # 使用 try-except 捕捉 API 錯誤
        try:
            # 針對 Google Cloud Vertex AI 金鑰的修正設定
            # 若你在其他地區(非 us-central1)，請將 location 修改為對應地區
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
                google_api_key=api_key,
                location="us-central1"
            )
            
            user_query = st.text_input("請輸入問題")
            if user_query:
                with st.spinner("AI 思考中..."):
                    prompt = f"文件內容：{text[:3000]}... \n\n問題：{user_query}"
                    response = llm.invoke(prompt)
                    st.write(response.content)
        except Exception as e:
            st.error(f"AI 連線失敗: {str(e)}")

elif not api_key:
    st.warning("請在側邊欄輸入 API Key 以開始使用")
elif not uploaded_file:
    st.info("請上傳 PDF 檔案以開始分析")
