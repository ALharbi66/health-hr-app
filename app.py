import streamlit as st
import pandas as pd

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستشار لائحة الصحة القابضة", layout="wide")

# تطبيق التنسيق الشامل لتلوين خانات البحث وضبط المحاذاة
st.markdown(
    """
    <style>
    /* تلوين وتظليل خانة البحث بلون متميز وجذاب */
    div[data-testid="stTextInput"] input {
        background-color: #eef7f4 !important; /* لون تظليل هادئ ومميز */
        border: 2px solid #2e7d32 !important; /* إطار أخضر خفيف */
        border-radius: 8px !important;
        font-weight: bold !important;
        color: #1b5e20 !important;
    }
    
    /* ضبط محاذاة نصوص العناوين لخانات البحث */
    div[data-testid="stTextInput"] label p {
        font-size: 16px !important;
        font-weight: bold !important;
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
        
        # إدارة حالة نص البحث والمحو للمواد
        if "mat_query" not in st.session_state:
            st.session_state.mat_query = ""
            
        search_mat = st.text_input("اكتب كلمة دلالية للبحث في المواد (مثل: إجازة، نقل، تجربة):", value=st.session_state.mat_query, key="mat_input")
        st.session_state.mat_query = search_mat

        # زر مسح كلمة البحث للمواد
        if st.button("🗑️ مسح كلمة البحث عن المواد"):
            st.session_state.mat_query = ""
            st.rerun()
        
        # تصفية الجدول وقلب ترتيب الأعمدة برمجياً لتبدأ من اليمين (الرقم -> الموضوع -> النص)
        if st.session_state.mat_query:
            filtered_mat = materials[materials.astype(str).apply(lambda x: x.str.contains(st.session_state.mat_query, case=False)).any(axis=1)]
            # إعادة ترتيب الأعمدة لتجبر إكسل وبايثون على عرضها من اليمين لليسار
            display_mat = filtered_mat[['الرقم', 'الموضوع', 'النص القانوني ومضمون المادة']]
            st.dataframe(display_mat, use_container_width=True)
        else:
            display_mat = materials[['الرقم', 'الموضوع', 'النص القانوني ومضمون المادة']]
            st.dataframe(display_mat, use_container_width=True)

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
        
        # تصفية جدول العقوبات وقلب ترتيب الأعمدة برمجياً
        columns_order_pen = ['الرقم', 'نوع وتصنيف المخالفة', 'وصف المخالفة الدقيق', 'العقوبة الأولى', 'العقوبة الثانية', 'العقوبة الثالثة', 'العقوبة الرابعة', 'ملاحظات مشتركة وإضافية']
        
        if st.session_state.pen_query:
            filtered_pen = penalties[penalties.astype(str).apply(lambda x: x.str.contains(st.session_state.pen_query, case=False)).any(axis=1)]
            display_pen = filtered_pen[columns_order_pen]
            st.dataframe(display_pen, use_container_width=True)
        else:
            display_pen = penalties[columns_order_pen]
            st.dataframe(display_pen, use_container_width=True)

except FileNotFoundError:
    st.error("يرجى التأكد من أن ملف الإكسل مرفوع باسم 'لائحة_الموارد_البشرية.xlsx' في المستودع.")
except Exception as e:
    st.error(f"حدث خطأ أثناء قراءة الملف، تأكد من تسمية الصفحات بـ 'المواد' و 'العقوبات'. التفاصيل: {e}")
