import streamlit as st
import google.generativeai as genai

# ---------------- 設定網頁基本資訊 ----------------
st.set_page_config(
    page_title="大聯盟英語特訓營",
    page_icon="⚾",
    layout="centered"
)

# ---------------- 初始化狀態 (計分板) ----------------
if 'points' not in st.session_state:
    st.session_state.points = 0

# ---------------- 側邊欄：教練辦公室 ----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3349/3349286.png", width=100) # 棒球圖示
    st.title("教練辦公室")
    st.write("請先插入大腦金鑰，啟動 AI 教練！")
    
    # 讓家長輸入 API 金鑰的地方，輸入密碼會以星號隱藏
    api_key = st.text_input("輸入 Gemini API Key:", type="password")
    
    st.divider()
    st.header("🏆 累積棒球基金")
    st.metric(label="目前累積點數", value=f"{st.session_state.points} 點")
    st.write("👉 目標：換取 SSK 新球棒或打擊場代幣！")

# ---------------- 主畫面區 ----------------
st.title("⚾ 專屬大聯盟英語特訓營")

# 檢查是否已經輸入金鑰
if not api_key:
    st.warning("教練還沒睡醒！請先在左邊輸入 API Key 啟動系統。")
else:
    # 成功輸入金鑰後，設定 AI 大腦
    genai.configure(api_key=api_key)
    st.success("AI 教練已上線！準備開始今天的打擊訓練！")
    
    # 建立三個分頁，對應我們的三局比賽
    tab1, tab2, tab3 = st.tabs(["📸 第一局：賽前情蒐 (上傳)", "🎤 第二局：揮棒練習 (跟讀)", "📝 第三局：戰術守備 (測驗)"])
    
    # --- 第一局：上傳雜誌照片 ---
    with tab1:
        st.header("📸 第一局：上傳今日教材")
        st.write("請拍下《大家說英語》今天的文章與 Key Words 區域。")
        uploaded_image = st.file_uploader("上傳教材照片", type=["jpg", "png", "jpeg"])
        
        if uploaded_image:
            st.image(uploaded_image, caption="已成功接收教材！AI 教練正在分析球路...", use_column_width=True)
            # 未來這裡會加入 API 呼叫，讓 Gemini 讀出照片裡的單字和句子
            st.info("✅ 系統已擷取今日重點單字與句型，請進入下一局！")

    # --- 第二局：語音跟讀 ---
    with tab2:
        st.header("🎤 第二局：揮棒練習 (Shadowing)")
        st.write("教練指示：請仔細聽文章，然後按住錄音鍵跟著唸。看準球再揮棒！")
        
        # 顯示要跟讀的句子 (未來由 AI 從照片擷取)
        st.markdown("> **Learning English is like playing baseball. You need to practice every day.**")
        
        # 語音上傳或錄音區塊
        audio_file = st.file_uploader("上傳你的跟讀錄音檔", type=["mp3", "m4a", "wav"])
        
        if st.button("⚾ 揮棒！(送出錄音)"):
            if audio_file:
                st.success("揮棒出去！AI 裁判正在觀看重播判定分數...")
                # 未來這裡會呼叫 Gemini API 聽音檔並給出 0-100 分
            else:
                st.error("球還沒投出來！請先上傳錄音檔。")

    # --- 第三局：單字與文法測驗 ---
    with tab3:
        st.header("📝 第三局：戰術與守備 (單字與句型)")
        st.write("守備失誤是會掉分的！請精準接住教練打出的每一球。")
        
        st.subheader("🛡️ 單字守備")
        vocab_answer = st.text_input("提示：棒球 (請輸入英文拼寫)")
        
        st.subheader("🧠 戰術重組 (句型)")
        st.write("教練解說：今天學到的句型是用 'need to' 表示『必須做某事』。")
        grammar_answer = st.text_input("請將以下單字重組成正確的句子：[ practice / to / everyday / you / need ]")
        
        if st.button("🏆 結算今日成績"):
            st.balloons() # 畫面會噴出慶祝氣球
            st.success("比賽結束！完美達成任務，獲得 100 點！")
            st.session_state.points += 100 # 點數加 100