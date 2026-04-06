from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import io

app = FastAPI()

# السماح للموقع الاتصال
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# الكلاسات
# --------------------------
CLASSES = ["angioedema", "normal", "not_angioedema", "other"]

# --------------------------
# تحميل الموديل
# --------------------------
def load_model():
    model = models.efficientnet_b3(weights=None)
    n = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(n, 4)  # 4 كلاسات
    
    model.load_state_dict(torch.load(
        "model/angio_model_best.pth", 
        map_location=torch.device("cpu")
    ))
    model.eval()
    return model

model = load_model()

# --------------------------
# تجهيز الصورة
# --------------------------
transform = transforms.Compose([
    transforms.Resize((300, 300)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

def preprocess(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return transform(img).unsqueeze(0)

# --------------------------
# API: /predict
# --------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    tensor = preprocess(image_bytes)
    
    with torch.no_grad():
        output = model(tensor)
        probs = torch.softmax(output, dim=1)
        conf = float(probs.max().item()) * 100
        pred_idx = int(torch.argmax(probs))
    
    result = CLASSES[pred_idx]
    
    return {
        "prediction": result,
        "confidence": f"{conf:.2f}%"
    }

# --------------------------
# تشغيل: uvicorn main:app --reload
# --------------------------