import streamlit as st
import time

st.set_page_config(page_title="Pediatric RR Counter", layout="centered")

# CSS المطور لمنع الضغط الخطأ وتكبير الزر
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    .stButton > button {
        width: 100vw !important;
        height: 65vh !important;
        font-size: 60px !important;
        font-weight: bold;
        color: white !important;
        background-color: #ff4b4b !important;
        border: none !important;
    }
    /* تنسيق خاص لزر Restart ليكون مختلفاً وبعيداً */
    .restart-btn > div > button {
        height: 80px !important;
        width: 200px !important;
        font-size: 20px !important;
        background-color: #333 !important;
        margin-top: 50px !important;
        border-radius: 10px !important;
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
    # منطقة الضغط العمياء
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
    # عرض النتائج في منطقة آمنة بعيدة عن مكان الضغط السابق
    final_rr = st.session_state.count * 4
    st.balloons()
    st.markdown(f"<h1 style='text-align: center; color: green;'>RR: {final_rr} bpm</h1>", unsafe_allow_html=True)
    st.write(f"Total breaths recorded: {st.session_state.count}")
    
    # مساحة فارغة لضمان عدم الضغط بالخطأ
    st.write("")
    st.write("")
    
    # زر Restart صغير وبعيد في حاوية منفصلة
    st.markdown('<div class="restart-btn">', unsafe_allow_html=True)
    if st.button("New Calculation"):
        st.session_state.count = 0
        st.session_state.start_time = None
        st.session_state.finished = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
