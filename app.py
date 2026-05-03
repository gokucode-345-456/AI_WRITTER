import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN CHUẨN ---
st.set_page_config(
    page_title="AI Viết Văn Pro",
    page_icon="✍️",
    layout="centered"
)

# CSS Custom: Đẹp trên cả máy tính lẫn điện thoại
st.markdown("""
    <style>
    /* Tổng thể */
    .stApp { background-color: #f8f9fa; }
    
    /* Ẩn bớt rác Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Khung nhập liệu */
    .stTextArea textarea {
        border-radius: 15px !important;
        font-size: 16px !important;
        border: 2px solid #ddd !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Nút bấm kiểu Modern */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    /* Khung kết quả bài văn */
    .paper-style {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        line-height: 1.8;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2d3436;
        border-top: 5px solid #667eea;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CẤU HÌNH API ---
try:
    # Lấy Key từ Secrets (Bạn nhớ dán Key mới vào Secrets rồi nhé!)
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # ÉP DÙNG MODEL BẠN CHỌN
    model = genai.GenerativeModel('models/gemini-3.1-flash-lite-preview')
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")
    st.stop()

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center; color: #4834d4;'>✍️ Trợ Lý Viết Văn AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #636e72;'>Sáng tạo nội dung đỉnh cao trong vài giây</p>", unsafe_allow_html=True)

# Ô nhập đề bài
topic = st.text_area("", placeholder="Ví dụ: Viết một bài văn biểu cảm về người mẹ thân yêu của em...", height=150)

# Nút bấm
if st.button("🚀 BẮT ĐẦU SÁNG TÁC"):
    if topic:
        with st.spinner('AI đang múa bút...'):
            try:
                # Gửi yêu cầu
                response = model.generate_content(f"Bạn là một nhà văn giỏi. Hãy viết một bài văn thật hay, giàu cảm xúc về: {topic}")
                
                # Hiển thị kết quả
                st.markdown("---")
                st.markdown(f'<div class="paper-style">{response.text}</div>', unsafe_allow_html=True)
                
                # Nút phụ để làm mới
                st.button("Viết đề bài khác", on_click=lambda: st.rerun)
                
            except Exception as e:
                # Xử lý lỗi quota 429
                if "429" in str(e):
                    st.warning("⚠️ AI đang hơi bận vì quá nhiều người dùng. Đợi 30 giây rồi nhấn lại bạn nhé!")
                else:
                    st.error(f"Có lỗi xảy ra: {e}")
    else:
        st.warning("Vui lòng nhập đề bài trước nhé!")
