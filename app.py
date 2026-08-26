import streamlit as st
import pandas as pd

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستشار لائحة الصحة القابضة", layout="wide")

# إعداد أنماط التصميم (CSS) لضبط الواجهة وتلوين خانات البحث بدقة
st.markdown(
    """
    <style>
    /* تلوين وتظليل خانة البحث بلون متميز */
    div[data-testid="stTextInput"] input {
        background-color: #eef7f4 !important; /* لون تظليل أخضر هادئ */
        border: 2px solid #2e7d32 !important; 
        border-radius: 8px !important;
        font-weight: bold !important;
        color: #1b5e20 !important;
        text-align: right !important;
        direction: rtl !important;
    }
    
    /* تنسيق أزرار المسح */
    .stButton button {
        background-color: #ffebee !important;
        color: #c62828 !important;
        border: 1px solid #ef9a9a !important;
    }

    /* تنسيق جدول HTML المخصص ليدعم اليمني لليسار بنسبة 100% */
    .rtl-table {
        width: 100%;
        direction: rtl !important;
        text-align: right !important;
        border-collapse: collapse;
        margin-top: 15px;
        font-family: sans-serif;
    }
    .rtl-table th {
        background-color: #2e7d32;
        color: white;
        padding: 12px;
        border: 1px solid #ddd;
        text-align: right !important;
    }
    .rtl-table td {
        padding: 10px;
        border: 1px solid #ddd;
        text-align: right !important;
    }
    .rtl-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .rtl-table tr:hover {
        background-color: #f1f1f1;
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

        if st.button("🗑️ مسح كلمة البحث عن المواد"):
            st.session_state.mat_query = ""
            st.rerun()
        
        # تصفية وعرض المواد عبر جدول HTML المتوافق مع الـ RTL
        if st.session_state.mat_query:
            filtered_mat = materials[materials.astype(str).apply(lambda x: x.str.contains(st.session_state.mat_query, case=False)).any(axis=1)]
        else:
            materials
            filtered_mat = materials

        # تحويل الجدول إلى HTML لعرضه من اليمين لليسار إجبارياً
        html_mat = filtered_mat.to_html(classes='rtl-table', index=False)
        st.markdown(html_mat, unsafe_allow_html=True)

    with tab2:
        st.subheader("ابحث عن أي مخالفة لمعرفة عقوبتها")
        
        if "pen_query" not in st.session_state:
            st.session_state.pen_query = ""

        search_pen = st.text_input("اكتب كلمة دلالية للبحث في العقوبات (مثل: غياب، تأخر، زي، تدخين):", value=st.session_state.pen_query, key="pen_input")
        st.session_state.pen_query = search_pen

        if st.button("🗑️ مسح كلمة البحث عن العقوبات"):
            st.session_state.pen_query = ""
            st.rerun()
        
        # تصفية وعرض العقوبات عبر جدول HTML المتوافق مع الـ RTL
        if st.session_state.pen_query:
            filtered_pen = penalties[penalties.astype(str).apply(lambda x: x.str.contains(st.session_state.pen_query, case=False)).any(axis=1)]
        else:
            filtered_pen = penalties

        # تحويل جدول العقوبات إلى HTML
        html_pen = filtered_pen.to_html(classes='rtl-table', index=False)
        st.markdown(html_pen, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("يرجى التأكد من أن ملف الإكسل مرفوع باسم 'لائحة_الموارد_البشرية.xlsx' في المستودع.")
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف، تأكد من تسمية الصفحات بـ 'المواد' و 'العقوبات'. التفاصيل: {e}")
