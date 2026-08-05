import os
import random
import shutil
from pathlib import Path

random.seed(42)

base = Path("dataset/data")
images = base / "images"
labels = base / "labels"

train_img = Path("dataset/train/images")
train_lbl = Path("dataset/train/labels")
valid_img = Path("dataset/valid/images")
valid_lbl = Path("dataset/valid/labels")

for folder in [train_img, train_lbl, valid_img, valid_lbl]:
    folder.mkdir(parents=True, exist_ok=True)

image_files = list(images.glob("*.jpg"))
random.shuffle(image_files)

split = int(len(image_files) * 0.8)

train = image_files[:split]
valid = image_files[split:]

def copy_files(files, img_dest, lbl_dest):
    for img in files:
        shutil.copy(img, img_dest / img.name)
        label = labels / (img.stem + ".txt")
        if label.exists():
            shutil.copy(label, lbl_dest / label.name)

copy_files(train, train_img, train_lbl)
copy_files(valid, valid_img, valid_lbl)

yaml = """path: dataset

train: train/images
val: valid/images

names:
  0: pothole
  1: crack
  2: manhole
"""

with open("dataset/data.yaml", "w") as f:
    f.write(yaml)

print("Dataset prepared successfully!")