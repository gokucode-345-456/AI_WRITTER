import streamlit as st
import google.generativeai as genai

# --- 1. CẤU HÌNH MOBILE-FIRST ---
st.set_page_config(
    page_title="Viết Văn AI",
    page_icon="✍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS CUSTOM ĐỂ NHÌN GIỐNG APP ĐIỆN THOẠI ---
st.markdown("""
    <style>
    /* Ẩn bớt các thành phần thừa của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chỉnh nền app */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Làm khung nhập liệu to và dễ gõ */
    .stTextArea textarea {
        border-radius: 15px !important;
        border: 2px solid #E0E0E0 !important;
        padding: 15px !important;
        font-size: 16px !important; /* Tránh iPhone tự động zoom khi focus */
    }
    
    /* Nút bấm kiểu iOS/Android hiện đại */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3em;
        background-color: #007AFF; /* Màu xanh Apple */
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    
    .stButton>button:active {
        transform: scale(0.98);
    }

    /* Khung kết quả bài văn */
    .result-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #007AFF;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        line-height: 1.6;
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KẾT NỐI API ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Lỗi API Key!")
    st.stop()

# --- 4. HÀM TÌM MODEL ---
@st.cache_resource
def get_model():
    # Ưu tiên Flash cho nhanh và mượt trên mobile
    for m_name in ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(m_name)
            return m
        except:
            continue
    return None

model = get_model()

# --- 5. GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center; color: #1C1C1E;'>✍️ Viết Văn AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8E8E93;'>Nhập đề bài và để AI lo phần còn lại</p>", unsafe_allow_html=True)

# Khung nhập liệu
topic = st.text_area("", placeholder="Hôm nay bạn muốn viết về chủ đề gì?", height=120)

# Nút bấm to, chiếm hết chiều ngang màn hình điện thoại
if st.button("🚀 BẮT ĐẦU VIẾT"):
    if topic:
        with st.spinner('Đang suy nghĩ...'):
            try:
                response = model.generate_content(f"Viết bài văn về: {topic}")
                
                st.markdown("### ✨ Kết quả:")
                # Cho kết quả vào một cái box nhìn cho chuyên nghiệp
                st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                
                # Nút copy nhanh (Streamlit hỗ trợ sẵn)
                st.copy_to_clipboard(response.text)
                st.toast("Đã copy bài văn!")
                
            except Exception as e:
                st.error(f"Lỗi: {e}")
    else:
        st.warning("Bạn chưa nhập đề bài mà!")
