# 🧠 AI Angioedema Diagnosis System  
## نظام تشخيص الوذمة الوعائية باستخدام الذكاء الاصطناعي

---

# ✅ 1) مقدمة — Introduction

هذا المشروع يهدف إلى تطوير نظام ذكي لتشخيص **الوذمة الوعائية (Angioedema)**  
عن طريق:

- تحليل صورة الوجه باستخدام نموذج EfficientNet‑B3
- طرح 10 أسئلة إكلينيكية (Clinical Questions)
- دمج نتيجة الذكاء الاصطناعي + نتيجة الأسئلة للحصول على تشخيص نهائي أدق

تم بناء النظام باستخدام:

- 🧠 Python + PyTorch (للذكاء الاصطناعي)
- 🚀 FastAPI (لبناء الـ API)
- 🌐 HTML/CSS/JS (لبناء واجهة الويب)

---

# ✅ 2) مميزات النظام — Features

- تحليل صورة الوجه وتحديد 4 فئات:
  - Angioedema
  - Not Angioedema
  - Normal
  - Other
- واجهة ويب لرفع الصورة ومعرفة النتيجة
- أسئلة طبية تظهر سؤال–سؤال
- حساب Score والتشخيص النهائي
- API جاهز للربط مع أي موقع أو تطبيق

---

# ✅ 3) بنية المشروع — Project Structure

```

Angioedema-AI-Diagnosis/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── model/
│       └── (فارغ — ملف الـ pth موجود في Release)
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── ai/
│   └── train.py
│
└── README.md

````

---

# ✅ 4) تحميل الموديل — Download Model (angio_model_best.pth)

لأن ملف الموديل حجمه كبير، فهو مرفوع داخل قسم **Releases** في GitHub.

📌 **رابط التحميل المباشر:**

🔗 **Download:**  
https://github.com/ahmed167t424/Angioedema-AI-Diagnosis/releases/download/v1/angio_model_best.pth

✅ **ملاحظة:**  
عدّل `USERNAME` ليكون اسم حساب GitHub الخاص بك.

---

# ✅ 5) تشغيل الـ API — Run Backend API

## ✅ تثبيت المتطلبات
من داخل مجلد backend:

```bash
cd backend
pip install -r requirements.txt
````

## ✅ تشغيل السيرفر

```bash
uvicorn main:app --port 8000 --reload
```

ثم افتح:

    http://127.0.0.1:8000/docs

ستظهر صفحة Swagger لتجربة رفع الصور.

***

# ✅ 6) تشغيل واجهة الويب — Run Frontend

افتح الملف:

    frontend/index.html

ثم:

1.  اختر صورة من جهازك
2.  اضغط "تحليل الصورة"
3.  تظهر نتيجة الذكاء الاصطناعي
4.  تبدأ الأسئلة في الظهور بشكل تفاعلي
5.  يظهر التشخيص النهائي

***

# ✅ 7) شرح الموديل — AI Model Details

*   النموذج المستخدم: **EfficientNet-B3**
*   عدد الفئات: 4
*   تم تدريب النموذج على بيانات طبية مصنّفة
*   Preprocessing:
    *   Resize 300×300
    *   Normalize
    *   ToTensor

### ✅ حفظ النموذج

    angio_model_best.pth

### ✅ تحميل النموذج داخل الـ API

```python
model.load_state_dict(torch.load("model/angio_model_best.pth", map_location="cpu"))
model.eval()
```

***

# ✅ 8) منطق الأسئلة الإكلينيكية — Clinical Logic

بعد تحليل الصورة:

✅ لو النتيجة = Normal أو Other →  
لا حاجة للأسئلة → يتم عرض النتيجة مباشرة.

✅ لو النتيجة = Angioedema أو Not Angioedema →  
تظهر الأسئلة (10 أسئلة طبية).

بعدها يتم الحساب:

    Score = عدد الإجابات التي كانت True

### ✅ التشخيص النهائي:

*   إذا **Score ≥ 6** → التشخيص: Angioedema
*   إذا **Score < 6** → التشخيص: Not Angioedema

> المنطق الطبي يعتمد على تجميع الأدلة (Evidence Accumulation)  
> لذلك لابد أن تظهر أغلب العلامات وليس بعضها فقط.

***

# ✅ 9) تشغيل المشروع بالكامل — Full System Run

1.  شغّل API
2.  افتح الواجهة
3.  ارفع صورة
4.  انتظر تحليل AI
5.  جاوب الأسئلة
6.  يظهر التشخيص النهائي

***

# ✅ 10) التقنيات المستخدمة — Tech Stack

*   Python
*   PyTorch
*   FastAPI
*   PIL
*   JavaScript
*   HTML
*   CSS
*   FileReader API
*   Fetch API

***

# ✅ 11) مطوّر المشروع — Author

Developed by: **Ahmed**  
Role: **AI Engineer — Graduation Project**  
Year: **2026**
تم التطوير بواسطة: **أحمد**
الوظيفة: **مهندس ذكاء اصطناعي - مشروع تخرج**
السنة: **2026**

***

# ✅ 12) License

This project is for educational and academic purposes.
هذا المشروع مخصص للأغراض التعليمية والأكاديمية.
