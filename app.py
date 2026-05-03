import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN MOBILE ---
st.set_page_config(page_title="Viết Văn AI", page_icon="✍️", layout="centered")

st.markdown("""
    <style>
    /* Làm gọn giao diện cho giống App */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #F8F9FA; }
    .stTextArea textarea { 
        border-radius: 15px !important; 
        font-size: 16px !important; 
    }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3.5em;
        background-color: #007AFF;
        color: white;
        font-weight: bold;
        border: none;
    }
    .result-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KẾT NỐI API ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Lỗi: Thiếu API Key trong Secrets!")
    st.stop()

# --- FIX LỖI 404 BẰNG CÁCH GỌI THẲNG MODEL TỪ DANH SÁCH ---
@st.cache_resource
def get_valid_model():
    # Cách an toàn nhất: Liệt kê các model thực tế mà Key của bạn có quyền dùng
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Danh sách ưu tiên (thử cái nào có sẵn trước)
        priorities = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        for p in priorities:
            if p in available_models:
                return genai.GenerativeModel(model_name=p)
        
        # Nếu không có trong ưu tiên, lấy cái đầu tiên tìm thấy
        return genai.GenerativeModel(model_name=available_models[0])
    except Exception as e:
        # Nếu không liệt kê được, dùng fallback cuối cùng
        return genai.GenerativeModel(model_name='gemini-1.5-flash')

model = get_valid_model()

# --- GIAO DIỆN ---
st.markdown("<h2 style='text-align: center;'>✍️ Trợ Lý Viết Văn</h2>", unsafe_allow_html=True)

topic = st.text_area("", placeholder="Nhập đề bài văn vào đây...", height=150)

if st.button("🚀 BẮT ĐẦU SÁNG TÁC"):
    if topic:
        with st.spinner('Đang múa bút...'):
            try:
                # Gọi trực tiếp content
                response = model.generate_content(f"Viết bài văn hay về: {topic}")
                
                st.markdown("### ✨ Bài văn của bạn:")
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
                # Nút copy
                st.button("Làm bài khác", on_click=lambda: st.rerun())
            except Exception as e:
                # Hiện lỗi cụ thể để xử lý nếu vẫn bị
                st.error(f"Lỗi: {e}")
    else:
        st.warning("Nhập đề bài đã cu!")
