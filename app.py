import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH API ---
# Tạm thời bạn dán API Key vào đây để chạy thử trên máy.
# --- CẤU HÌNH API ---
# Tạm thời bạn dán API Key vào đây để chạy thử trên máy.
API_KEY = "AIzaSyA_R4xk7_YWbQ4RBtst0O5-subg13R1CeY"
genai.configure(api_key=API_KEY)

# Tuyệt chiêu: Tự động quét và chọn mô hình AI phù hợp nhất
model_name = "gemini-1.5-flash" # Tên dự phòng
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        model_name = m.name # Tự động lấy tên chuẩn xác nhất từ hệ thống Google
        break

model = genai.GenerativeModel(model_name)
# --- CẤU HÌNH GIAO DIỆN WEB ---
st.set_page_config(page_title="La Bàn AI", page_icon="🧭", layout="wide")

# Thiết kế Thanh Menu bên trái (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3212/3212608.png", width=100) # Logo mượn tạm
    st.title("Về Dự Án")
    st.info(
        "**La Bàn AI** là dự án STEM thuộc Nhóm 3 (Website/App). "
        "Ứng dụng Trí tuệ nhân tạo để hỗ trợ tâm lý và định hướng nghề nghiệp cho học sinh THPT, "
        "giúp giảm thiểu áp lực đồng trang lứa và rủi ro chọn sai ngành."
    )
    st.success("Tác giả: Nhóm thi STEM Khối D")

# Phần nội dung chính (Main Content)
st.title("🧭 La Bàn AI - Trạm Lắng Nghe & Hướng Nghiệp")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    diem_manh = st.text_input("✨ Điểm mạnh / Sở thích của bạn là gì?", placeholder="VD: Em thích vẽ, học khá Văn, giao tiếp tốt...")
    diem_yeu = st.text_input("🌧️ Điểm yếu / Môn học e ngại?", placeholder="VD: Em sợ môn Toán, hay rụt rè trước đám đông...")

with col2:
    tam_ly = st.text_area("💭 Hiện tại bạn đang cảm thấy thế nào?", placeholder="VD: Em đang rất áp lực vì bố mẹ muốn em thi Kinh tế nhưng em lại thích làm Designer...", height=110)

st.markdown("---")

# --- XỬ LÝ LOGIC ---
if st.button("🚀 Gửi cho La Bàn AI", use_container_width=True):
    if diem_manh and diem_yeu and tam_ly:
        with st.spinner("La Bàn đang phân tích và tìm hướng đi cho bạn..."):
            try:
                # Lệnh mồi (Prompt) "chí mạng" ăn điểm nội dung
                prompt_he_thong = """
                Bạn là một chuyên gia tư vấn tâm lý học đường và định hướng nghề nghiệp xuất sắc tại Việt Nam. 
                Bạn cực kỳ thấu cảm, tinh tế và hiểu tâm lý học sinh Gen Z (15-18 tuổi).
                Dựa vào thông tin học sinh cung cấp, hãy viết một bức thư ngắn gọn (khoảng 250 chữ) để:
                1. Đồng cảm và xoa dịu cảm xúc hiện tại của em ấy một cách ấm áp, không phán xét.
                2. Phân tích logic sự liên kết giữa điểm mạnh và điểm yếu.
                3. Gợi ý 2-3 ngành học hoặc trường Đại học cụ thể tại Việt Nam phù hợp nhất với năng lực.
                Hãy dùng định dạng rõ ràng (bullet point), ngôn từ truyền cảm hứng và thêm một vài emoji phù hợp.
                """
                
                prompt_nguoi_dung = f"Thông tin học sinh:\n- Điểm mạnh: {diem_manh}\n- Điểm yếu: {diem_yeu}\n- Tâm lý: {tam_ly}"
                
                response = model.generate_content(prompt_he_thong + prompt_nguoi_dung)
                
                # Hiển thị kết quả trong một khung đẹp mắt
                st.success("Ting! La Bàn có phản hồi cho bạn đây:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hệ thống đang quá tải, vui lòng thử lại sau! (Lỗi: {e})")
    else:
        st.warning("Bạn vui lòng điền đầy đủ cả 3 ô để La Bàn có thể hiểu bạn trọn vẹn nhất nhé!")
