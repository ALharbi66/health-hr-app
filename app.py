import streamlit as st
import pandas as pd
import json

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستشار لائحة الصحة القابضة - تجمع المدينة المنورة", layout="wide")

@st.cache_data
def load_data():
    file_name = "لائحة_الموارد_البشرية.xlsx"
    materials_df = pd.read_excel(file_name, sheet_name="المواد")
    penalties_df = pd.read_excel(file_name, sheet_name="العقوبات")
    return materials_df, penalties_df

try:
    materials, penalties = load_data()
    materials_json = materials.to_json(orient="records", force_ascii=False)
    penalties_json = penalties.to_json(orient="records", force_ascii=False)

    # 1. تصميم الهيدر برمجياً بالكامل (رسم الشعار والتموجات والانسيابيات الزرقاء الرسمية وتناسق الخطوط)
    st.markdown(
        """
        <div dir="rtl" style="
            background: linear-gradient(135deg, #e0f2fe 0%, #f0fdf4 50%, #ffffff 100%);
            border: 2px solid #bae6fd;
            border-radius: 12px;
            padding: 25px 35px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 25px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        ">
            <!-- الجهة اليمنى: الشعار النجمي وتجمع المدينة المنورة الصحي -->
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="
                    width: 75px;
                    height: 75px;
                    background: radial-gradient(circle, #0052cc 20%, #3399ff 60%, transparent 85%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <!-- تمثيل الشعار النجمي الخماسي للتجمع برمجياً -->
                    <span style="color: white; font-size: 35px; font-weight: bold; line-height: 1;">❄️</span>
                </div>
                <div style="text-align: right;">
                    <h2 style="margin: 0; color: #003366; font-size: 26px; font-weight: 800; letter-spacing: -0.5px;">تجمع المدينة المنورة الصحي</h2>
                    <p style="margin: 1px 0 0 0; color: #3399ff; font-size: 13px; font-weight: 600; font-family: monospace;">Madinah Health Cluster</p>
                </div>
            </div>
            
            <!-- الجهة اليسرى: الإدارات الفرعية بخطوط صغيرة متناسقة جداً ومحاذية لليسار -->
            <div style="text-align: left; border-right: 4px solid #3399ff; padding-right: 20px;">
                <h3 style="margin: 0; color: #0f172a; font-size: 16px; font-weight: bold; letter-spacing: 0.5px;">إدارة الحج والعمرة</h3>
                <h4 style="margin: 5px 0 0 0; color: #64748b; font-size: 13px; font-weight: 600;">الموارد البشرية</h4>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. عنوان النظام الموسط تماماً وبخط رسمي فخم وعريض ومطابق لطلبك
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px; margin-bottom: 40px;">
            <h1 style="
                color: #003366; 
                font-family: 'Times New Roman', Times, serif; 
                font-weight: bold; 
                font-size: 38px; 
                border-bottom: 4px double #0066cc; 
                padding-bottom: 15px; 
                display: inline-block;
                letter-spacing: 0.5px;
            ">
                نظام البحث الذكي في لائحة الموارد البشرية
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # كود الواجهة التفاعلية السريعة (RTL 100%) ومحرك البحث
    part1 = '<div dir="rtl" style="font-family:sans-serif; text-align:right; padding:5px;">'
    tabs_part = """
    <div style="margin-bottom:20px; display:flex; gap:10px;">
        <button id="btn1" onclick="tab('m')" style="padding:10px 20px; font-weight:bold; background:#0066cc; color:white; border:none; border-radius:5px; cursor:pointer;">📄 البحث في المواد القانونية</button>
        <button id="btn2" onclick="tab('p')" style="padding:10px 20px; font-weight:bold; background:#f5f5f5; color:#333; border:1px solid #ccc; border-radius:5px; cursor:pointer;">⚠️ البحث في المخالفات والعقوبات</button>
    </div>
    <div id="secM"><h3>ابحث عن أي موضوع أو رقم مادة</h3>
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <input type="text" id="inM" onkeyup="srcM()" placeholder="اكتب للبحث..." style="flex:1; padding:12px; border:2px solid #0066cc; border-radius:6px; background:#f0f4f8; font-weight:bold; text-align:right; direction:rtl; color:#003366;">
        <button onclick="clr('inM','m')" style="padding:12px 25px; font-weight:bold; background:#ffebee; color:#c62828; border:1px solid #ef9a9a; border-radius:6px; cursor:pointer;">مسح البحث</button>
    </div><div style="overflow-x:auto;"><table class="tbl" style="width:100%; border-collapse:collapse; direction:rtl; text-align:right;">
    <thead style="background:#0066cc; color:white;"><tr><th style="padding:12px; border:1px solid #ddd;">الرقم</th><th style="padding:12px; border:1px solid #ddd;">الموضوع</th><th style="padding:12px; border:1px solid #ddd;">النص القانوني ومضمون المادة</th></tr></thead>
    <tbody id="bM"></tbody></table></div></div>
    
    <div id="secP" style="display:none;"><h3>ابحث عن أي مخالفة لمعرفة عقوبتها</h3>
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <input type="text" id="inP" onkeyup="srcP()" placeholder="اكتب للبحث..." style="flex:1; padding:12px; border:2px solid #3399ff; border-radius:6px; background:#f0f8ff; font-weight:bold; text-align:right; direction:rtl; color:#003366;">
        <button onclick="clr('inP','p')" style="padding:12px 25px; font-weight:bold; background:#ffebee; color:#c62828; border:1px solid #ef9a9a; border-radius:6px; cursor:pointer;">مسح البحث</button>
    </div><div style="overflow-x:auto;"><table class="tbl" style="width:100%; border-collapse:collapse; direction:rtl; text-align:right;">
    <thead style="background:#3399ff; color:white;"><tr><th style="padding:10px; border:1px solid #ddd;">الرقم</th><th style="padding:10px; border:1px solid #ddd;">نوع وتصنيف المخالفة</th><th style="padding:10px; border:1px solid #ddd;">وصف المخالفة الدقيق</th><th style="padding:10px; border:1px solid #ddd;">العقوبة الأولى</th><th style="padding:10px; border:1px solid #ddd;">العقوبة الثانية</th><th style="padding:10px; border:1px solid #ddd;">العقوبة الثالثة</th><th style="padding:10px; border:1px solid #ddd;">العقوبة الرابعة</th><th style="padding:10px; border:1px solid #ddd;">ملاحظات مشتركة وإضافية</th></tr></thead>
    <tbody id="bP"></tbody></table></div></div></div>
    """

    css_style = '<style>.tbl tr:nth-child(even){background:#fcfdfe;} .tbl tr:hover{background:#f1f5f9;} .tbl td{padding:10px; border:1px solid #ddd; text-align:right; font-size:14px;}</style>'

    js_script = """
    <script>
        const dM = DATA_MAT_PLACEHOLDER;
        const dP = DATA_PEN_PLACEHOLDER;

        function rM(d) {
            const b = document.getElementById("bM"); b.innerHTML = "";
            d.forEach(r => {
                b.innerHTML += "<tr><td style='font-weight:bold; white-space:nowrap;'>" + (r["الرقم"]||"") + "</td><td style='font-weight:bold; color:#0066cc; white-space:nowrap;'>" + (r["الموضوع"]||"") + "</td><td>" + (r["النص القانوني ومضمون المادة"]||"") + "</td></tr>";
            });
        }

        function rP(d) {
            const b = document.getElementById("bP"); b.innerHTML = "";
            d.forEach(r => {
                b.innerHTML += "<tr><td>" + (r["الرقم"]||"") + "</td><td style='font-weight:bold;\'>" + (r["نوع وتصنيف المخالفة"]||"") + "</td><td style='color:#b71c1c;\'>" + (r["وصف المخالفة الدقيق"]||"") + "</td><td>" + (r["العقوبة الأولى"]||"") + "</td><td>" + (r["العقوبة الثانية"]||"") + "</td><td>" + (r["العقوبة الثالثة"]||"") + "</td><td>" + (r["العقوبة الرابعة"]||"") + "</td><td style='font-size:12px; color:#666;'>" + (r["ملاحظات مشتركة وإضافية"]||"") + "</td></tr>";
            });
        }

        function srcM() {
            const q = document.getElementById("inM").value.toLowerCase();
            const f = dM.filter(r => String(r["الرقم"]).toLowerCase().includes(q) || String(r["الموضوع"]).toLowerCase().includes(q) || String(r["النص القانوني ومضمون المادة"]).toLowerCase().includes(q));
            rM(f);
        }

        function srcP() {
            const q = document.getElementById("inP").value.toLowerCase();
            const f = dP.filter(r => String(r["نوع وتصنيف المخالفة"]).toLowerCase().includes(q) || String(r["وصف المخالفة الدقيق"]).toLowerCase().includes(q) || String(r["العقوبة الأولى"]).toLowerCase().includes(q));
            rP(f);
        }

        function clr(id, t) {
            document.getElementById(id).value = "";
            if(t === "m") { rM(dM); } else { rP(dP); }
        }

        function tab(t) {
            const sM = document.getElementById("secM"); const sP = document.getElementById("secP");
            const b1 = document.getElementById("btn1"); const b2 = document.getElementById("btn2");
            if(t === "m") {
                sM.style.display = "block"; sP.style.display = "none";
                b1.style.background = "#0066cc"; b1.style.color = "white";
                b2.style.background = "#f5f5f5"; b2.style.color = "#333"; b2.style.border = "1px solid #ccc";
            } else {
                sM.style.display = "none"; sP.style.display = "block";
                b2.style.background = "#3399ff"; b2.style.color = "white";
                b1.style.background = "#f5f5f5"; b1.style.color = "#333"; b1.style.border = "1px solid #ccc";
            }
        }

        rM(dM);
        rP(dP);
    </script>
    """

    full_html = part1 + tabs_part + css_style + js_script
