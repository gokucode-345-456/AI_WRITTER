import streamlit as st
import google.generativeai as genai

# --- 1. CẤU HÌNH GIAO DIỆN (Để hiển thị đẹp trên điện thoại) ---
st.set_page_config(
    page_title="Viết Văn AI",
    page_icon="✍️",
    layout="centered" # Giúp nội dung không bị tràn sang hai bên
)

# --- 2. CẤU HÌNH BẢO MẬT API KEY ---
# Khi đưa lên web, chúng ta dùng st.secrets để giấu Key đi
# Lát nữa mình sẽ chỉ bạn chỗ dán Key thật trên web Streamlit
GOOGLE_API_KEY = "AIzaSyDRBlRB8o2VUWZgATilB5CWmZQnxpncKyM"
# Đoạn code này sẽ tự thử từng tên một, cái nào chạy được thì lấy
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('gemini-pro') # Phương án dự phòng cuối cùng
# --- 3. CHỌN MODEL ---
# Dùng tên model chuẩn để tránh lỗi 404
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 4. GIAO DIỆN APP ---
st.title("✍️ Trợ Lý Viết Văn AI")
st.markdown("đưa đề văn đây")

# Ô nhập liệu - được tối ưu để gõ trên điện thoại dễ hơn
topic = st.text_area("Chủ đề bài văn:", 
                     placeholder="Ví dụ: Tả Michael Jackson hoặc Nghị luận về học tập...",
                     height=150)

# Nút bấm
if st.button("🚀 Bắt đầu sáng tác"):
    if topic:
        with st.spinner('Đang múa bút... đợi tí nhé!'):
            try:
                # Prompt để AI viết hay hơn
                full_prompt = f"Bạn là một học sinh giỏi văn. Hãy viết một bài văn sâu sắc, giàu cảm xúc về: {topic}"
                response = model.generate_content(full_prompt)
                
                # Hiển thị kết quả
                st.success("Xong rồi nè!")
                st.markdown("---")
                st.write(response.text)
                
                # Thêm nút để copy nhanh (tiện cho điện thoại)
                st.button("Làm lại bài khác", on_click=lambda: st.rerun())
            except Exception as e:
                st.error(f"Lỗi rồi: {e}")
    else:
        st.warning("Nhập cái gì đó đi chứ cu!")