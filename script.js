// ==============================
// قائمة الأسئلة
// ==============================
const questions = [
    "هل يوجد تورّم عميق تحت الجلد؟",
    "هل التورّم في العين/الشفاه/اللسان؟",
    "هل التورّم ناعم وسلس بدون قشور؟",
    "هل يوجد حرقان بدون ألم شديد؟",
    "هل ظهر التورّم فجأة خلال ساعات؟",
    "هل لا توجد حكة شديدة؟",
    "هل التورّم بلا حدود واضحة؟",
    "هل التورّم أكبر من الاحمرار؟",
    "هل يوجد تورّم في اللسان أو الشفتين؟",
    "هل بدأ التورّم بعد دواء / أكل / لسعة؟"
];

let answers = [];
let currentQuestion = 0;
let aiResult = "";

// ==============================
// معاينة الصورة عند الاختيار
// ==============================
document.getElementById("imageInput").addEventListener("change", function () {
    let file = this.files[0];
    if (!file) return;

    let reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById("preview").innerHTML = `<img src="${e.target.result}" alt="الصورة المختارة">`;
    };
    reader.readAsDataURL(file);
});

// ==============================
// رفع الصورة + الاتصال بالـ API
// ==============================
async function analyzeImage() {
    let file = document.getElementById("imageInput").files[0];
    if (!file) {
        alert("⚠️ من فضلك اختر صورة أولاً");
        return;
    }

    // إخفاء النتائج السابقة
    document.getElementById("questionsBox").style.display = "none";
    document.getElementById("finalDiagnosis").innerHTML = "";
    document.getElementById("result").innerHTML = "⏳ جاري التحليل...";

    let form = new FormData();
    form.append("file", file);

    try {
        let res = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            body: form
        });

        if (!res.ok) {
            throw new Error("السيرفر لا يعمل");
        }

        let data = await res.json();
        aiResult = data.prediction;

        // عرض نتيجة التحليل
        let resultColor = "#1a1a2e";
        if (aiResult === "angioedema") resultColor = "#dc3545";
        else if (aiResult === "normal") resultColor = "#28a745";
        else if (aiResult === "not_angioedema") resultColor = "#fd7e14";

        document.getElementById("result").innerHTML = `
            <div style="border-right: 4px solid ${resultColor}; padding: 12px;">
                <strong>🤖 نتيجة الذكاء الاصطناعي:</strong><br>
                🩺 التشخيص: <span style="color: ${resultColor}; font-weight: bold;">${aiResult}</span><br>
                📊 نسبة الثقة: ${data.confidence}
            </div>
        `;

        // ظهور الأسئلة لو النتيجة تحتاجها
        if (aiResult === "angioedema" || aiResult === "not_angioedema") {
            startQuestions();
        } else {
            showFinalDiagnosis(aiResult, 0);
        }

    } catch (error) {
        document.getElementById("result").innerHTML = `
            <div style="color: red; padding: 12px;">
                ❌ خطأ: تأكد من تشغيل السيرفر على port 8000<br>
                ${error.message}
            </div>
        `;
        console.error(error);
    }
}

// ==============================
// بدء الأسئلة
// ==============================
function startQuestions() {
    currentQuestion = 0;
    answers = [];
    document.getElementById("questionsBox").style.display = "block";
    showNextQuestion();
}

// ==============================
// عرض سؤال واحد في كل مرة
// ==============================
function showNextQuestion() {
    if (currentQuestion < questions.length) {
        document.getElementById("questionText").innerHTML = questions[currentQuestion];
    } else {
        finishDiagnosis();
    }
}

// ==============================
// أزرار نعم / لا
// ==============================
function answer(value) {
    answers.push(value);
    currentQuestion++;
    showNextQuestion();
}

// ==============================
// التشخيص النهائي
// ==============================
function finishDiagnosis() {
    let score = answers.filter(a => a === true).length;
    let finalDiagnosis;

    if (aiResult === "normal" || aiResult === "other") {
        finalDiagnosis = aiResult;
    } else {
        finalDiagnosis = score >= 6 ? "angioedema" : "not_angioedema";
    }

    showFinalDiagnosis(finalDiagnosis, score);
}

// ==============================
// عرض التشخيص النهائي
// ==============================
function showFinalDiagnosis(diagnosis, score) {
    let diagnosisText = "";
    let diagnosisClass = "";

    switch (diagnosis) {
        case "angioedema":
            diagnosisText = "⚠️ وذمة وعائية - يُرجى استشارة الطبيب";
            diagnosisClass = "diagnosis-angioedema";
            break;
        case "normal":
            diagnosisText = "✅ طبيعي - لا توجد علامات للوذمة";
            diagnosisClass = "diagnosis-normal";
            break;
        case "not_angioedema":
            diagnosisText = "🟡 ليس وذمة وعائية - قد يكون سبب آخر";
            diagnosisClass = "diagnosis-not_angioedema";
            break;
        case "other":
            diagnosisText = "🔘 حالة أخرى ";
            diagnosisClass = "diagnosis-other";
            break;
        default:
            diagnosisText = diagnosis;
            diagnosisClass = "diagnosis-other";
    }

    let scoreText = score > 0 ? `<br>📊 نتيجة الأسئلة: ${score}/10` : "";
    
    document.getElementById("finalDiagnosis").innerHTML = `
        <div class="${diagnosisClass}" style="padding: 15px; border-radius: 12px;">
            <strong>🩺 التشخيص النهائي:</strong><br>
            ${diagnosisText}${scoreText}
        </div>
    `;
}