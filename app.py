import streamlit as st
from google import genai
from google.genai import types  # 引入型別定義，解決 ValidationError
from PIL import Image

# ---------------- 設定網頁基本資訊 ----------------
st.set_page_config(page_title="大聯盟英語特訓營", page_icon="⚾")

if 'points' not in st.session_state:
    st.session_state.points = 0

# ---------------- 側邊欄 ----------------
with st.sidebar:
    st.title("⚾ 教練辦公室")
    api_key = st.text_input("請輸入 API Key:", type="password")
    st.divider()
    st.metric(label="🏆 目前累積點數", value=f"{st.session_state.points} 點")

st.title("大聯盟英語特訓營")

if not api_key:
    st.warning("請先輸入金鑰啟動教練！")
else:
    client = genai.Client(api_key=api_key)
    CURRENT_MODEL = "gemini-1.5-flash"

    tab1, tab2, tab3 = st.tabs(["📸 情蒐 (擷取)", "🎤 揮棒 (跟讀)", "📝 守備 (文法)"])

    # --- 第一局：擷取單字 ---
    with tab1:
        st.header("📸 第一局：上傳教材照片")
        uploaded_image = st.file_uploader("上傳照片", type=["jpg", "png", "jpeg"])
        
        if uploaded_image:
            st.image(uploaded_image, use_container_width=True)
            
            if st.button("請教練分析敵情"):
                with st.spinner("教練正在解讀暗號..."):
                    # 使用 types.Part 來包裝，確保通過 Pydantic 驗證
                    image_part = types.Part.from_bytes(
                        data=uploaded_image.getvalue(),
                        mime_type=uploaded_image.type
                    )
                    
                    response = client.models.generate_content(
                        model=CURRENT_MODEL,
                        contents=[
                            "你是一位熱血的棒球英語教練。請從圖中找出 3 到 5 個單字，列出英中解釋與例句。",
                            image_part
                        ]
                    )
                    st.success("分析完成！")
                    st.write(response.text)

    # --- 第二局：語音跟讀 ---
    with tab2:
        st.header("🎤 第二局：揮棒練習")
        audio_file = st.file_uploader("上傳跟讀錄音", type=["mp3", "m4a", "wav"])
        
        if st.button("⚾ 提交錄音！"):
            if audio_file:
                with st.spinner("裁判正在觀看重播..."):
                    # 語音部分同樣使用 types.Part 包裝
                    audio_part = types.Part.from_bytes(
                        data=audio_file.getvalue(),
                        mime_type=audio_file.type
                    )
                    
                    response = client.models.generate_content(
                        model=CURRENT_MODEL,
                        contents=[
                            "你是一位棒球教練。請聽這段跟讀音檔，給予 0-100 評分並指出發音優缺點。",
                            audio_part
                        ]
                    )
                    st.write(response.text)
                    st.session_state.points += 50
            else:
                st.error("請先上傳錄音檔！")

    with tab3:
        st.header("📝 第三局：戰術重組")
        st.info("[ baseball / is / playing / fun / very ]")
        ans = st.text_input("輸入答案：")
        if st.button("傳球！"):
            if ans.lower().strip() == "playing baseball is very fun":
                st.balloons()
                st.session_state.points += 50
                st.success("完美雙殺！獲得 50 點！")
