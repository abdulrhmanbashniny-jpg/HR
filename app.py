import streamlit as st

st.set_page_config(page_title="منصة إدارة الموارد البشرية", page_icon="🏢", layout="wide")

# بيانات المستخدمين
USERS_DB = {
    "1001": {"name": "أحمد محمد", "role": "الموظف", "password": "123", "dept": "IT"},
    "1002": {"name": "سارة علي", "role": "مشرف القسم", "password": "123", "dept": "IT"},
    "1003": {"name": "خالد عمر", "role": "مدير القسم", "password": "123", "dept": "IT"},
    "1004": {"name": "منى سعيد", "role": "مدير الموارد البشرية", "password": "123", "dept": "HR"},
    "1005": {"name": "فهد ناصر", "role": "مدير مالي", "password": "123", "dept": "Finance"},
    "9999": {"name": "Admin", "role": "مدير النظام", "password": "admin", "dept": "Admin"}
}

# تهيئة الجلسة
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_info' not in st.session_state: st.session_state.user_info = None
if 'requests_db' not in st.session_state: st.session_state.requests_db = []

def login(uid, pwd):
    if uid in USERS_DB and USERS_DB[uid]['password'] == pwd:
        st.session_state.logged_in = True
        st.session_state.user_info = USERS_DB[uid]
        st.session_state.user_id = uid
        return True
    return False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 بوابة الموظفين")
        uid = st.text_input("الرقم الوظيفي")
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول", use_container_width=True):
            if login(uid, pwd): st.rerun()
            else: st.error("بيانات خاطئة")
        with st.expander("بيانات التجربة"):
            st.code("الموظف: 1001 / 123\nالمدير: 1003 / 123")
else:
    user = st.session_state.user_info
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.sidebar.title(f"مرحباً {user['name']}")
    st.sidebar.info(f"المنصب: {user['role']}")
    
    if st.sidebar.button("تسجيل خروج"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()
    
    st.title("🏠 الصفحة الرئيسية")
    m1, m2, m3 = st.columns(3)
    m1.metric("الرصيد الإجازات", "30 يوم")
    m2.metric("الطلبات النشطة", len(st.session_state.requests_db))
    m3.metric("ساعات العمل", "8:00")
    st.success("✅ تم تسجيل الدخول بنجاح. انتقل للقائمة الجانبية لاستخدام الخدمات.")
