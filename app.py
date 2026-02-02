import streamlit as st
import time

st.set_page_config(page_title="Pediatric RR Counter", layout="centered")

st.title("🫁 Pediatric RR Counter")
st.write("Tap the button for each breath. The timer starts on the first tap.")

# تهيئة المتغيرات في الجلسة (Session State)
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'finished' not in st.session_state:
    st.session_state.finished = False

# وظيفة الزر
def count_breath():
    if not st.session_state.finished:
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        
        elapsed = time.time() - st.session_state.start_time
        
        if elapsed < 15:
            st.session_state.count += 1
        else:
            st.session_state.finished = True

# تصميم الواجهة
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if not st.session_state.finished:
        # زر كبير يشبه الدائرة
        st.button("TAP HERE", on_click=count_breath, use_container_width=True, type="primary")
        
        if st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, 15 - int(elapsed))
            st.metric("Time Remaining", f"{remaining}s")
            st.write(f"Current Count: {st.session_state.count}")
            # إعادة تحميل الصفحة تلقائياً لتحديث المؤقت
            if remaining > 0:
                time.sleep(0.1)
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()
    else:
        # النتائج النهائية
        final_rr = st.session_state.count * 4
        st.success(f"Calculation Finished!")
        st.metric("Final RR", f"{final_rr} bpm")
        st.info(f"Total breaths in 15s: {st.session_state.count}")
        
        if st.button("Restart Counter"):
            st.session_state.count = 0
            st.session_state.start_time = None
            st.session_state.finished = False
            st.rerun()
