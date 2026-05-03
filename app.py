import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions # Thêm dòng này để ép phiên bản

st.set_page_config(page_title="Viết Văn AI", page_icon="✍️")

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Cấu hình API key
    genai.configure(api_key=API_KEY)
except:
    st.error("Thiếu GOOGLE_API_KEY!")
    st.stop()

# --- CHIÊU CUỐI: ÉP PHIÊN BẢN API VÀO REQUEST ---
# Chúng ta dùng RequestOptions để bắt nó chạy bản v1 thay vì v1beta
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', # Quay lại bản ổn định nhất
)

st.title("✍️ Trợ Lý Viết Văn AI")

topic = st.text_area("Nhập đề bài:", height=150)

if st.button("🚀 Bắt đầu sáng tác"):
    if topic:
        with st.spinner('Đang múa bút...'):
            try:
                # ÉP PHIÊN BẢN API Ở ĐÂY
                response = model.generate_content(
                    f"Viết bài văn về: {topic}",
                    request_options=RequestOptions(api_version='v1') # ÉP DÙNG V1
                )
                st.success("Xong rồi nè!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi rồi cu ơi: {e}")
                st.info("Thử đổi tên model trong code thành 'gemini-3.1-flash-live-preview' nếu vẫn lỗi 404 nhé!")