import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN CHUẨN MOBILE ---
st.set_page_config(page_title="Viết Văn AI", page_icon="✍️", layout="centered")

st.markdown("""
    <style>
    /* Giấu các thành phần dư thừa */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #F0F2F5; }
    
    /* Input kiểu app điện thoại */
    .stTextArea textarea { 
        border-radius: 20px !important; 
        font-size: 16px !important; 
        border: 2px solid #ddd !important;
    }
    
    /* Nút bấm to, dễ chạm trên cảm ứng */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        height: 3.5em;
        background: linear-gradient(135deg, #007AFF 0%, #0056b3 100%);
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        margin-top: 10px;
    }
    
    /* Khung hiển thị bài văn */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        line-height: 1.8;
        font-size: 16px;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KẾT NỐI API ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Chưa cấu hình API Key trong Secrets!")
    st.stop()

# --- CƠ CHẾ TỰ ĐỘNG TÌM MODEL ĐANG SỐNG (FIX 404) ---
@st.cache_resource
def find_working_model():
    try:
        # Lấy danh sách tất cả model mà Key này được phép dùng
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Danh sách ưu tiên
        targets = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        for t in targets:
            if t in available:
                return genai.GenerativeModel(t)
        
        # Nếu không thấy cái nào trong list ưu tiên, lấy đại cái đầu tiên đang sống
        if available:
            return genai.GenerativeModel(available[0])
    except:
        # Fallback cuối cùng nếu list_models cũng lỗi
        return genai.GenerativeModel('gemini-1.5-flash')
    return None

model = find_working_model()

# --- GIAO DIỆN APP ---
st.markdown("<h2 style='text-align: center; color: #007AFF;'>✍️ Trợ Lý Viết Văn</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Cực nhanh - Cực hay - Cực dễ</p>", unsafe_allow_html=True)

topic = st.text_area("", placeholder="Nhập chủ đề bài văn bạn muốn viết...", height=150)

if st.button("🚀 BẮT ĐẦU SÁNG TÁC"):
    if topic:
        with st.spinner('AI đang múa bút, chờ tí nhé...'):
            try:
                # Gửi yêu cầu viết văn
                prompt = f"Bạn là một chuyên gia viết văn. Hãy viết một bài văn sâu sắc, hay về: {topic}"
                response = model.generate_content(prompt)
                
                st.markdown("### ✨ Tác phẩm của bạn:")
                st.markdown(f'<div class="result-card">{response.text}</div>', unsafe_allow_html=True)
                
                # Nút reset đơn giản
                if st.button("Viết bài khác"):
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Lỗi: {e}")
                st.info("Mẹo: Đợi 30 giây rồi nhấn lại nhé (lỗi giới hạn lượt dùng).")
    else:
        st.warning("Nhập cái gì đó đi đã cu!")
