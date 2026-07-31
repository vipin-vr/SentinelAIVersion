from ultralytics import YOLO

# Load pretrained YOLO11 Nano model
model = YOLO("yolo11n.pt")

# Train the model
model.train(
    data="dataset/data.yaml",
    epochs=20,
    imgsz=640,
    batch=8,
    project="runs",
    name="sentinel_ai"
)

print("Training Completed!")