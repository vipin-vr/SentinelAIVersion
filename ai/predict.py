from ultralytics import YOLO
import sys
import os

# Load trained model
model = YOLO("runs/detect/runs/sentinel_ai/weights/best.pt")

# Check if image is provided
if len(sys.argv) < 2:
    print("Usage: python ai/predict.py image.jpg")
    exit()

image = sys.argv[1]

# Run prediction
results = model.predict(
    source=image,
    conf=0.05,
    save=True
)

print("\n========== Detection Results ==========\n")

total = 0

for result in results:

    boxes = result.boxes

    if len(boxes) == 0:
        print("No objects detected.")
    else:
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            print(
                f"{model.names[cls]} : {conf:.2f}"
            )

            total += 1

    # Path of image with bounding boxes
    output_image = os.path.join(
        result.save_dir,
        os.path.basename(image)
    )

print("\n--------------------------------")
print(f"Total Objects Detected : {total}")
print(f"Saved Image            : {output_image}")
print("--------------------------------")
print("\nPrediction completed!")