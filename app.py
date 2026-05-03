import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện Mobile
st.set_page_config(page_title="AI Thám Tử", page_icon="🕵️")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background: #007AFF; color: white; border: none; }
    .status-box { padding: 15px; border-radius: 15px; background: white; margin-bottom: 10px; border-left: 5px solid #007AFF; }
    </style>
    """, unsafe_allow_html=True)

# Kết nối API
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Thiếu API Key trong Secrets!")
    st.stop()

st.title("🕵️ Máy Dò Model AI")

# --- PHẦN 1: THÁM TỬ ---
if st.button("🔍 BẮT ĐẦU DÒ TÌM MODEL"):
    with st.spinner("Đang lục soát kho hàng của Google..."):
        try:
            # Lấy tất cả model hỗ trợ viết văn
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if models:
                st.success(f"Tìm thấy {len(models)} model khả dụng!")
                # Lưu danh sách vào session để dùng cho phần dưới
                st.session_state['found_models'] = models
                for m in models:
                    st.code(m)
            else:
                st.error("Không tìm thấy model nào! Có thể Key bị chặn vùng.")
        except Exception as e:
            st.error(f"Lỗi khi dò tìm: {e}")

st.divider()

# --- PHẦN 2: CHỌN VÀ VIẾT ---
if 'found_models' in st.session_state:
    st.subheader("✍️ Thử nghiệm viết văn")
    
    # Cho bạn chọn model từ danh sách vừa tìm được
    selected_model_name = st.selectbox("Chọn model muốn thử:", st.session_state['found_models'])
    
    topic = st.text_area("Nhập đề bài:", placeholder="Ví dụ: Tả con chó nhà em")
    
    if st.button("🚀 CHẠY THỬ MODEL NÀY"):
        try:
            # Khởi tạo model bạn đã chọn
            test_model = genai.GenerativeModel(selected_model_name)
            response = test_model.generate_content(f"Viết bài văn ngắn về: {topic}")
            
            st.markdown("### ✨ Kết quả:")
            st.info(response.text)
        except Exception as e:
            st.error(f"Model này báo lỗi: {e}")
            st.warning("Gợi ý: Thử chọn model khác trong danh sách trên!")
else:
    st.info("Bấm nút 'Dò tìm' ở trên trước để xem Key của bạn dùng được những gì nhé!")
