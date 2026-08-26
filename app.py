import streamlit as st
import pandas as pd

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستشار لائحة الصحة القابضة", layout="wide")

# هندسة التصميم الحديث لإجبار كامل عناصر التطبيق على التحول من اليمين إلى اليسار (RTL)
st.markdown(
    """
    <style>
    /* 1. قلب اتجاه التطبيق بالكامل وكل الحاويات الداخلية */
    .stApp, [data-testid="stMain"], [data-testid="block-container"], .element-container {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* 2. ضبط اتجاه التبويبات (Tabs) لتنطلق من اليمين لليسار */
    div[data-testid="stTabs"] button {
        direction: rtl !important;
    }
    div[data-testid="stTabs"] {
        direction: rtl !important;
    }
    
    /* 3. تظليل وتلوين خانة البحث وضبط نصوصها من اليمين */
    div[data-testid="stTextInput"] input {
        background-color: #eef7f4 !important; /* لون تظليل أخضر هادئ */
        border: 2px solid #2e7d32 !important; 
        border-radius: 8px !important;
        font-weight: bold !important;
        color: #1b5e20 !important;
        text-align: right !important;
        direction: rtl !important;
    }
    
    /* 4. ضبط محاذاة العناوين التوضيحية فوق خانة البحث */
    div[data-testid="stTextInput"] label, div[data-testid="stTextInput"] p {
        text-align: right !important;
        direction: rtl !important;
        width: 100% !important;
    }
    
    /* 5. محاذاة أزرار المسح وتنسيقها لتظهر بشكل كامل ومتناسق */
    div.stButton button {
        width: 100% !important;
        background-color: #ffebee !important;
        color: #c62828 !important;
        border: 1px solid #ef9a9a !important;
        border-radius: 6px !important;
        font-weight: bold !important;
    }
    
    /* 6. إجبار نصوص خلايا وعناوين الجدول على المحاذاة اليمينية */
    th, td, .stDataFrame div {
        text-align: right !important;
        direction: rtl !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔍 نظام البحث الذكي في لائحة الموارد البشرية")

# قراءة البيانات من ملف الإكسل
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
        
        if "mat_query" not in st.session_state:
            st.session_state.mat_query = ""
            
        search_mat = st.text_input("اكتب كلمة دلالية للبحث في المواد (مثل: إجازة، نقل، تجربة):", value=st.session_state.mat_query, key="mat_input")
        st.session_state.mat_query = search_mat

        if st.button("🗑️ مسح البحث", key="clear_mat"):
            st.session_state.mat_query = ""
            st.rerun()
        
        # تصفية المواد
        if st.session_state.mat_query:
            filtered_mat = materials[materials.astype(str).apply(lambda x: x.str.contains(st.session_state.mat_query, case=False)).any(axis=1)]
        else:
            filtered_mat = materials

        # عرض الجدول العربي مع إخفاء عمود الترقيم التلقائي
        st.dataframe(filtered_mat, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("ابحث عن أي مخالفة لمعرفة عقوبتها")
        
        if "pen_query" not in st.session_state:
            st.session_state.pen_query = ""

        search_pen = st.text_input("اكتب كلمة دلالية للبحث في العقوبات (مثل: غياب، تأخر، زي، تدخين):", value=st.session_state.pen_query, key="pen_input")
        st.session_state.pen_query = search_pen

        if st.button("🗑️ مسح البحث", key="clear_pen"):
            st.session_state.pen_query = ""
            st.rerun()
        
        # تصفية جدول العقوبات
        if st.session_state.pen_query:
            filtered_pen = penalties[penalties.astype(str).apply(lambda x: x.str.contains(st.session_state.pen_query, case=False)).any(axis=1)]
        else:
            filtered_pen = penalties

        # عرض جدول العقوبات العربي مع إخفاء عمود الترقيم التلقائي
        st.dataframe(filtered_pen, use_container_width=True, hide_index=True)

except FileNotFoundError:
    st.error("يرجى التأكد من أن ملف الإكسل مرفوع باسم 'لائحة_الموارد_البشرية.xlsx' في المستودع.")
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف، تأكد من تسمية الصفحات بـ 'المواد' و 'العقوبات'. التفاصيل: {e}")
