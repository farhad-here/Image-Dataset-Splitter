import os
import streamlit as st
import shutil
import random
import zipfile
from pathlib import Path
from io import BytesIO

# Configuration
SPLIT_RATIO = (0.7, 0.15, 0.15)  # train, val, test
TEMP_EXTRACT_DIR = "temp_extracted"
TARGET_DIR = "final_dataset"

st.title("📁 Dataset Splitter")

# File uploader
uploaded_zip = st.file_uploader("Upload a ZIP file containing folders of images (each folder = 1 class)", type=["zip"])

if uploaded_zip:
    # Cleanup previous runs
    if os.path.exists(TEMP_EXTRACT_DIR):
        shutil.rmtree(TEMP_EXTRACT_DIR)
    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)

    #Extract uploaded zip file
    with zipfile.ZipFile(uploaded_zip, "r") as zip_ref:
        zip_ref.extractall(TEMP_EXTRACT_DIR)
    st.success("ZIP file extracted successfully.")

    # Create output folders
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(TARGET_DIR, split), exist_ok=True)

    # Process each class folder
    for class_name in os.listdir(TEMP_EXTRACT_DIR):
        class_path = os.path.join(TEMP_EXTRACT_DIR, class_name)
        if not os.path.isdir(class_path):
            continue

        images = list(Path(class_path).glob("*.*"))
        random.shuffle(images)

        train_end = int(len(images) * SPLIT_RATIO[0])
        val_end = train_end + int(len(images) * SPLIT_RATIO[1])

        splits = {
            "train": images[:train_end],
            "val": images[train_end:val_end],
            "test": images[val_end:]
        }

        # Copy images to corresponding folders
        for split_name, split_images in splits.items():
            split_class_dir = os.path.join(TARGET_DIR, split_name, class_name)
            os.makedirs(split_class_dir, exist_ok=True)
            for img_path in split_images:
                dest_path = os.path.join(split_class_dir, img_path.name)
                shutil.copy(img_path, dest_path)

    st.success("Images successfully split into train/val/test folders.")

    # Create downloadable ZIP file of the final dataset
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(TARGET_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, TARGET_DIR)
                zipf.write(file_path, arcname)
    zip_buffer.seek(0)

    st.download_button(
        label="📥 Download Final Dataset (train/val/test)",
        data=zip_buffer,
        file_name="dataset_split.zip",
        mime="application/zip"
    )
