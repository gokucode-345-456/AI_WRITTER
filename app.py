import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện
st.set_page_config(page_title="Viết Văn AI", page_icon="✍️", layout="centered")

# Lấy Key từ Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Thiếu GOOGLE_API_KEY trong phần Secrets!")
    st.stop()

# --- CHIÊU CUỐI: TỰ ĐỘNG DÒ TÌM MODEL ---
@st.cache_resource # Lưu lại kết quả để không phải quét nhiều lần
def get_working_model():
    # Danh sách các tên gọi có thể chạy được của Gemini
    model_names = [
        'gemini-1.5-flash', 
        'models/gemini-1.5-flash', 
        'gemini-pro', 
        'models/gemini-pro'
    ]
    
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # Thử yêu cầu nhẹ để check xem có chạy thật không
            m.generate_content("hi", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = get_working_model()

if model is None:
    st.error("Không tìm thấy model nào khả dụng. Kiểm tra lại API Key hoặc vùng địa lý!")
    st.stop()

# --- GIAO DIỆN APP ---
st.title("✍️ Trợ Lý Viết Văn AI")
topic = st.text_area("Chủ đề bài văn:", height=150)

if st.button("🚀 Bắt đầu sáng tác"):
    if topic:
        with st.spinner('Đang múa bút...'):
            try:
                response = model.generate_content(f"Viết bài văn về: {topic}")
                st.success("Xong rồi nè!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi: {e}")