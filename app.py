import streamlit as st
import pandas as pd

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستشار لائحة الصحة القابضة", layout="wide")

# تطبيق التنسيق الشامل من اليمين إلى اليسار (RTL) وتلوين خانات البحث
st.markdown(
    """
    <style>
    /* قلب اتجاه التطبيق بالكامل من اليمين لليسار */
    .stApp {
        direction: RTL !important;
        text-align: right !important;
    }
    
    /* ضبط اتجاه التبويبات والمستندات */
    div[data-testid="stTabs"] {
        direction: RTL !important;
    }
    button[data-testid="stMarkdownContainer"] {
        text-align: right !important;
    }
    
    /* تظليل خانة البحث بلون خلفية مميز وهادئ */
    div[data-testid="stTextInput"] input {
        direction: RTL !important;
        text-align: right !important;
        background-color: #f0f7f4 !important; /* لون تظليل مريح للعين */
        border: 2px solid #a3cdf1 !important; /* إطار خفيف */
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    
    /* ضبط محاذاة نصوص العناوين لخانات البحث */
    div[data-testid="stTextInput"] label p {
        text-align: right !important;
        font-size: 16px !important;
    }
    
    /* ضبط محاذاة جداول البيانات */
    div[data-testid="stDataFrame"] {
        direction: RTL !important;
    }
    th, td {
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
        
        # إدارة حالة نص البحث والمحو للمواد
        if "mat_query" not in st.session_state:
            st.session_state.mat_query = ""
            
        search_mat = st.text_input("اكتب كلمة دلالية للبحث في المواد (مثل: إجازة، نقل، تجربة):", value=st.session_state.mat_query, key="mat_input")
        st.session_state.mat_query = search_mat

        # زر مسح كلمة البحث للمواد
        if st.button("🗑️ مسح كلمة البحث عن المواد"):
            st.session_state.mat_query = ""
            st.rerun()
        
        # تصفية الجدول بناءً على البحث وإظهاره في الأسفل
        if st.session_state.mat_query:
            filtered_mat = materials[materials.astype(str).apply(lambda x: x.str.contains(st.session_state.mat_query, case=False)).any(axis=1)]
            st.dataframe(filtered_mat, use_container_width=True)
        else:
            st.dataframe(materials, use_container_width=True)

    with tab2:
        st.subheader("ابحث عن أي مخالفة لمعرفة عقوبتها")
        
        # إدارة حالة نص البحث والمحو للعقوبات
        if "pen_query" not in st.session_state:
            st.session_state.pen_query = ""

        search_pen = st.text_input("اكتب كلمة دلالية للبحث في العقوبات (مثل: غياب، تأخر، زي، تدخين):", value=st.session_state.pen_query, key="pen_input")
        st.session_state.pen_query = search_pen

        # زر مسح كلمة البحث للعقوبات
        if st.button("🗑️ مسح كلمة البحث عن العقوبات"):
            st.session_state.pen_query = ""
            st.rerun()
        
        # تصفية جدول العقوبات وإظهاره في الأسفل
        if st.session_state.pen_query:
            filtered_pen = penalties[penalties.astype(str).apply(lambda x: x.str.contains(st.session_state.pen_query, case=False)).any(axis=1)]
            st.dataframe(filtered_pen, use_container_width=True)
        else:
            st.dataframe(penalties, use_container_width=True)

except FileNotFoundError:
    st.error("يرجى التأكد من أن ملف الإكسل مرفوع باسم 'لائحة_الموارد_البشرية.xlsx' في المستودع.")
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف، تأكد من تسمية الصفحات بـ 'المواد' و 'العقوبات'. التفاصيل: {e}")
