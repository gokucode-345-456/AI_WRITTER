import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viết Văn AI", page_icon="✍️")

# 1. Cấu hình API Key
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Thiếu GOOGLE_API_KEY trong Secrets!")
    st.stop()

# 2. KHỞI TẠO MODEL THEO CÁCH "AN TOÀN" NHẤT
# Mình sẽ bỏ RequestOptions và chỉ dùng tên model kèm prefix
# Thử dùng bản Flash ổn định nhất hiện nay
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("✍️ Trợ Lý Viết Văn AI")

topic = st.text_area("Nhập đề bài:", height=150)

if st.button("🚀 Bắt đầu sáng tác"):
    if topic:
        with st.spinner('Đang múa bút...'):
            try:
                # Gửi yêu cầu bình thường, không thêm option phức tạp
                response = model.generate_content(f"Viết bài văn về: {topic}")
                
                st.success("Xong rồi nè!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                # Nếu vẫn báo 404, chúng ta sẽ thử "ép" tên model khác ngay tại đây
                st.warning("Đang thử kết nối lại bằng giao thức dự phòng...")
                try:
                    # Thử lại với tên đầy đủ nếu bản ngắn gọn bị 404
                    alternative_model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = alternative_model.generate_content(f"Viết bài văn về: {topic}")
                    st.success("Xong rồi nè!")
                    st.write(response.text)
                except Exception as e2:
                    st.error(f"Lỗi hệ thống: {e2}")
    else:
        st.warning("Nhập đề bài đã cu!")
