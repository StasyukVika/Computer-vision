import sys
import cv2
import numpy as np

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QSlider,
    QComboBox,
    QSpinBox,
    QGridLayout,
)


# HELPER FUNCTIONS
def cv_to_pixmap(image):
    """Convert OpenCV image to QPixmap"""

    if image is None:
        return QPixmap()

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w

    qimage = QImage(
        rgb_image.data,
        w,
        h,
        bytes_per_line,
        QImage.Format.Format_RGB888
    )

    return QPixmap.fromImage(qimage)


def resize_to_label(image, width=400, height=300):
    """Resize image to fit preview"""

    if image is None:
        return None

    return cv2.resize(image, (width, height))


def show_image(label, image):
    """Display image in QLabel"""

    if image is None:
        return

    image = resize_to_label(image)

    pixmap = cv_to_pixmap(image)

    label.setPixmap(
        pixmap.scaled(
            label.width(),
            label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        )
    )



# BASE WINDOW
class BaseImageWindow(QWidget):

    def __init__(self, title):
        super().__init__()

        self.setWindowTitle(title)
        self.resize(1000, 600)

        self.image = None
        self.result_image = None

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:
            self.image = cv2.imread(path)

            if self.image is None:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to load image"
                )
                return

            self.on_image_loaded()

    def on_image_loaded(self):
        pass



# A) INVERT WINDOW
class InvertWindow(BaseImageWindow):

    def __init__(self):
        super().__init__("A) Image Inversion")

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)

        self.process_btn = QPushButton("Invert")
        self.process_btn.clicked.connect(self.invert_image)

        button_layout.addWidget(self.load_btn)
        button_layout.addWidget(self.process_btn)

        images_layout = QHBoxLayout()

        self.original_label = QLabel("Original Image")
        self.original_label.setFixedSize(450, 400)
        self.original_label.setStyleSheet(
            "border:1px solid black;"
        )
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.result_label = QLabel("Inverted Image")
        self.result_label.setFixedSize(450, 400)
        self.result_label.setStyleSheet(
            "border:1px solid black;"
        )
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        images_layout.addWidget(self.original_label)
        images_layout.addWidget(self.result_label)

        layout.addLayout(button_layout)
        layout.addLayout(images_layout)

        self.setLayout(layout)

    def on_image_loaded(self):
        show_image(
            self.original_label,
            self.image
        )

    def invert_image(self):

        if self.image is None:
            QMessageBox.warning(
                self,
                "Error",
                "Load image first"
            )
            return

        self.result_image = 255 - self.image

        show_image(
            self.result_label,
            self.result_image
        )



# B) RGB MODIFY WINDOW
class RGBModifyWindow(BaseImageWindow):

    def __init__(self):
        super().__init__("B) RGB Component Modification")

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()

        controls = QHBoxLayout()

        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)

        self.channel_combo = QComboBox()
        self.channel_combo.addItems(
            ["Red", "Green", "Blue"]
        )

        self.value_spin = QSpinBox()
        self.value_spin.setRange(-255, 255)
        self.value_spin.setValue(50)

        self.process_btn = QPushButton(
            "Modify Channel"
        )
        self.process_btn.clicked.connect(
            self.modify_channel
        )

        controls.addWidget(self.load_btn)
        controls.addWidget(QLabel("Channel:"))
        controls.addWidget(self.channel_combo)
        controls.addWidget(QLabel("Value:"))
        controls.addWidget(self.value_spin)
        controls.addWidget(self.process_btn)

        images_layout = QHBoxLayout()

        self.original_label = QLabel(
            "Original Image"
        )
        self.original_label.setFixedSize(450, 400)
        self.original_label.setStyleSheet(
            "border:1px solid black;"
        )
        self.original_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.result_label = QLabel(
            "Modified Image"
        )
        self.result_label.setFixedSize(450, 400)
        self.result_label.setStyleSheet(
            "border:1px solid black;"
        )
        self.result_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        images_layout.addWidget(
            self.original_label
        )
        images_layout.addWidget(
            self.result_label
        )

        main_layout.addLayout(controls)
        main_layout.addLayout(images_layout)

        self.setLayout(main_layout)

    def on_image_loaded(self):

        show_image(
            self.original_label,
            self.image
        )

    def modify_channel(self):

        if self.image is None:
            QMessageBox.warning(
                self,
                "Error",
                "Load image first"
            )
            return

        result = self.image.copy()

        value = self.value_spin.value()

        channel = self.channel_combo.currentText()

        if channel == "Blue":
            idx = 0
        elif channel == "Green":
            idx = 1
        else:
            idx = 2

        temp = result[:, :, idx].astype(np.int16)

        temp = np.clip(
            temp + value,
            0,
            255
        )

        result[:, :, idx] = temp.astype(np.uint8)

        self.result_image = result

        show_image(
            self.result_label,
            self.result_image
        )



# C) RGB SPLIT WINDOW
class RGBSplitWindow(BaseImageWindow):

    def __init__(self):
        super().__init__("C) RGB Split")
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        self.load_btn = QPushButton("Load Image")
        self.load_btn.clicked.connect(self.load_image)

        self.split_btn = QPushButton("Split RGB")
        self.split_btn.clicked.connect(self.split_rgb)

        top_layout.addWidget(self.load_btn)
        top_layout.addWidget(self.split_btn)

        grid = QGridLayout()

        self.original_label = QLabel("Original")
        self.original_label.setFixedSize(400, 300)
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setStyleSheet(
            "border:1px solid black;"
        )

        self.red_label = QLabel("Red")
        self.red_label.setFixedSize(400, 300)
        self.red_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.red_label.setStyleSheet(
            "border:1px solid black;"
        )

        self.green_label = QLabel("Green")
        self.green_label.setFixedSize(400, 300)
        self.green_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.green_label.setStyleSheet(
            "border:1px solid black;"
        )

        self.blue_label = QLabel("Blue")
        self.blue_label.setFixedSize(400, 300)
        self.blue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blue_label.setStyleSheet(
            "border:1px solid black;"
        )

        grid.addWidget(self.original_label, 0, 0)
        grid.addWidget(self.red_label, 0, 1)
        grid.addWidget(self.green_label, 1, 0)
        grid.addWidget(self.blue_label, 1, 1)

        layout.addLayout(top_layout)
        layout.addLayout(grid)

        self.setLayout(layout)

    def on_image_loaded(self):

        show_image(
            self.original_label,
            self.image
        )

    def split_rgb(self):

        if self.image is None:
            QMessageBox.warning(
                self,
                "Error",
                "Load image first"
            )
            return

        b, g, r = cv2.split(self.image)

        red_img = np.zeros_like(self.image)
        green_img = np.zeros_like(self.image)
        blue_img = np.zeros_like(self.image)

        red_img[:, :, 2] = r
        green_img[:, :, 1] = g
        blue_img[:, :, 0] = b

        show_image(self.red_label, red_img)
        show_image(self.green_label, green_img)
        show_image(self.blue_label, blue_img)



# D) BLEND WINDOW
class BlendWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("D) Blend Images")
        self.resize(1100, 650)

        self.image1 = None
        self.image2 = None
        self.result_image = None

        self.alpha = 0.5
        self.timer = QTimer()

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        controls = QHBoxLayout()

        self.load1_btn = QPushButton("Load Image 1")
        self.load1_btn.clicked.connect(
            self.load_image1
        )

        self.load2_btn = QPushButton("Load Image 2")
        self.load2_btn.clicked.connect(
            self.load_image2
        )

        self.slider = QSlider(
            Qt.Orientation.Horizontal
        )
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(
            self.update_blend
        )

        self.alpha_label = QLabel(
            "Alpha: 0.50"
        )

        self.animate_btn = QPushButton(
            "Start Animation"
        )
        self.animate_btn.clicked.connect(
            self.start_animation
        )

        controls.addWidget(self.load1_btn)
        controls.addWidget(self.load2_btn)
        controls.addWidget(self.alpha_label)
        controls.addWidget(self.slider)
        controls.addWidget(self.animate_btn)

        images_layout = QHBoxLayout()

        self.label1 = QLabel("Image 1")
        self.label2 = QLabel("Image 2")
        self.result_label = QLabel("Blended")

        for lbl in [
            self.label1,
            self.label2,
            self.result_label
        ]:
            lbl.setFixedSize(320, 400)
            lbl.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            lbl.setStyleSheet(
                "border:1px solid black;"
            )

        images_layout.addWidget(self.label1)
        images_layout.addWidget(self.label2)
        images_layout.addWidget(
            self.result_label
        )

        layout.addLayout(controls)
        layout.addLayout(images_layout)

        self.setLayout(layout)

        self.timer.timeout.connect(
            self.animate_step
        )

    def load_image1(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image 1",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:
            self.image1 = cv2.imread(path)
            show_image(
                self.label1,
                self.image1
            )
            self.update_blend()

    def load_image2(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image 2",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:
            self.image2 = cv2.imread(path)
            show_image(
                self.label2,
                self.image2
            )
            self.update_blend()

    def update_blend(self):

        if self.image1 is None or self.image2 is None:
            return

        self.alpha = (
            self.slider.value() / 100
        )

        self.alpha_label.setText(
            f"Alpha: {self.alpha:.2f}"
        )

        h = min(
            self.image1.shape[0],
            self.image2.shape[0]
        )

        w = min(
            self.image1.shape[1],
            self.image2.shape[1]
        )

        img1 = cv2.resize(
            self.image1,
            (w, h)
        )

        img2 = cv2.resize(
            self.image2,
            (w, h)
        )

        beta = 1 - self.alpha

        self.result_image = cv2.addWeighted(
            img1,
            self.alpha,
            img2,
            beta,
            0
        )

        show_image(
            self.result_label,
            self.result_image
        )

    def start_animation(self):

        self.timer.start(100)

    def animate_step(self):

        value = self.slider.value() + 5

        if value > 100:
            value = 0

        self.slider.setValue(value)



# E) FILTER WINDOW
class FilterWindow(BaseImageWindow):

    def __init__(self):
        super().__init__("E) Filters")
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        top = QHBoxLayout()

        self.load_btn = QPushButton(
            "Load Image"
        )
        self.load_btn.clicked.connect(
            self.load_image
        )

        self.combo = QComboBox()
        self.combo.addItems([
            "Blur",
            "Sharpen",
            "Median",
            "Erosion",
            "Dilation",
            "Sobel"
        ])

        self.apply_btn = QPushButton(
            "Apply Filter"
        )
        self.apply_btn.clicked.connect(
            self.apply_filter
        )

        top.addWidget(self.load_btn)
        top.addWidget(self.combo)
        top.addWidget(self.apply_btn)

        images = QHBoxLayout()

        self.original_label = QLabel(
            "Original"
        )
        self.result_label = QLabel(
            "Result"
        )

        for lbl in [
            self.original_label,
            self.result_label
        ]:
            lbl.setFixedSize(450, 400)
            lbl.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )
            lbl.setStyleSheet(
                "border:1px solid black;"
            )

        images.addWidget(
            self.original_label
        )
        images.addWidget(
            self.result_label
        )

        layout.addLayout(top)
        layout.addLayout(images)

        self.setLayout(layout)

    def on_image_loaded(self):

        show_image(
            self.original_label,
            self.image
        )

    def apply_filter(self):

        if self.image is None:
            QMessageBox.warning(
                self,
                "Error",
                "Load image first"
            )
            return

        filter_name = (
            self.combo.currentText()
        )

        img = self.image.copy()

        if filter_name == "Blur":

            result = cv2.blur(img, (5, 5))

        elif filter_name == "Sharpen":

            kernel = np.array([
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ])

            result = cv2.filter2D(
                img,
                -1,
                kernel
            )

        elif filter_name == "Median":

            result = cv2.medianBlur(
                img,
                5
            )

        elif filter_name == "Erosion":

            kernel = np.ones(
                (5, 5),
                np.uint8
            )

            result = cv2.erode(
                img,
                kernel,
                iterations=1
            )

        elif filter_name == "Dilation":

            kernel = np.ones(
                (5, 5),
                np.uint8
            )

            result = cv2.dilate(
                img,
                kernel,
                iterations=1
            )

        elif filter_name == "Sobel":

            gray = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

            sobel_x = cv2.Sobel(
                gray,
                cv2.CV_64F,
                1,
                0,
                ksize=3
            )

            sobel_y = cv2.Sobel(
                gray,
                cv2.CV_64F,
                0,
                1,
                ksize=3
            )

            sobel = cv2.magnitude(
                sobel_x,
                sobel_y
            )

            result = np.uint8(
                np.clip(
                    sobel,
                    0,
                    255
                )
            )

            result = cv2.cvtColor(
                result,
                cv2.COLOR_GRAY2BGR
            )

        self.result_image = result

        show_image(
            self.result_label,
            self.result_image
        )


# F) WATERMARK EMBED WINDOW
class WatermarkEmbedWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "F) Watermark Embed (LSB)"
        )

        self.resize(1200, 700)

        self.container_image = None
        self.watermark_image = None
        self.result_image = None

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()

        controls = QHBoxLayout()

        self.load_container_btn = QPushButton(
            "Load Container"
        )
        self.load_container_btn.clicked.connect(
            self.load_container
        )

        self.load_watermark_btn = QPushButton(
            "Load Watermark"
        )
        self.load_watermark_btn.clicked.connect(
            self.load_watermark
        )

        self.bit_spin = QSpinBox()
        self.bit_spin.setRange(1, 8)
        self.bit_spin.setValue(1)

        self.embed_btn = QPushButton(
            "Embed Watermark"
        )
        self.embed_btn.clicked.connect(
            self.embed_watermark
        )

        self.save_btn = QPushButton(
            "Save Result"
        )
        self.save_btn.clicked.connect(
            self.save_result
        )

        controls.addWidget(
            self.load_container_btn
        )

        controls.addWidget(
            self.load_watermark_btn
        )

        controls.addWidget(
            QLabel("Bit Plane:")
        )

        controls.addWidget(self.bit_spin)

        controls.addWidget(self.embed_btn)

        controls.addWidget(self.save_btn)

        images_layout = QHBoxLayout()

        self.container_label = QLabel(
            "Container"
        )

        self.watermark_label = QLabel(
            "Watermark"
        )

        self.result_label = QLabel(
            "Embedded Result"
        )

        for lbl in [
            self.container_label,
            self.watermark_label,
            self.result_label
        ]:

            lbl.setFixedSize(350, 500)

            lbl.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            lbl.setStyleSheet(
                "border:1px solid black;"
            )

        images_layout.addWidget(
            self.container_label
        )

        images_layout.addWidget(
            self.watermark_label
        )

        images_layout.addWidget(
            self.result_label
        )

        main_layout.addLayout(controls)
        main_layout.addLayout(images_layout)

        self.setLayout(main_layout)

    def load_container(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Container Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:

            self.container_image = cv2.imread(path)

            show_image(
                self.container_label,
                self.container_image
            )

    def load_watermark(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Watermark",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:

            self.watermark_image = cv2.imread(path)

            show_image(
                self.watermark_label,
                self.watermark_image
            )

    def embed_watermark(self):

        if self.container_image is None:

            QMessageBox.warning(
                self,
                "Error",
                "Load container image"
            )

            return

        if self.watermark_image is None:

            QMessageBox.warning(
                self,
                "Error",
                "Load watermark image"
            )

            return

        result = self.container_image.copy()

        gray = cv2.cvtColor(
            self.watermark_image,
            cv2.COLOR_BGR2GRAY
        )

        
        _, binary = cv2.threshold(
            gray,
            127,
            1,
            cv2.THRESH_BINARY
        )

        h, w = result.shape[:2]

        wh, ww = binary.shape

        
        bit_plane = self.bit_spin.value() - 1

        for y in range(h):

            for x in range(w):

                wm_pixel = binary[
                    y % wh,
                    x % ww
                ]

                blue = int(result[y, x, 0])


                mask = 255 ^ (1 << bit_plane)

                # очищення потрібного біта
                blue = blue & mask

                # запис watermark біта
                blue = blue | (
                    int(wm_pixel) << bit_plane
                )

                result[y, x, 0] = np.uint8(blue)

        self.result_image = result

        show_image(
            self.result_label,
            self.result_image
        )

    def save_result(self):

        if self.result_image is None:

            QMessageBox.warning(
                self,
                "Error",
                "No result image"
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Result",
            "",
            "PNG (*.png)"
        )

        if path:

            cv2.imwrite(
                path,
                self.result_image
            )

            QMessageBox.information(
                self,
                "Saved",
                "Image saved successfully"
            )



# G) WATERMARK EXTRACT WINDOW
class WatermarkExtractWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "G) Watermark Extract"
        )

        self.resize(1000, 650)

        self.image = None
        self.extracted = None

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()

        controls = QHBoxLayout()

        self.load_btn = QPushButton(
            "Load Watermarked Image"
        )

        self.load_btn.clicked.connect(
            self.load_image
        )

        self.bit_spin = QSpinBox()

        self.bit_spin.setRange(1, 8)

        self.bit_spin.setValue(1)

        self.extract_btn = QPushButton(
            "Extract Watermark"
        )

        self.extract_btn.clicked.connect(
            self.extract_watermark
        )

        self.save_btn = QPushButton(
            "Save Watermark"
        )

        self.save_btn.clicked.connect(
            self.save_watermark
        )

        controls.addWidget(self.load_btn)

        controls.addWidget(
            QLabel("Bit Plane:")
        )

        controls.addWidget(self.bit_spin)

        controls.addWidget(self.extract_btn)

        controls.addWidget(self.save_btn)

        images_layout = QHBoxLayout()

        self.original_label = QLabel(
            "Watermarked Image"
        )

        self.result_label = QLabel(
            "Extracted Watermark"
        )

        for lbl in [
            self.original_label,
            self.result_label
        ]:

            lbl.setFixedSize(450, 500)

            lbl.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            lbl.setStyleSheet(
                "border:1px solid black;"
            )

        images_layout.addWidget(
            self.original_label
        )

        images_layout.addWidget(
            self.result_label
        )

        main_layout.addLayout(controls)
        main_layout.addLayout(images_layout)

        self.setLayout(main_layout)

    def load_image(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Watermarked Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:

            self.image = cv2.imread(path)

            show_image(
                self.original_label,
                self.image
            )

    def extract_watermark(self):

        if self.image is None:

            QMessageBox.warning(
                self,
                "Error",
                "Load image first"
            )

            return

        bit_plane = self.bit_spin.value() - 1

        blue = self.image[:, :, 0]

        extracted = (
            (
                blue >> bit_plane
            ) & 1
        ) * 255

        extracted = extracted.astype(
            np.uint8
        )

        self.extracted = extracted

        extracted_bgr = cv2.cvtColor(
            extracted,
            cv2.COLOR_GRAY2BGR
        )

        show_image(
            self.result_label,
            extracted_bgr
        )

    def save_watermark(self):

        if self.extracted is None:

            QMessageBox.warning(
                self,
                "Error",
                "No extracted watermark"
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Watermark",
            "",
            "PNG (*.png)"
        )

        if path:

            cv2.imwrite(
                path,
                self.extracted
            )

            QMessageBox.information(
                self,
                "Saved",
                "Watermark saved"
            )



# MAIN WINDOW
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Computer Practicum - Image Processing"
        )

        self.resize(450, 500)

        self.windows = []

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel(
            "Image Processing Application"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )

        layout.addWidget(title)

        btn_a = QPushButton(
            "A) Invert Image"
        )
        btn_a.clicked.connect(
            self.open_invert
        )

        btn_b = QPushButton(
            "B) Modify RGB Component"
        )
        btn_b.clicked.connect(
            self.open_rgb_modify
        )

        btn_c = QPushButton(
            "C) Split RGB"
        )
        btn_c.clicked.connect(
            self.open_rgb_split
        )

        btn_d = QPushButton(
            "D) Blend Images"
        )
        btn_d.clicked.connect(
            self.open_blend
        )

        btn_e = QPushButton(
            "E) Filters"
        )
        btn_e.clicked.connect(
           self.open_filters
        )

        btn_f = QPushButton(
           "F) Watermark Embed"
        )
        btn_f.clicked.connect(
           self.open_embed
        )

        btn_g = QPushButton(
           "G) Watermark Extract"
        )
        btn_g.clicked.connect(
           self.open_extract
        )

        layout.addWidget(btn_a)
        layout.addWidget(btn_b)
        layout.addWidget(btn_c)
        layout.addWidget(btn_d)
        layout.addWidget(btn_e)
        layout.addWidget(btn_f)
        layout.addWidget(btn_g)

        self.setLayout(layout)

    def open_invert(self):

        window = InvertWindow()

        self.windows.append(window)

        window.show()

    def open_rgb_modify(self):

        window = RGBModifyWindow()

        self.windows.append(window)

        window.show()
        
    def open_rgb_split(self):

        window = RGBSplitWindow()

        self.windows.append(window)

        window.show()


    def open_blend(self):

        window = BlendWindow()

        self.windows.append(window)

        window.show()


    def open_filters(self):

        window = FilterWindow()

        self.windows.append(window)

        window.show()
        
    def open_embed(self):

        window = WatermarkEmbedWindow()

        self.windows.append(window)

        window.show()


    def open_extract(self):

        window = WatermarkExtractWindow()

        self.windows.append(window)

        window.show()



# RUN APP
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

