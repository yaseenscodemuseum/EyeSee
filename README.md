  # 👁️‍🗨️ Eye See — Real-Time Face Detection App

> A desktop application for face detection using OpenCV's DNN (deep neural network) module and a sleek PyQt5 user interface.  
> Works offline, supports multiple lighting conditions, and highlights detected faces using a fast SSD + ResNet model.

---

## 🚀 Features

- ⚡ Modern face detection using OpenCV's **DNN module** (ResNet-SSD)
- 🎮 Pixel-style **PyQt5 UI** with glowing labels and snapshot buttons
- 📸 Saves both **raw and processed** snapshots
- 🌑 Dark mode with optional pixel-art background
- 🧠 Smarter than Haar — works with side faces, low light, and phones

---

##App GUI

![](Images/Screenshot.png)

## 🖼️ Detection Examples

### 1. Low light detection comparison
| Original | Processed |
|----------|-----------|
| ![](Images/snap1.png) | ![](Images/snap1_imagedetect.png) |
> Low light face detection comparison showing original and processed output

---

### 2. Side profile detection
| Original | Processed |
|----------|-----------|
| ![](Images/snap3.png) | ![](Images/snap3_imagedetect.png) |

---

### 3. Detection with various poses
| Original | Processed |
|----------|-----------|
| ![](Images/snap6.png) | ![](Images/snap6_imagedetect.png) |

---

### 4. Resistant to false positives
| Original | Processed |
|----------|-----------|
| ![](Images/snap7.png) | ![](Images/snap7_imagedetect.png) |
> Doesn't detect random masks or objects with eyes

---

### 5. Phone face detection via webcam
| Original | Processed |
|----------|-----------|
| ![](Images/snap12.png) | ![](Images/snap12_imagedetect.png) |

---

### 6. Multi-face detection on phone screens
| Original | Processed |
|----------|-----------|
| ![](Images/snap16.png) | ![](Images/snap16_imagedetect.png) |

---

## 📦 Setup & Usage

1. 📁 **Clone or download** the repository
2. 🧠 Make sure you have **Python 3.13** (or compatible)
3. ✅ Run the app using the "Autorun.bat" file
