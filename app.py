import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện
st.set_page_config(page_title="Viết Văn AI", page_icon="✍️")

# Kết nối API Key từ Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Thiếu GOOGLE_API_KEY trong Secrets!")
    st.stop()

# --- SỬ DỤNG MODEL BẠN VỪA TÌM THẤY ---
model = genai.GenerativeModel('models/gemini-3.1-flash-live-preview')

st.title("✍️ Trợ Lý Viết Văn AI")
st.markdown("Đã kết nối với bộ não mới nhất: **Gemini 3.1 Flash**")

topic = st.text_area("Nhập đề văn của bạn:", placeholder="Ví dụ: Tả con mèo nhà em...", height=150)

if st.button("🚀 Bắt đầu sáng tác"):
    if topic:
        with st.spinner('Đang múa bút...'):
            try:
                response = model.generate_content(f"Hãy viết một bài văn hay về: {topic}")
                st.success("Xong rồi nè!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi: {e}")
    else:
        st.warning("Nhập đề bài đã cu!")