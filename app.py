import streamlit as st

st.set_page_config(page_title="دفتر ديوني", page_icon="📖", layout="wide")

st.title("📖 دفتر ديوني - متعدد العملات")

if "debtors" not in st.session_state:
    st.session_state.debtors = {}

if "calc_display" not in st.session_state:
    st.session_state.calc_display = ""

tab1, tab2, tab3 = st.tabs(["📊 لوحة التحكم", "👥 العملاء والديون", "🧮 الحاسبة"])

with tab1:
    st.subheader("📊 ملخص الاحصائيات")
    total_clients = len(st.session_state.debtors)
    total_yer = 0.0
    total_sar = 0.0
    total_usd = 0.0

    for key, amount in st.session_state.debtors.items():
        if "ريال يمني" in key:
            total_yer += amount
        elif "ريال سعودي" in key:
            total_sar += amount
        elif "دولار أمريكي" in key:
            total_usd += amount

    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric(label="إجمالي العملاء", value=total_clients)

    st.write("---")
    st.write("### 💰 مبالغ العملات")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.metric(label="ريال يمني (YER)", value=f"{total_yer:,.2f}")
    with col_c2:
        st.metric(label="ريال سعودي (SAR)", value=f"{total_sar:,.2f}")
    with col_c3:
        st.metric(label="دولار أمريكي (USD)", value=f"{total_usd:,.2f}")

with tab2:
    st.subheader("➕ إضافة عميل جديد")
    with st.form("add_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("اسم العميل")
            phone = st.text_input("رقم الهاتف (اختياري)")
        with col2:
            amount = st.number_input("المبلغ الأولي", min_value=0.0, step=1.0)
        with col3:
            currency = st.selectbox("العملة", ["ريال يمني", "ريال سعودي", "دولار أمريكي"])
        
        submitted = st.form_submit_button("حفظ العميل")
        if submitted:
            if name.strip() == "":
                st.error("الرجاء إدخال اسم العميل!")
            else:
                key = f"{name} ({currency})"
                st.session_state.debtors[key] = amount
                st.success(f"تم حفظ العميل {name} بنجاح!")
                st.rerun()

    st.write("---")
    st.subheader("📋 إدارة الديون والتسديد")

    if not st.session_state.debtors:
        st.info("لا توجد حسابات مسجلة حتى الآن.")
    else:
        selected_key = st.selectbox("اختر العميل للتعديل:", list(st.session_state.debtors.keys()))
        current_val = st.session_state.debtors[selected_key]
        st.write(f"**المبلغ المتبقي الحالي:** `{current_val:,.2f}`")
        
        col_a, col_b = st.columns(2)
        with col_a:
            add_val = st.number_input("مبلغ الإضافة (+)", min_value=0.0, step=1.0, key="add_val")
            if st.button("إضافة دين"):
                st.session_state.debtors[selected_key] += add_val
                st.success("تمت الإضافة بنجاح!")
                st.rerun()
                
        with col_b:
            pay_val = st.number_input("مبلغ التسديد (-)", min_value=0.0, step=1.0, key="pay_val")
            if st.button("تسديد المبلغ"):
                st.session_state.debtors[selected_key] -= pay_val
                st.success("تم التسديد بنجاح!")
                st.rerun()

with tab3:
    st.write("### ⌨️ الآلة الحاسبة")
    st.text_input("الشاشة:", value=st.session_state.calc_display, key="d_input")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("1"): st.session_state.calc_display += "1"; st.rerun()
        if st.button("4"): st.session_state.calc_display += "4"; st.rerun()
        if st.button("7"): st.session_state.calc_display += "7"; st.rerun()
        if st.button("C"): st.session_state.calc_display = ""; st.rerun()
    with col2:
        if st.button("2"): st.session_state.calc_display += "2"; st.rerun()
        if st.button("5"): st.session_state.calc_display += "5"; st.rerun()
        if st.button("8"): st.session_state.calc_display += "8"; st.rerun()
        if st.button("0"): st.session_state.calc_display += "0"; st.rerun()
    with col3:
        if st.button("3"): st.session_state.calc_display += "3"; st.rerun()
        if st.button("6"): st.session_state.calc_display += "6"; st.rerun()
        if st.button("9"): st.session_state.calc_display += "9"; st.rerun()
        if st.button("."): st.session_state.calc_display += "."; st.rerun()
    with col4:
        if st.button("+"): st.session_state.calc_display += " + "; st.rerun()
        if st.button("-"): st.session_state.calc_display += " - "; st.rerun()
        if st.button("*"): st.session_state.calc_display += " * "; st.rerun()
        if st.button("/"): st.session_state.calc_display += " / "; st.rerun()

    if st.button("="):
        try:
            result = eval(st.session_state.calc_display)
            st.session_state.calc_display = str(result)
            st.rerun()
        except:
            st.error("خطأ في العملية الحسابية")