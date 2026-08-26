import streamlit as st
import pandas as pd
import json

# إعداد واجهة التطبيق وحذف أي هوامش افتراضية للمنصة
st.set_page_config(page_title="مستشار لائحة الصحة القابضة", layout="wide")

# قراءة البيانات من ملف الإكسل
@st.cache_data
def load_data():
    file_name = "لائحة_الموارد_البشرية.xlsx"
    materials_df = pd.read_excel(file_name, sheet_name="المواد")
    penalties_df = pd.read_excel(file_name, sheet_name="العقوبات")
    return materials_df, penalties_df

try:
    materials, penalties = load_data()
    
    # تحويل البيانات إلى صيغة جافاسكريبت لتعمل محلياً بسرعة فائقة في المتصفح
    materials_json = materials.to_json(orient="records", force_ascii=False)
    penalties_json = penalties.to_json(orient="records", force_ascii=False)

    st.title("🔍 نظام البحث الذكي في لائحة الموارد البشرية")

    # بناء الواجهة بالكامل باستخدام الـ HTML و JavaScript لضمان الـ RTL بنسبة 100%
    html_code = f"""
    <div dir="rtl" style="font-family: sans-serif; text-align: right; background-color: #ffffff; padding: 15px; border-radius: 8px;">
        
        <!-- أزرار التنقل بين الأقسام -->
        <div style="margin-bottom: 20px; display: flex; gap: 10px;">
            <button id="btnTabs1" onclick="switchTab('tab1')" style="padding: 10px 20px; font-size: 16px; font-weight: bold; background-color: #2e7d32; color: white; border: none; border-radius: 5px; cursor: pointer;">📄 البحث في المواد القانونية</button>
            <button id="btnTabs2" onclick="switchTab('tab2')" style="padding: 10px 20px; font-size: 16px; font-weight: bold; background-color: #f5f5f5; color: #333; border: 1px solid #ccc; border-radius: 5px; cursor: pointer;">⚠️ البحث في المخالفات والعقوبات</button>
        </div>

        <!-- شاشة البحث في المواد -->
        <div id="sectionMaterials">
            <h3 style="color: #2e7d32; margin-bottom: 5px;">ابحث عن أي موضوع أو رقم مادة</h3>
            <p style="color: #666; font-size: 14px; margin-top: 0;">اكتب كلمة دلالية للبحث في المواد (مثل: إجازة، نقل، تجربة):</p>
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <input type="text" id="inputMat" onkeyup="searchMaterials()" placeholder="اكتب للبحث..." style="flex: 1; padding: 12px; font-size: 16px; border: 2px solid #2e7d32; border-radius: 6px; background-color: #eef7f4; font-weight: bold; color: #1b5e20; text-align: right; direction: rtl;">
                <button onclick="clearSearch('inputMat', 'tableMaterials', 'mat')" style="padding: 12px 25px; font-size: 16px; font-weight: bold; background-color: #ffebee; color: #c62828; border: 1px solid #ef9a9a; border-radius: 6px; cursor: pointer;">مسح البحث</button>
            </div>
            <div style="overflow-x: auto;">
                <table class="custom-table" id="tableMaterials" style="width: 100%; border-collapse: collapse; margin-top: 10px; direction: rtl; text-align: right;">
                    <thead>
                        <tr style="background-color: #2e7d32; color: white;">
                            <th style="padding: 12px; border: 1px solid #ddd; text-align: right;">الرقم</th>
                            <th style="padding: 12px; border: 1px solid #ddd; text-align: right;">الموضوع</th>
                            <th style="padding: 12px; border: 1px solid #ddd; text-align: right;">النص القانوني ومضمون المادة</th>
                        </tr>
                    </thead>
                    <tbody id="tbodyMat"></tbody>
                </table>
            </div>
        </div>

        <!-- شاشة البحث في العقوبات -->
        <div id="sectionPenalties" style="display: none;">
            <h3 style="color: #c62828; margin-bottom: 5px;">ابحث عن أي مخالفة لمعرفة عقوبتها</h3>
            <p style="color: #666; font-size: 14px; margin-top: 0;">اكتب كلمة دلالية للبحث في العقوبات (مثل: غياب، تأخر، زي، تدخين):</p>
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <input type="text" id="inputPen" onkeyup="searchPenalties()" placeholder="اكتب للبحث..." style="flex: 1; padding: 12px; font-size: 16px; border: 2px solid #c62828; border-radius: 6px; background-color: #fdf2f2; font-weight: bold; color: #b71c1c; text-align: right; direction: rtl;">
                <button onclick="clearSearch('inputPen', 'tablePenalties', 'pen')" style="padding: 12px 25px; font-size: 16px; font-weight: bold; background-color: #ffebee; color: #c62828; border: 1px solid #ef9a9a; border-radius: 6px; cursor: pointer;">مسح البحث</button>
            </div>
            <div style="overflow-x: auto;">
                <table class="custom-table" id="tablePenalties" style="width: 100%; border-collapse: collapse; margin-top: 10px; direction: rtl; text-align: right;">
                    <thead>
                        <tr style="background-color: #c62828; color: white;">
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">الرقم</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">نوع وتصنيف المخالفة</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">وصف المخالفة الدقيق</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">العقوبة الأولى</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">العقوبة الثانية</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">العقوبة الثالثة</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">العقوبة الرابعة</th>
                            <th style="padding: 10px; border: 1px solid #ddd; text-align: right;">ملاحظات مشتركة وإضافية</th>
                        </tr>
                    </thead>
                    <tbody id="tbodyPen"></tbody>
                </table>
            </div>
        </div>
    </div>

    <style>
        .custom-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .custom-table tr:hover {{ background-color: #f1f1f1; }}
        .custom-table td {{ padding: 10px; border: 1px solid #ddd; text-align: right; font-size: 14px; }}
    </style>

    <script>
        // تحميل البيانات من البايثون إلى المتصفح مباشرة
        const materialsData = {materials_json};
        const penaltiesData = {penalties_json};

        // دالة تعبئة جدول المواد القانونية
        function renderMaterials(data) {{
            const tbody = document.getElementById('tbodyMat');
            tbody.innerHTML = '';
            data.forEach(row => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="font-weight:bold; white-space:nowrap;">${{row['الرقم'] || ''}}</td>
                    <td style="font-weight:bold; color:#2e7d32; white-space:nowrap;">${{row['الموضوع'] || ''}}</td>
                    <td>${{row['النص القانوني ومضمون المادة'] || ''}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // دالة تعبئة جدول العقوبات
        function renderPenalties(data) {{
            const tbody = document.getElementById('tbodyPen');
            tbody.innerHTML = '';
            data.forEach(row => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${{row['الرقم'] || ''}}</td>
                    <td style="font-weight:bold;">${{row['نوع وتصنيف المخالفة'] || ''}}</td>
                    <td style="color:#b71c1c;">${{row['وصف المخالفة الدقيق'] || ''}}</td>
                    <td>${{row['العقوبة الأولى'] || ''}}</td>
                    <td>${{row['العقوبة الثانية'] || ''}}</td>
                    <td>${{row['العقوبة الثالثة'] || ''}}</td>
                    <td>${{row['العقوبة الرابعة'] || ''}}</td>
                    <td style="font-size:12px; color:#666;">${{row['ملاحظات مشتركة وإضافية'] || ''}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // دوال البحث الفوري السريع جداً وبدون استخدام السيرفر
        function searchMaterials() {{
            const query = document.getElementById('inputMat').value.toLowerCase();
            const filtered = materialsData.filter(row => 
                String(row['الرقم']).toLowerCase().includes(query) ||
                String(row['الموضوع']).toLowerCase().includes(query) ||
                String(row['النص القانوني ومضمون المادة']).toLowerCase().includes(query)
            );
            renderMaterials(filtered);
        }}

        function searchPenalties() {{
            const query = document.getElementById('inputPen').value.toLowerCase();
            const filtered = penaltiesData.filter(row => 
                String(row['نوع وتصنيف المخالفة']).toLowerCase().includes(query) ||
                String(row['وصف المخالفة الدقيق']).toLowerCase().includes(query) ||
                String(row['العقوبة الأولى']).toLowerCase().includes(query)
            );
            renderPenalties(filtered);
        }}

        // دالة مسح خانة البحث وإعادة الجداول كاملة
        function clearSearch(inputId, tableId, type) {{
            document.getElementById(inputId).value = '';
            if(type === 'mat') {{ renderMaterials(materialsData); }}
            else {{ renderPenalties(penaltiesData); }}
        }}

        // دالة التنقل بين التبويبات وتغيير مظهر الأزرار
        function switchTab(tab) {{
            const matSec = document.getElementById('sectionMaterials');
            const penSec = document.getElementById('sectionPenalties');
            const btn1 = document.getElementById('btnTabs1');
            const btn2 = document.getElementById('btnTabs2');

            if(tab === 'tab1') {{
                matSec.style.display = 'block';
                penSec.style.display = 'none';
                btn1.style.background = '#2e7d32'; btn1.style.color = 'white';
