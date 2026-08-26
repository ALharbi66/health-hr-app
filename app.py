import streamlit as st
import pandas as pd

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستشار لائحة الصحة القابضة", layout="wide")

# تطبيق التنسيق من اليمين إلى اليسار (RTL) للغة العربية في الواجهة
st.markdown(
    """
    <style>
    .stApp {
        direction: RTL;
        text-align: right;
    }
    div[data-testid="stTextInput"] label {
        text-align: right;
        width: 100%;
    }
    input {
        direction: RTL;
        text-align: right;
    }
    th {
        text-align: right !important;
    }
    td {
        text-align: right !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔍 نظام البحث الذكي في لائحة الموارد البشرية")

# قراءة البيانات من ملف الإكسل الخاص بك
@st.cache_data
def load_data():
    file_name = "لائحة_الموارد_البشرية.xlsx"
    materials_df = pd.read_excel(file_name, sheet_name="المواد")
    penalties_df = pd.read_excel(file_name, sheet_name="العقوبات")
    return materials_df, penalties_df

try:
    materials, penalties = load_data()

    # إنشاء علامات تبويب للواجهة (خانتين للبحث)
    tab1, tab2 = st.tabs(["📄 البحث في المواد القانونية", "⚠️ البحث في المخالفات والعقوبات"])

    with tab1:
        st.subheader("ابحث عن أي موضوع أو رقم مادة")
        search_mat = st.text_input("اكتب كلمة دلالية للبحث في المواد (مثل: إجازة، نقل، تجربة):", key="mat")
        
        # تصفية الجدول بناءً على البحث وإظهاره في الأسفل
        if search_mat:
            filtered_mat = materials[materials.astype(str).apply(lambda x: x.str.contains(search_mat, case=False)).any(axis=1)]
            st.dataframe(filtered_mat, use_container_width=True)
        else:
            st.dataframe(materials, use_container_width=True)

    with tab2:
        st.subheader("ابحث عن أي مخالفة لمعرفة عقوبتها")
        search_pen = st.text_input("اكتب كلمة دلالية للبحث في العقوبات (مثل: غياب، تأخر، زي، تدخين):", key="pen")
        
        # تصفية جدول العقوبات وإظهاره في الأسفل
        if search_pen:
            filtered_pen = penalties[penalties.astype(str).apply(lambda x: x.str.contains(search_pen, case=False)).any(axis=1)]
            st.dataframe(filtered_pen, use_container_width=True)
        else:
            st.dataframe(penalties, use_container_width=True)

except FileNotFoundError:
    st.error("يرجى التأكد من أن ملف الإكسل مرفوع بنفس الاسم 'لائحة_الموارد_البشرية.xlsx' في المستودع.")
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف، تأكد من تسمية الصفحات بـ 'المواد' و 'العقوبات'. التفاصيل: {e}")
