import streamlit as st
import pandas as pd

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("سجل الدخول أولاً")
    st.stop()

st.header("📊 التقارير والإحصائيات")
st.bar_chart({"يناير": 5, "فبراير": 12, "مارس": 8})
st.info("هذه الصفحة مخصصة لعرض تقارير الموظفين والرواتب.")
