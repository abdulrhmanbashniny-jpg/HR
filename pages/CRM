import streamlit as st
from datetime import datetime
import pandas as pd
import time

# التحقق من تسجيل الدخول
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ يرجى تسجيل الدخول من الصفحة الرئيسية أولاً")
    st.stop()

user = st.session_state.user_info

# --- دوال المعالجة ---
def submit_request(req_type, req_title, details, loan_amount=0, start_date=None, end_date=None):
    new_req = {
        "id": len(st.session_state.requests_db) + 1,
        "emp_id": st.session_state.user_id,
        "employee": user['name'],
        "type": req_type,
        "title": req_title,
        "details": details,
        "loan_amount": loan_amount,
        "start_date": str(start_date) if start_date else "-",
        "end_date": str(end_date) if end_date else "-",
        "current_stage": 2,  # يبدأ عند المشرف
        "status": "Pending",
        "history": [f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: تم تقديم الطلب"]
    }
    st.session_state.requests_db.append(new_req)

def process_request(rid, action, role, reason=""):
    for r in st.session_state.requests_db:
        if r['id'] == rid:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            if action == "approve":
                # منطق سير العمل
                if role == "مشرف القسم" and r['current_stage'] == 2: r['current_stage'] = 3
                elif role == "مدير القسم" and r['current_stage'] == 3: r['current_stage'] = 4
                elif role == "مدير الموارد البشرية" and r['current_stage'] == 4: r['current_stage'] = 5
                elif role == "مدير مالي" and r['current_stage'] == 5: 
                    r['current_stage'] = 6
                    r['status'] = "Approved"
                    r['history'].append(f"{timestamp}: موافقة نهائية من {role}")
                else:
                    r['history'].append(f"{timestamp}: موافقة مرحلية من {role}")
                
                st.success("✅ تم اعتماد الموافقة")
                time.sleep(1)
                st.rerun()
                
            elif action == "reject":
                r['status'] = "Rejected"
                r['current_stage'] = 0
                r['history'].append(f"{timestamp}: تم الرفض بواسطة {role}. السبب: {reason}")
                st.error("❌ تم رفض الطلب")
                time.sleep(1)
                st.rerun()

# --- الواجهة ---
st.header("📝 الخدمات الذاتية ونظام الموافقات")

# ================= واجهة الموظف =================
if user['role'] == "الموظف":
    st.subheader("تقديم طلب جديد")
    
    c1, c2 = st.columns(2)
    with c1:
        req_type = st.selectbox("نوع الطلب", ["إجازة", "سلفة", "تعريف راتب", "شكوى"])
    
    # تحديث القائمة الثانية بناءً على الأولى
    titles = []
    if req_type == "إجازة": titles = ["سنوية", "اضطرارية", "مرضية", "بدون راتب"]
    elif req_type == "سلفة": titles = ["زواج", "سيارة", "شخصية", "علاج"]
    elif req_type == "تعريف راتب": titles = ["للبنك", "للسفارة", "لجهة حكومية"]
    else: titles = ["عام"]
    
    with c2:
        req_title = st.selectbox("عنوان الطلب", titles)
    
    # حقول متغيرة
    amount = 0
    s_date, e_date = None, None
    
    if req_type == "إجازة":
        col_d1, col_d2 = st.columns(2)
        s_date = col_d1.date_input("تاريخ البداية")
        e_date = col_d2.date_input("تاريخ النهاية")
    elif req_type == "سلفة":
        amount = st.number_input("مبلغ السلفة المطلوب", step=500, min_value=0)

    details = st.text_area("ملاحظات إضافية / التفاصيل")
    
    if st.button("إرسال الطلب", type="primary"):
        submit_request(req_type, req_title, details, amount, s_date, e_date)
        st.success("تم إرسال الطلب بنجاح للمدير المباشر!")
        time.sleep(1.5)
        st.rerun()

    st.divider()
    st.subheader("📂 طلباتي السابقة")
    my_reqs = [r for r in st.session_state.requests_db if r['emp_id'] == st.session_state.user_id]
    
    if my_reqs:
        for r in my_reqs:
            status_color = "orange" if r['status'] == "Pending" else ("green" if r['status'] == "Approved" else "red")
            with st.expander(f"{r['title']} ({r['status']})"):
                st.markdown(f"**الحالة:** :{status_color}[{r['status']}]")
                st.write(f"**التاريخ:** {r['history'][0]}")
                st.write("**سجل الموافقات:**")
                for h in r['history']:
                    st.text(h)
    else:
        st.info("لا توجد طلبات سابقة.")

# ================= واجهة المدراء =================
else:
    st.subheader("📥 صندوق الوارد (الطلبات بانتظار موافقتك)")
    
    # تحديد أي مرحلة يراها هذا المدير
    target_stage = 0
    if user['role'] == "مشرف القسم": target_stage = 2
    elif user['role'] == "مدير القسم": target_stage = 3
    elif user['role'] == "مدير الموارد البشرية": target_stage = 4
    elif user['role'] == "مدير مالي": target_stage = 5
    
    # تصفية الطلبات
    pending_list = [r for r in st.session_state.requests_db if r['current_stage'] == target_stage and r['status'] == "Pending"]
    
    if not pending_list:
        st.success("🎉 لا توجد طلبات معلقة لديك.")
    
    for req in pending_list:
        with st.container(border=True):
            c_head, c_act = st.columns([3, 1])
            with c_head:
                st.markdown(f"### 👤 {req['employee']}")
                st.markdown(f"**الطلب:** {req['title']} ({req['type']})")
                st.write(f"**التفاصيل:** {req['details']}")
                if req['type'] == "سلفة": st.write(f"💰 **المبلغ:** {req['loan_amount']}")
                if req['type'] == "إجازة": st.write(f"📅 {req['start_date']} ➡️ {req['end_date']}")
                
                with st.expander("عرض السجل السابق"):
                    st.write(req['history'])
            
            with c_act:
                if st.button("✅ موافقة", key=f"ok_{req['id']}", use_container_width=True):
                    process_request(req['id'], "approve", user['role'])
                
                st.write("---")
                reason = st.text_input("سبب الرفض", key=f"reason_{req['id']}")
                if st.button("❌ رفض", key=f"no_{req['id']}", use_container_width=True):
                    if reason:
                        process_request(req['id'], "reject", user['role'], reason)
                    else:
                        st.warning("اكتب السبب!")

