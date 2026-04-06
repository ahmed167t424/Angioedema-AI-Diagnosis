import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import os

# ================================
# PATHS
# ================================
BASE_DIR = os.path.dirname(__file__)
data_dir = os.path.join(BASE_DIR, "dataset")
model_dir = os.path.join(BASE_DIR, "model")

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

IMG_SIZE = 300   # EfficientNet-B3 recommended size

# ================================
# TRANSFORMS
# ================================
train_transforms = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomRotation(35),
    transforms.RandomPerspective(distortion_scale=0.45, p=0.5),
    transforms.RandomAffine(
        degrees=25,
        translate=(0.15, 0.15),
        scale=(0.75, 1.2),
        shear=15,
    ),
    transforms.RandomResizedCrop(
        IMG_SIZE,
        scale=(0.55, 1.0),
        ratio=(0.75, 1.3)
    ),
    transforms.RandomHorizontalFlip(p=0.6),
    transforms.ColorJitter(
        brightness=0.40,
        contrast=0.40,
        saturation=0.35,
        hue=0.02
    ),
    transforms.GaussianBlur(kernel_size=3, sigma=(0.3, 1.5)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

test_transforms = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])

# ================================
# LOAD DATASET
# ================================
dataset = datasets.ImageFolder(root=data_dir, transform=train_transforms)

# ✅ عدد الكلاسات تلقائيًا
num_classes = len(dataset.classes)
print("✅ Classes detected:", dataset.classes)

# Split dataset
train_size = int(0.85 * len(dataset))
test_size = len(dataset) - train_size

train_data, test_data = random_split(dataset, [train_size, test_size])

# Apply test transforms
test_data.dataset.transform = test_transforms

# DataLoaders
train_loader = DataLoader(train_data, batch_size=8, shuffle=True)
test_loader = DataLoader(test_data, batch_size=8, shuffle=False)

print("Train Samples:", len(train_data))
print("Test Samples :", len(test_data))

# ================================
# DEVICE
# ================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

# ================================
# MODEL — EfficientNet-B3
# ================================
model = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.DEFAULT)

# ✅ Fine-tune last 60 layers
for param in list(model.parameters())[:-60]:
    param.requires_grad = False

# ✅ Replace classifier for multi-class
num_f = model.classifier[1].in_features
model.classifier[1] = nn.Linear(num_f, num_classes)

model = model.to(device)

# ================================
# LOSS + OPTIMIZER + LR Scheduler
# ================================
criterion = nn.CrossEntropyLoss()

optimizer = optim.AdamW(
    model.parameters(),
    lr=3e-5,
    weight_decay=0.0005
)

scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
    optimizer,
    T_0=5,
    T_mult=2
)

# ================================
# TRAIN LOOP
# ================================
epochs = 40
best_loss = float("inf")

for epoch in range(epochs):

    model.train()
    running_loss = 0
    correct = 0
    total = 0

    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    train_acc = (correct / total) * 100
    avg_loss = running_loss / len(train_loader)

    scheduler.step(epoch)

    print(f"Epoch [{epoch+1}/{epochs}]  Loss: {avg_loss:.4f} | Accuracy: {train_acc:.2f}%")

    # ✅ Save best model
    if avg_loss < best_loss:
        best_loss = avg_loss
        save_path = os.path.join(model_dir, "angio_model_best.pth")
        torch.save(model.state_dict(), save_path)
        print("✅ Best model saved!")

print("\n✅ Multi-Class Training Finished.")
