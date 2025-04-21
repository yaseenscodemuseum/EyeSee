# 👁️‍🗨️ Eye_See — Real-Time Face Detection App

> **AI-powered desktop app** that captures and detects faces using OpenCV DNN and a clean custom UI built with PyQt5.  
> Works offline, supports multiple lighting conditions, and highlights detected faces using a fast SSD + ResNet model.

---

## 🚀 Features

- ⚡ Modern face detection using OpenCV's **DNN module** (ResNet-SSD)
- 🎮 Pixel-style **PyQt5 UI** with glowing labels and snapshot buttons
- 📸 Saves both **raw and detected** snapshots
- 🌑 Dark mode with optional pixel-art background
- 🧠 Smarter than Haar — works with side faces, low light, and phones

---

## 🖼️ Detection Examples

### 1. Low light detection comparison
| Original | Processed |
|----------|-----------|
| ![](images/snap1.png) | ![](images/snap1_imagedetect.png) |
> Low light face detection comparison showing original and processed output

---

### 2. Side profile detection
| Original | Processed |
|----------|-----------|
| ![](images/snap3.png) | ![](images/snap3_imagedetect.png) |

---

### 3. Detection with various poses
| Original | Processed |
|----------|-----------|
| ![](images/snap6.png) | ![](images/snap6_imagedetect.png) |

---

### 4. Resistant to false positives
| Original | Processed |
|----------|-----------|
| ![](images/snap7.png) | ![](images/snap7_imagedetect.png) |
> Doesn't detect random masks or objects with eyes

---

### 5. Phone face detection via webcam
| Original | Processed |
|----------|-----------|
| ![](images/snap12.png) | ![](images/snap12_imagedetect.png) |

---

### 6. Multi-face detection on phone screens
| Original | Processed |
|----------|-----------|
| ![](images/snap16.png) | ![](images/snap16_imagedetect.png) |

---

## 📦 Setup & Usage

1. 📁 **Clone or download** the repository
2. 🧠 Make sure you have **Python 3.13** (or compatible)
3. ✅ Run the app using:
   ```bash
   Autorun.bat
