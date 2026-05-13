import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

# ---------------- 設定網頁基本資訊 ----------------
st.set_page_config(page_title="大聯盟英語特訓營", page_icon="⚾", layout="centered")

# 初始化計分板
if 'points' not in st.session_state:
    st.session_state.points = 0

# ---------------- 側邊欄：教練辦公室 ----------------
with st.sidebar:
    st.title("⚾ 教練辦公室")
    api_key = st.text_input("請輸入大腦金鑰 (API Key):", type="password")
    st.divider()
    st.metric(label="🏆 目前累積點數", value=f"{st.session_state.points} 點")

st.title("大聯盟英語特訓營")

# ---------------- 檢查金鑰並啟動 AI ----------------
if not api_key:
    st.warning("教練還沒睡醒！請先在左側輸入 API Key 啟動系統。")
else:
    # 2026 最新設定：使用 v1beta 搭配最新 Alias
    try:
        client = genai.Client(
            api_key=api_key, 
            http_options={'api_version': 'v1beta'}
        )
        # 自動指向您清單中 2026 最新的 Flash 模型 (如 Gemini 3.1 Flash-Lite)
        CURRENT_MODEL = "gemini-flash-latest" 

        tab1, tab2, tab3 = st.tabs(["📸 第一局: 情蒐 (擷取)", "🎤 第二局: 揮棒 (跟讀)", "📝 第三局: 守備 (文法)"])

        # --- 第一局：擷取單字 ---
        with tab1:
            st.header("📸 第一局：上傳教材照片")
            uploaded_image = st.file_uploader("上傳照片", type=["jpg", "png", "jpeg"])
            
            if uploaded_image:
                st.image(uploaded_image, use_container_width=True)
                
                if st.button("請教練分析敵情"):
                    with st.spinner("教練正在解讀暗號..."):
                        # 使用正式型別 Part.from_bytes 確保通過驗證
                        image_part = types.Part.from_bytes(
                            data=uploaded_image.getvalue(),
                            mime_type=uploaded_image.type
                        )
                        
                        response = client.models.generate_content(
                            model=CURRENT_MODEL,
                            contents=["你是一位熱血的棒球英語教練。請從這張圖中找出 3 到 5 個英文單字，列出英中解釋與例句。請用棒球教練的口吻給予鼓勵！", image_part]
                        )
                        st.success("分析完成！")
                        st.write(response.text)

        # --- 第二局：語音跟讀 ---
        with tab2:
            st.header("🎤 第二局：揮棒練習 (Shadowing)")
            audio_file = st.file_uploader("上傳你的錄音檔 (mp3/m4a/wav)", type=["mp3", "m4a", "wav"])
            
            if st.button("⚾ 提交錄音！"):
                if audio_file:
                    with st.spinner("裁判正在觀看重播 (分析發音中)..."):
                        audio_part = types.Part.from_bytes(
                            data=audio_file.getvalue(),
                            mime_type=audio_file.type
                        )
                        
                        response = client.models.generate_content(
                            model=CURRENT_MODEL,
                            contents=["你是一位大聯盟棒球教練。請聽這段英文跟讀，給予 0-100 的流暢度評分，並用棒球術語給予評價。", audio_part]
                        )
                        st.write(response.text)
                        st.session_state.points += 50
                        st.success("順利上壘！獲得 50 點訓練點數！")
                else:
                    st.error("球還沒投出來！請先上傳錄音檔。")

        # --- 第三局：文法測驗 ---
        with tab3:
            st.header("📝 第三局：戰術重組 (句型)")
            st.info("[ baseball / is / playing / fun / very ]")
            ans = st.text_input("請輸入你的答案：")
            
            if st.button("傳球！"):
                if ans.lower().strip() == "playing baseball is very fun":
                    st.balloons()
                    st.success("紅中好球！獲得 50 點！")
                    st.session_state.points += 50
                else:
                    st.warning("投偏了喔，檢查一下順序再投一次！")

    except Exception as e:
        st.error(f"系統連接異常，請確認 API Key 權限：{str(e)}")
