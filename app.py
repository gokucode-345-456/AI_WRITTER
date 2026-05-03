import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viết Văn AI", page_icon="✍️")

# 1. Cấu hình
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Thiếu GOOGLE_API_KEY trong Secrets!")
    st.stop()

# 2. Hàm tìm model "sống"
@st.cache_resource
def load_model():
    # Danh sách ưu tiên các model từ mới đến cũ
    priority_models = [
        'gemini-1.5-flash',
        'models/gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro'
    ]
    
    # Thử lấy danh sách model thực tế từ API
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Ưu tiên những thằng có trong danh sách của mình mà API cũng có
        for p in priority_models:
            # Kiểm tra xem tên có khớp (có hoặc không có tiền tố models/)
            for a in available:
                if p in a:
                    return genai.GenerativeModel(a)
        # Nếu không khớp cái nào, lấy đại thằng đầu tiên trong danh sách API trả về
        if available:
            return genai.GenerativeModel(available[0])
    except:
        # Nếu ngay cả việc liệt kê cũng lỗi, dùng liều bản ổn định nhất
        return genai.GenerativeModel('gemini-1.5-flash')

model = load_model()

# 3. Giao diện
st.title("✍️ Trợ Lý Viết Văn AI")
if model:
    st.caption(f"🤖 Đang sử dụng não: {model.model_name}")

topic = st.text_area("Nhập đề bài:", height=150)

if st.button("🚀 Bắt đầu sáng tác"):
    if topic:
        with st.spinner('Đang múa bút...'):
            try:
                # Gửi yêu cầu
                response = model.generate_content(f"Viết một bài văn hay về: {topic}")
                st.success("Xong rồi nè!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi rồi cu ơi: {e}")
    else:
        st.warning("Nhập đề bài đã cu!")
