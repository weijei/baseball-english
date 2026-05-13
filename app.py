import streamlit as st
import google.generativeai as genai
from PIL import Image
import tempfile
import os

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
    # 設定金鑰，並指定使用能力最強的多模態模型
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    tab1, tab2, tab3 = st.tabs(["📸 第一局: 情蒐 (擷取單字)", "🎤 第二局: 揮棒 (語音跟讀)", "📝 第三局: 守備 (文法)"])

    # --- 第一局：AI 讀取雜誌照片 ---
    with tab1:
        st.header("📸 第一局：上傳今日教材")
        uploaded_image = st.file_uploader("上傳《大家說英語》內頁照片", type=["jpg", "png", "jpeg"])
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, use_column_width=True)
            
            if st.button("請教練分析敵情 (擷取單字)"):
                with st.spinner("教練正在解讀暗號..."):
                    prompt = "你是一位熱血的棒球英語教練。請從這張圖片中找出3到5個重點單字，列出英文拼寫、中文解釋，並給予一句簡單的英文例句。請用棒球教練的口吻給予鼓勵！"
                    response = model.generate_content([prompt, image])
                    st.success("分析完成！")
                    st.write(response.text)

    # --- 第二局：AI 聆聽跟讀音檔 ---
    with tab2:
        st.header("🎤 第二局：揮棒練習 (Shadowing)")
        st.write("請唸出剛剛教練指定的句子，讓教練聽聽你的揮棒力道！")
        audio_file = st.file_uploader("上傳你的錄音檔 (mp3/m4a/wav)", type=["mp3", "m4a", "wav"])
        
        if st.button("⚾ 提交錄音！"):
            if audio_file:
                with st.spinner("裁判正在看慢動作重播 (分析發音中)..."):
                    # 將錄音檔暫存，以便傳送給 AI
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                        tmp.write(audio_file.read())
                        tmp_path = tmp.name
                    
                    try:
                        audio_upload = genai.upload_file(path=tmp_path)
                        prompt = "你是一位大聯盟棒球英語教練。請仔細聆聽這段學生的英文跟讀，給出 0-100 的流暢度評分。挑出他發音含糊的單字，並用棒球術語（如揮棒落空、安打等）給予他熱血的評語與改進建議。"
                        response = model.generate_content([prompt, audio_upload])
                        st.write(response.text)
                        
                        st.session_state.points += 50
                        st.success("順利上壘！獲得 50 點訓練點數！")
                    except Exception as e:
                        st.error("球具出現問題，請重新上傳音檔一次！")
                    finally:
                        os.remove(tmp_path) # 清除暫存檔
            else:
                st.error("球還沒投出來！請先上傳錄音檔。")

    # --- 第三局：簡單文法防呆測驗 ---
    with tab3:
        st.header("📝 第三局：戰術重組 (句型)")
        st.write("教練指示：請把以下單字重組成正確的句子！")
        st.info("[ baseball / is / playing / fun / very ]")
        ans = st.text_input("請在這裡輸入你的答案 (不需加標點符號)：")
        
        if st.button("傳球！(送出答案)"):
            if ans.lower().strip() == "playing baseball is very fun":
                st.balloons()
                st.success("紅中好球！完美雙殺守備！獲得 50 點！")
                st.session_state.points += 50
            else:
                st.warning("這球稍微投偏了喔，檢查一下單字順序，再投一次！")
