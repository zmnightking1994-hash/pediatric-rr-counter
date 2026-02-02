import streamlit as st
import time

st.set_page_config(page_title="Pediatric RR Counter", layout="centered")

# CSS لتخصيص الواجهة ومنع الأخطاء
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    /* الزر الرئيسي العملاق */
    .stButton > button {
        width: 100vw !important;
        height: 65vh !important;
        font-size: 60px !important;
        font-weight: bold;
        color: white !important;
        background-color: #ff4b4b !important;
        border: none !important;
    }
    /* زر Restart الصغير جداً في الزاوية */
    .restart-container {
        display: flex;
        justify-content: flex-end;
        padding-right: 10px;
        margin-top: 100px;
    }
    .restart-container div div button {
        height: 30px !important;
        width: 100px !important;
        font-size: 12px !important;
        background-color: #f0f2f6 !important;
        color: #333 !important;
        border: 1px solid #ccc !important;
        border-radius: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🫁 Pediatric RR Counter")

if 'count' not in st.session_state:
    st.session_state.count = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'finished' not in st.session_state:
    st.session_state.finished = False

def count_breath():
    if not st.session_state.finished:
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        
        elapsed = time.time() - st.session_state.start_time
        if elapsed < 15:
            st.session_state.count += 1
        else:
            st.session_state.finished = True

if not st.session_state.finished:
    st.button("TAP ANYWHERE", on_click=count_breath)
    
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 15 - int(elapsed))
        st.metric("⏱ Time Left", f"{remaining}s")
        if remaining > 0:
            time.sleep(0.1)
            st.rerun()
        else:
            st.session_state.finished = True
            st.rerun()
else:
    # عرض النتيجة بشكل واضح وكبير
    final_rr = st.session_state.count * 4
    st.balloons()
    st.markdown(f"<div style='text-align: center;'><h3 style='color: grey;'>Final Result</h3><h1 style='font-size: 100px; color: #2e7d32;'>{final_rr}</h1><p>bpm</p></div>", unsafe_allow_html=True)
    
    # وضع زر إعادة التشغيل في حاوية "الزاوية البعيدة"
    st.markdown('<div class="restart-container">', unsafe_allow_html=True)
    if st.button("Reset"):
        st.session_state.count = 0
        st.session_state.start_time = None
        st.session_state.finished = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
