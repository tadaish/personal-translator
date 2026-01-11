import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Dịch Thuật Cá Nhân", page_icon="🌏")

# --- CSS TÙY CHỈNH (CHO ĐẸP HƠN) ---
st.markdown("""
<style>
    .stTextArea textarea {font-size: 16px !important;}
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ---
st.title("🌏 Dịch thuật Đa Ngôn Ngữ")
st.caption("Sử dụng Gemini 2.5 Flash - Anh | Trung | Indo | Việt")

# --- LẤY API KEY TỪ SECRETS (BẢO MẬT) ---
# Khi chạy trên máy local, bạn có thể thay dòng này bằng api_key = "KEY_CUA_BAN"
# Nhưng khi deploy, hãy dùng st.secrets để không bị lộ key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.warning("Chưa cấu hình API Key trong Secrets.")
    st.stop()

# --- CẤU HÌNH GEMINI ---
genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.3,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

# System Instruction: Nhắc model vai trò dịch thuật
system_prompt = """
Bạn là một biên dịch viên chuyên nghiệp, thông thạo tiếng Việt, Anh, Trung (Giản thể) và Indonesia.
Nội dung dịch về các giao dịch tiền tệ trong game: Lineage 2M, Throne and Liberty, Blade and Soul Neo, Dragon Nest
Nhiệm vụ: Dịch văn bản người dùng nhập sang ngôn ngữ đích.
Yêu cầu:
1. Chỉ trả về kết quả dịch, không giải thích dài dòng.
2. Văn phong tự nhiên, đời thường, phù hợp với các cuộc đối thoại trên mạng cũng như ngoài đời.
3. Nếu dịch sang tiếng Việt: Xưng hô lịch sự hoặc trung tính.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite", # Model nhanh và free nhất
    generation_config=generation_config,
    system_instruction=system_prompt
)

# --- GIAO DIỆN NGƯỜI DÙNG ---

# 1. Chọn ngôn ngữ đích
col1, col2 = st.columns([1, 3])
with col1:
    target_lang = st.selectbox(
        "Dịch sang:",
        ["Tiếng Việt", "Tiếng Anh", "Tiếng Trung", "Tiếng Indo"],
        index=0 # Mặc định chọn Tiếng Việt
    )

# 2. Nhập văn bản
source_text = st.text_area("Nhập văn bản cần dịch:", height=150, placeholder="Nhập nội dung..")

# 3. Nút dịch và Xử lý
if st.button("Dịch Ngay", type="primary"):
    if not source_text:
        st.toast("Vui lòng nhập nội dung!", icon="⚠️")
    else:
        with st.spinner("Đang dịch..."):
            try:
                # Tạo prompt gửi đi
                prompt = f"Dịch văn bản sau sang {target_lang}:\n\n{source_text}"
                response = model.generate_content(prompt)
                
                # Hiển thị kết quả
                st.success("Kết quả dịch:")
                st.markdown(f"### {response.text}")
                
                # Nút copy (Streamlit hỗ trợ copy code block, nên ta để trong code block cho tiện)
                st.code(response.text, language=None)
                
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")