import streamlit as st
import time

# إعداد الصفحة
st.set_page_config(page_title="Pediatric RR Counter", layout="centered")

# CSS لجعل الزر عملاقاً وملء الشاشة تقريباً
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 60vh;
        font-size: 50px !important;
        font-weight: bold;
        color: white !important;
        background-color: #ff4b4b !important;
        border-radius: 20px;
        border: none;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: transform 0.1s;
    }
    .stButton > button:active {
        transform: scale(0.95);
        background-color: #cc0000 !important;
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

# عرض الواجهة
if not st.session_state.finished:
    # زر عملاق
    st.button("TAP HERE", on_click=count_breath)
    
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 15 - int(elapsed))
        st.subheader(f"⏱ Time Left: {remaining}s")
        st.write(f"🔢 Count: {st.session_state.count}")
        
        if remaining > 0:
            time.sleep(0.1)
            st.rerun()
        else:
            st.session_state.finished = True
            st.rerun()
else:
    final_rr = st.session_state.count * 4
    st.balloons()
    st.success(f"Final Result: {final_rr} bpm")
    
    if st.button("Restart Counter"):
        st.session_state.count = 0
        st.session_state.start_time = None
        st.session_state.finished = False
        st.rerun()
