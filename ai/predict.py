from ultralytics import YOLO
import sys
import os
import time

# -----------------------------
# Load trained model
# -----------------------------
model = YOLO("runs/detect/runs/sentinel_ai/weights/best.pt")

# -----------------------------
# Check image argument
# -----------------------------
if len(sys.argv) < 2:
    print("Usage:")
    print("python ai/predict.py image.jpg")
    exit()

image = sys.argv[1]

if not os.path.exists(image):
    print("Image not found:", image)
    exit()

print("\nLoading image:", image)

start = time.time()

# -----------------------------
# Run prediction
# -----------------------------
results = model.predict(
    source=image,
    conf=0.25,
    imgsz=640,
    iou=0.45,
    save=True,
    augment=False,
    verbose=False
)

print("\n========== Detection Results ==========\n")

total = 0

for result in results:

    if len(result.boxes) == 0:
        print("No objects detected.")
    else:
        for box in result.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            print(
                f"{model.names[cls]} : {conf:.2f}"
            )

            total += 1

    output_image = os.path.join(
        result.save_dir,
        os.path.basename(image)
    )

print("\n--------------------------------------")
print("Total Objects Detected :", total)
print("Output Image           :", output_image)
print("Prediction Time        : %.2f sec" % (time.time() - start))
print("--------------------------------------")
print("\nPrediction Completed Successfully!")