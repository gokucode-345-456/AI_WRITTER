import streamlit as st
import google.generativeai as genai

st.title("🕵️ Máy dò lỗi Gemini")

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    st.write("✅ Kết nối API Key thành công!")
    
    st.subheader("Danh sách Model mà Key của bạn được phép dùng:")
    models = [m.name for m in genai.list_models()]
    
    if models:
        st.success(f"Tìm thấy {len(models)} models!")
        st.write(models)
        st.info("Hãy copy 1 cái tên trong danh sách trên dán vào code cũ là chạy được!")
    else:
        st.error("Danh sách trống rỗng! Google đang chặn Key này trên server này rồi.")

except Exception as e:
    st.error(f"Lỗi hệ thống: {e}")