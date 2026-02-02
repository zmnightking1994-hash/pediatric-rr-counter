import streamlit as st
import time

# إعداد الصفحة وتكبير الخط
st.set_page_config(page_title="Pediatric RR Counter", layout="centered")

# كود CSS لجعل الزر ضخماً جداً ودائرياً
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        height: 300px;
        width: 300px;
        border-radius: 50%;
        border: 10px solid #ff2b2b;
        font-size: 30px;
        font-weight: bold;
        display: block;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    div.stButton > button:hover {
        background-color: #ff2b2b;
        color: white;
        border: 10px solid white;
    }
    </style>
""", unsafe_allow_stdio=True)

st.title("🫁 Pediatric RR Counter")
st.write("Click the RED CIRCLE for each breath. Starts on first tap.")

if 'count' not in st.session_state:
    st.session_state.count = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'finished' not in st.session_state:
    st.session_state.finished = False

# منطق العمل
def count_breath():
    if not st.session_state.finished:
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        
        elapsed = time.time() - st.session_state.start_time
        
        if elapsed < 15:
            st.session_state.count += 1
        else:
            st.session_state.finished = True

# عرض الزر والنتائج
if not st.session_state.finished:
    # سيظهر هذا الزر كدائرة حمراء ضخمة بفضل الـ CSS أعلاه
    st.button("TAP", on_click=count_breath)
    
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 15 - int(elapsed))
        st.metric("Time Left", f"{remaining}s")
        st.write(f"Breaths: {st.session_state.count}")
        
        if remaining > 0:
            time.sleep(0.1)
            st.rerun()
        else:
            st.session_state.finished = True
            st.rerun()
else:
    final_rr = st.session_state.count * 4
    st.success("Finished!")
    st.metric("Final Respiratory Rate", f"{final_rr} bpm")
    
    if st.button("Restart"):
        st.session_state.count = 0
        st.session_state.start_time = None
        st.session_state.finished = False
        st.rerun()
