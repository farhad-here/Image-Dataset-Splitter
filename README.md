# 📁 Image Dataset Splitter

This Streamlit app allows you to split any labeled image dataset into `train`, `validation`, and `test` sets — all with a single click. Simply upload a `.zip` file where each folder represents a class, and the app will generate a downloadable zip with the organized dataset structure.

---

## 🚀 Features

✅ Upload a `.zip` file with folders of images (each folder is treated as a class)  
✅ Automatically split into `train`, `val`, and `test` folders  
✅ Random shuffling of images for fair distribution  
✅ Download the final dataset as a ready-to-use `.zip`  
✅ Clean UI with Streamlit  

---

## 📂 Expected Input Format

Your input `.zip` file should be structured like this:


Each folder is interpreted as a separate class label.

---

## 🧾 Output Format

After splitting, the app generates a `.zip` file like this:


---

## ⚙️ Configuration

You can modify the train/val/test split ratios by editing this line in `app.py`:

```python
SPLIT_RATIO = (0.7, 0.15, 0.15)

git clone https://github.com/your-username/image-dataset-splitter.git
cd image-dataset-splitter
```

```python
pip install streamlit
streamlit run app.py
```
---

📌 Use Cases
- Preparing image datasets for machine learning / deep learning

- Organizing animal or object classification datasets

- Creating train/val/test splits without writing custom scripts

