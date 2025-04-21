import sys
import cv2
import glob
import re
import os
import numpy as np
from PIL import Image, ImageOps
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QImage, QPixmap, QFontDatabase, QFont, QPalette, QBrush, QColor, QDesktopServices
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QPushButton,
    QVBoxLayout, QWidget, QHBoxLayout, QGraphicsDropShadowEffect
)

class FaceDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎮 Eye See - Face Detection App")
        self.setGeometry(100, 100, 900, 700)

        # ================= LOAD CUSTOM PIXELIFY FONT =================
        font_id = QFontDatabase.addApplicationFont("PixelifySans-VariableFont_wght.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)

        # Use the pixel font if loaded; else fallback to Arial
        if families:
            pixel_font = QFont(families[0], 12)
        else:
            print("⚠️ Failed to load PixelifySans font, using default.")
            pixel_font = QFont("Arial", 12)
            
        # Add title "Eye See"
        title_label = QLabel("Eye See")
        title_label.setFont(QFont(families[0] if families else "Arial", 36))
        title_label.setStyleSheet("""
            color: white;
            padding: 10px 20px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Enhanced glow effect for title
        title_glow = QGraphicsDropShadowEffect()
        title_glow.setBlurRadius(25)
        title_glow.setColor(QColor(0, 157, 255))
        title_glow.setOffset(0)
        title_glow.setXOffset(0)
        title_glow.setYOffset(0)
        title_label.setGraphicsEffect(title_glow)

        # Add clickable logo with inverted colors and larger size
        logo_label = QLabel()
        try:
            # Load the PNG with transparency
            original_logo = Image.open("logo.png").convert('RGBA')
            
            # Split the image into bands (R,G,B,A)
            r, g, b, a = original_logo.split()
            
            # Invert only the RGB bands
            r_inv = ImageOps.invert(r)
            g_inv = ImageOps.invert(g)
            b_inv = ImageOps.invert(b)
            
            # Merge back with original alpha channel
            inverted_logo = Image.merge('RGBA', (r_inv, g_inv, b_inv, a))
            
            # Convert PIL image back to QPixmap
            logo_path = "inverted_logo_temp.png"
            inverted_logo.save(logo_path)
            logo_pixmap = QPixmap(logo_path)
            os.remove(logo_path)  # Clean up temporary file
            
            if logo_pixmap.isNull():
                print("⚠️ Failed to load logo.png")
                logo_pixmap = QPixmap(70, 70)
                logo_pixmap.fill(Qt.transparent)
            else:
                print("✅ Logo loaded successfully, dimensions:", logo_pixmap.width(), "x", logo_pixmap.height())
                scaled_logo = logo_pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled_logo)
                logo_label.setMinimumSize(70, 70)
                logo_label.setStyleSheet("""
                    QLabel {
                        padding: 5px;
                        margin-right: 10px;
                    }
                """)
        except Exception as e:
            print(f"⚠️ Error loading logo: {str(e)}")
            empty_pixmap = QPixmap(50, 50)
            empty_pixmap.fill(Qt.transparent)
            logo_label.setPixmap(empty_pixmap)
        
        logo_label.setCursor(Qt.PointingHandCursor)
        # Update mousePressEvent to open link without closing app
        def open_portfolio(event):
            QDesktopServices.openUrl(QUrl("https://yaseensportfolio.vercel.app/"))
            event.accept()  # Accept the event but keep app running
            
        logo_label.mousePressEvent = open_portfolio

        # Create container for logo and title with shared background
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.addWidget(logo_label)
        title_layout.addWidget(title_label)
        title_layout.setContentsMargins(10, 5, 10, 5)
        title_container.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.6);
                border-radius: 15px;
            }
        """)

        # Create top bar layout
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(title_container)
        top_bar.addStretch()

        # ================= DARK MODE + BACKGROUND ===================
        self.setAutoFillBackground(True)
        palette = self.palette()

        # Set dark background color
        palette.setColor(QPalette.Window, QColor(30, 30, 30))

        # Load and scale background image with error handling
        try:
            bg_pixmap = QPixmap("background.png")
            if bg_pixmap.isNull():
                print("⚠️ Failed to load background.png")
                palette.setColor(QPalette.Window, QColor(30, 30, 30))
            else:
                scaled_bg = bg_pixmap.scaled(
                    self.size(), 
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
                palette.setBrush(QPalette.Window, QBrush(scaled_bg))
        except Exception as e:
            print(f"⚠️ Error loading background: {str(e)}")
            palette.setColor(QPalette.Window, QColor(30, 30, 30))

        self.setPalette(palette)
        # ============================================================

        # ================= UI LAYOUT SETUP ==========================
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Add top bar to main layout
        main_layout.addLayout(top_bar)

        # Webcam feed display
        self.image_label = QLabel()
        self.image_label.setFixedSize(640, 480)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 3px solid #fff; border-radius: 10px;")

        # Face count label
        self.face_count_label = QLabel("Faces Detected: 0")
        self.face_count_label.setFont(pixel_font)
        self.face_count_label.setAlignment(Qt.AlignCenter)
        self.face_count_label.setStyleSheet("""
            color: #ffffff;
            background: transparent;
            font-size: 24px;
            padding: 15px;
            font-weight: bold;
        """)
        
        # Create and configure face count glow effect
        face_count_glow = QGraphicsDropShadowEffect()
        face_count_glow.setBlurRadius(10)
        face_count_glow.setColor(QColor(255, 255, 255))
        face_count_glow.setOffset(0)
        self.face_count_label.setGraphicsEffect(face_count_glow)

        # Toggle detection button
        self.toggle_button = QPushButton("🎯 Toggle Detection")
        self.toggle_button.setFont(pixel_font)
        self.toggle_button.setStyleSheet("""
            padding: 10px;
            background-color: #44475a;
            color: white;
            border-radius: 6px;
        """)
        toggle_text_glow = QGraphicsDropShadowEffect()
        toggle_text_glow.setBlurRadius(15)
        toggle_text_glow.setColor(QColor(255, 255, 255))
        toggle_text_glow.setOffset(0)
        self.toggle_button.setGraphicsEffect(toggle_text_glow)

        # Save snapshot button
        self.snapshot_button = QPushButton("📸 Save Snapshot")
        self.snapshot_button.setFont(pixel_font)
        self.snapshot_button.setStyleSheet("""
            padding: 10px;
            background-color: #6272a4;
            color: white;
            border-radius: 6px;
        """)
        snapshot_text_glow = QGraphicsDropShadowEffect()
        snapshot_text_glow.setBlurRadius(15)
        snapshot_text_glow.setColor(QColor(255, 255, 255))
        snapshot_text_glow.setOffset(0)
        self.snapshot_button.setGraphicsEffect(snapshot_text_glow)

        # Connect buttons to functions
        self.toggle_button.clicked.connect(self.toggle_detection)
        self.snapshot_button.clicked.connect(self.save_snapshot)

        # Layout for video display
        video_layout = QHBoxLayout()
        video_layout.addStretch()
        video_layout.addWidget(self.image_label)
        video_layout.addStretch()

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.toggle_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(self.snapshot_button)
        button_layout.addStretch()

        # Combine all layouts into main layout
        main_layout.addLayout(video_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.face_count_label)
        main_layout.addSpacing(10)
        main_layout.addLayout(button_layout)

        # Set layout to window
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        # ============================================================

        # =================== FACE DETECTION SETUP ===================
        # Load DNN face detector
        self.dnn_net = cv2.dnn.readNet(
            "deploy.prototxt",
            "res10_300x300_ssd_iter_140000.caffemodel"
        )
        self.cap = cv2.VideoCapture(0)  # Start webcam capture
        self.face_detection_enabled = True  # Toggle for face detection

        # Find the highest snapshot number from existing files
        existing_snapshots = glob.glob("snap*.png")
        highest_num = 0
        for snap in existing_snapshots:
            match = re.search(r'snap(\d+)', snap)
            if match:
                num = int(match.group(1))
                highest_num = max(highest_num, num)
        self.snapshot_counter = highest_num + 1

        # Timer to repeatedly grab frames from webcam
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Run every 30ms (~30 FPS)
        # ============================================================

    def update_frame(self):
        # Grab a frame from the webcam
        ret, frame = self.cap.read()
        if not ret:
            return

        # If detection is enabled, detect faces using DNN
        if self.face_detection_enabled:
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))

            self.dnn_net.setInput(blob)
            detections = self.dnn_net.forward()

            face_count = 0

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    face_count += 1

            self.face_count_label.setText(f"Faces Detected: {face_count}")
        else:
            self.face_count_label.setText("Faces Detected: 0")

        # Convert OpenCV BGR to RGB for Qt display
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Show the frame in the QLabel
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def toggle_detection(self):
        # Toggle on/off face detection
        self.face_detection_enabled = not self.face_detection_enabled

    def save_snapshot(self):
        # Read current frame
        ret, frame = self.cap.read()
        if ret:
            frame_no_rect = frame.copy()  # Copy of frame without rectangles
            
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))
            self.dnn_net.setInput(blob)
            detections = self.dnn_net.forward()

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            # Generate filenames using counter
            snap_plain_name = f"snap{self.snapshot_counter}.png"
            snap_detect_name = f"snap{self.snapshot_counter}_imagedetect.png"

            # Save both images
            cv2.imwrite(snap_plain_name, frame_no_rect)
            cv2.imwrite(snap_detect_name, frame)

            print(f"✅ Snapshots saved as: {snap_plain_name} and {snap_detect_name}")

            # Increment counter for next snapshot
            self.snapshot_counter += 1

    def closeEvent(self, event):
        # When window closes, release the camera
        self.cap.release()
        event.accept()

# ======================== APP ENTRY POINT ===========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceDetectionApp()
    window.show()
    sys.exit(app.exec_())
