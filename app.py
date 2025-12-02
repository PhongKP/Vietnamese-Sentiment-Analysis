import streamlit as st
import math
from sentiment_model import SentimentService
from database import init_db, insert_record, get_latest, get_total_count

st.set_page_config(page_title="Vietnamese Sentiment Assistant", layout="centered")

@st.cache_resource
def _service():
    init_db()
    svc = SentimentService(use_tokenize=True, abbr_path="abbreviation.csv")
    try:
        _ = svc.analyze("ok")
    except Exception:
        pass
    return svc

def get_paginated_history(page=1, per_page=5):
    offset = (page - 1) * per_page
    total_count = get_total_count()
    total_pages = math.ceil(total_count / per_page) if total_count > 0 else 1
    
    rows = get_latest(per_page, offset)
    
    return rows, total_pages, total_count

def main():
    st.title("Vietnamese Sentiment Analysis")
    
    # Initialize service
    svc = _service()
    
    # Create tabs
    tab1, tab2 = st.tabs(["Phân loại cảm xúc", "📊 Lịch sử gần đây"])
    
    with tab1:
        st.subheader("Nhập câu tiếng Việt")
        
        with st.form("sentiment_form"):
            text = st.text_area(
                "Nhập văn bản cần phân tích:",
                height=120, 
                placeholder="VD: Hôm nay tôi rất vui"
            )
            submitted = st.form_submit_button("Phân loại cảm xúc", type="primary")
            
            if submitted:
                if not text or not text.strip():
                    st.warning("Câu không hợp lệ, thử lại.")
                elif len(text.strip()) < 5:
                    st.error("Câu quá ngắn! (≥ 5 ký tự)")
                else:
                    try:
                        res = svc.analyze(text)
                        if res["sentiment"] == "INVALID":
                            st.warning("Câu không hợp lệ, thử lại.")
                        else:
                            # Hiển thị kết quả với màu sắc
                            if res["sentiment"] == "POSITIVE":
                                st.success(f"Kết quả: **Tích cực**")
                            elif res["sentiment"] == "NEGATIVE":
                                st.error(f"Kết quả: **Tiêu cực**")
                            else:
                                st.info(f"Kết quả: **Trung tính**")
                            
                            # Hiển thị văn bản đã được xử lý
                            if res["text"] != text.strip():
                                st.write(f"📝 Văn bản sau xử lý: *{res['text']}*")
                            
                            insert_record(res["text"], res["sentiment"])
                    except Exception as e:
                        st.error("Câu không hợp lệ, thử lại.")
                        print(f"[Pipeline error] {e}")
    
    with tab2:
        st.subheader("Lịch sử phân tích gần đây")
        
        # Initialize pagination state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        # Get paginated data - chỉ 5 records mỗi trang
        rows, total_pages, total_count = get_paginated_history(
            st.session_state.current_page, 5
        )
        
        if rows:
            st.write(f"📊 Tổng cộng: **{total_count}** bản ghi")
            
            # Display data
            df_data = [
                {
                    "ID": r[0], 
                    "Văn bản": r[1], 
                    "Cảm xúc": r[2], 
                    "Thời gian": r[3]
                } for r in rows
            ]
            
            st.dataframe(
                df_data,
                hide_index=True, 
                width='stretch'
            )
            
            # Pagination
            col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
            
            with col1:
                if st.button("⏮️", disabled=(st.session_state.current_page <= 1), help="Trang đầu"):
                    st.session_state.current_page = 1
                    st.rerun()
            
            with col2:
                if st.button("◀️", disabled=(st.session_state.current_page <= 1), help="Trang trước"):
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col3:
                st.write(f"📄 Trang **{st.session_state.current_page}** / **{total_pages}**")
            
            with col4:
                if st.button("▶️", disabled=(st.session_state.current_page >= total_pages), help="Trang sau"):
                    st.session_state.current_page += 1
                    st.rerun()
            
            with col5:
                if st.button("⏭️", disabled=(st.session_state.current_page >= total_pages), help="Trang cuối"):
                    st.session_state.current_page = total_pages
                    st.rerun()
                    
        else:
            st.info("📝 Chưa có lịch sử phân tích nào.")

if __name__ == "__main__":
    main()