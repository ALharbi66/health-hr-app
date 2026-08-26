import streamlit as st
import pandas as pd
import json

# إعداد واجهة التطبيق
st.set_page_config(page_title="مستشار لائحة الصحة القابضة", layout="wide")

@st.cache_data
def load_data():
    file_name = "لائحة_الموارد_البشرية.xlsx"
    materials_df = pd.read_excel(file_name, sheet_name="المواد")
    penalties_df = pd.read_excel(file_name, sheet_name="العقوبات")
    return materials_df, penalties_df

try:
    materials, penalties = load_data()
    
    # تحويل البيانات إلى جيسون لسرعة البحث المحلى في المتصفح
    materials_json = materials.to_json(orient="records", force_ascii=False)
    penalties_json = penalties.to_json(orient="records", force_ascii=False)

    st.title("🔍 نظام البحث الذكي في لائحة الموارد البشرية")

    # كود الواجهة مقسم بشكل نصوص بسيطة ومستقلة تماماً لمنع أي تعارض في الرموز
    part1 = '<div dir="rtl" style="font-family:sans-serif; text-align:right; padding:15px;">'
    part2 = '<div style="margin-bottom:20px; display:flex; gap:10px;">'
    part3 = '<button id="btn1" onclick="tab(\'m\')" style="padding:10px 20px; font-weight:bold; background:#2e7d32; color:white; border:none; border-radius:5px; cursor:pointer;">📄 البحث في المواد القانونية</button>'
    part4 = '<button id="btn2" onclick="tab(\'p\')" style="padding:10px 20px; font-weight:bold; background:#f5f5f5; color:#333; border:1px solid #ccc; border-radius:5px; cursor:pointer;">⚠️ البحث في المخالفات والعقوبات</button>'
    part5 = '</div>'
    
    # واجهة المواد
    part6 = '<div id="secM"><h3>ابحث عن أي موضوع أو رقم مادة</h3>'
    part7 = '<div style="display:flex; gap:10px; margin-bottom:20px;">'
    part8 = '<input type="text" id="inM" onkeyup="srcM()" placeholder="اكتب للبحث..." style="flex:1; padding:12px; border:2px solid #2e7d32; border-radius:6px; background:#eef7f4; font-weight:bold; text-align:right; direction:rtl;">'
    part9 = '<button onclick="clr(\'inM\',\'m\')" style="padding:12px 25px; font-weight:bold; background:#ffebee; color:#c62828; border:1px solid #ef9a9a; border-radius:6px; cursor:pointer;">مسح البحث</button>'
    part10 = '</div><div style="overflow-x:auto;"><table class="tbl" style="width:100%; border-collapse:collapse; direction:rtl; text-align:right;">'
    part11 = '<thead style="background:#2e7d32; color:white;"><tr><th style="padding:12px; border:1px solid #ddd;">الرقم</th><th style="padding:12px; border:1px solid #ddd;">الموضوع</th><th style="padding:12px; border:1px solid #ddd;">النص القانوني ومضمون المادة</th></tr></thead>'
    part12 = '<tbody id="bM"></tbody></table></div></div>'
    
    # واجهة العقوبات
    part13 = '<div id="secP" style="display:none;"><h3>ابحث عن أي مخالفة لمعرفة عقوبتها</h3>'
    part14 = '<div style="display:flex; gap:10px; margin-bottom:20px;">'
    part15 = '<input type="text" id="inP" onkeyup="srcP()" placeholder="اكتب للبحث..." style="flex:1; padding:12px; border:2px solid #c62828; border-radius:6px; background:#fdf2f2; font-weight:bold; text-align:right; direction:rtl;">'
    part16 = '<button onclick="clr(\'inP\',\'p\')" style="padding:12px 25px; font-weight:bold; background:#ffebee; color:#c62828; border:1px solid #ef9a9a; border-radius:6px; cursor:pointer;">مسح البحث</button>'
    part17 = '</div><div style="overflow-x:auto;"><table class="tbl" style="width:100%; border-collapse:collapse; direction:rtl; text-align:right;">'
    part18 = '<thead style="background:#c62828; color:white;"><tr><th style="padding:10px; border:1px solid #ddd;">الرقم</th><th style="padding:10px; border:1px solid #ddd;">نوع وتصنيف المخالفة</th><th style="padding:10px; border:1px solid #ddd;">وصف المخالفة الدقيق</th><th style="padding:10px; border:1px solid #ddd;">العقوبة الأولى</th><th style="padding:10px; border:1px solid #ddd;">العقوبة الثانية</th><th style="padding:10px; border:1px solid #ddd;">العقوبة الثالثة</th><th style="padding:10px; border:1px solid #ddd;">العقوبة الرابعة</th><th style="padding:10px; border:1px solid #ddd;">ملاحظات مشتركة وإضافية</th></tr></thead>'
    part19 = '<tbody id="bP"></tbody></table></div></div></div>'

    # الأنماط البرمجية والتنسيقات
    css_style = '<style>.tbl tr:nth-child(even){background:#f9f9f9;} .tbl tr:hover{background:#f1f1f1;} .tbl td{padding:10px; border:1px solid #ddd; text-align:right; font-size:14px;}</style>'

    # أكواد الجافا سكريبت المفصولة والمؤمنة بالكامل ضد أخطاء السلاسل النصية في بايثون
    js_script = """
    <script>
        const dM = DATA_MAT_PLACEHOLDER;
        const dP = DATA_PEN_PLACEHOLDER;

        function rM(d) {
            const b = document.getElementById("bM"); b.innerHTML = "";
            d.forEach(r => {
                b.innerHTML += "<tr><td style='font-weight:bold; white-space:nowrap;'>" + (r["الرقم"]||"") + "</td><td style='font-weight:bold; color:#2e7d32; white-space:nowrap;'>" + (r["الموضوع"]||"") + "</td><td>" + (r["النص القانوني ومضمون المادة"]||"") + "</td></tr>";
            });
        }

        function rP(d) {
            const b = document.getElementById("bP"); b.innerHTML = "";
            d.forEach(r => {
                b.innerHTML += "<tr><td>" + (r["الرقم"]||"") + "</td><td style='font-weight:bold;'>" + (r["نوع وتصنيف المخالفة"]||"") + "</td><td style='color:#b71c1c;\'>" + (r["وصف المخالفة الدقيق"]||"") + "</td><td>" + (r["العقوبة الأولى"]||"") + "</td><td>" + (r["العقوبة الثانية"]||"") + "</td><td>" + (r["العقوبة الثالثة"]||"") + "</td><td>" + (r["العقوبة الرابعة"]||"") + "</td><td style='font-size:12px; color:#666;'>" + (r["ملاحظات مشتركة وإضافية"]||"") + "</td></tr>";
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
                b1.style.background = "#2e7d32"; b1.style.color = "white";
                b2.style.background = "#f5f5f5"; b2.style.color = "#333"; b2.style.border = "1px solid #ccc";
            } else {
                sM.style.display = "none"; sP.style.display = "block";
                b2.style.background = "#c62828"; b2.style.color = "white";
                b1.style.background = "#f5f5f5"; b1.style.color = "#333"; b1.style.border = "1px solid #ccc";
            }
        }

        rM(dM);
        rP(dP);
    </script>
    """

    # تجميع الهيكل النهائي
    full_html = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16 + part17 + part18 + part19 + css_style + js_script
    
    # دمج بيانات ملف الإكسل داخل الكود بأمان
    full_html = full_html.replace("DATA_MAT_PLACEHOLDER", materials_json)
    full_html = full_html.replace("DATA_PEN_PLACEHOLDER", penalties_json)
    
    # تشغيل وعرض واجهة التطبيق
    st.components.v1.html(full_html, height=900, scrolling=True)

except FileNotFoundError:
    st.error("يرجى التأكد من أن ملف الإكسل مرفوع باسم 'لائحة_الموارد_البشرية.xlsx' في المستودع.")
except Exception as e:
    st.error(f"حدث خطأ في النظام. التفاصيل: {e}")
