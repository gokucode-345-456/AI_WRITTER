import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="AI Viết Văn Pro", page_icon="✍️")

# CSS cho giao diện App và Nhật ký
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 12px; background: #007AFF; color: white; font-weight: bold; }
    .paper-style { background: white; padding: 25px; border-radius: 15px; border-left: 5px solid #007AFF; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .history-card { background: #fff; padding: 10px; border-radius: 8px; margin-bottom: 5px; border: 1px solid #ddd; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- KHỞI TẠO DỮ LIỆU LƯU TRỮ ---
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- KẾT NỐI API ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Ưu tiên bản 3.1 Lite bạn thích, không được thì 1.5
    model = genai.GenerativeModel('models/gemini-3.1-flash-lite-preview')
except:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- GIAO DIỆN CHÍNH ---
st.title("✍️ Trợ Lý Viết Văn AI")

topic = st.text_area("", placeholder="Nhập đề bài văn vào đây...", height=120)

if st.button("🚀 BẮT ĐẦU SÁNG TÁC"):
    if topic:
        with st.spinner('AI đang sáng tác...'):
            try:
                response = model.generate_content(f"Hãy viết một bài văn chuyên văn cực hay về: {topic}")
                content = response.text
                
                # Lưu vào lịch sử (đưa lên đầu danh sách)
                st.session_state.history.insert(0, {"topic": topic, "content": content})
                
                # Hiển thị bài vừa viết
                st.markdown("### ✨ Tác phẩm mới nhất:")
                st.markdown(f'<div class="paper-style">{content}</div>', unsafe_allow_html=True)
                
                # Nút tải về máy
                st.download_button(label="📥 Tải bài văn này (.txt)", data=content, file_name=f"{topic[:20]}.txt", mime="text/plain")
                
            except Exception as e:
                st.error(f"Lỗi: {e}")
    else:
        st.warning("Nhập đề bài đã cu!")

# --- PHẦN NHẬT KÝ LƯU TRỮ ---
if st.session_state.history:
    st.divider()
    st.subheader("📚 Nhật ký sáng tác")
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"📝 {item['topic'][:50]}..."):
            st.write(item['content'])
            st.download_button(label="Tải lại file", data=item['content'], file_name=f"bai_van_{i}.txt", key=f"btn_{i}")
