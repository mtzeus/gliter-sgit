
#
#
#
# WELCOME TO GLITER 1.0 - GLITCH IMAGE TOOL #
# THIS PROGRAM WAS MADE WITH CHATGPT TO HELP PEOPLE CREATE WITHOUT LIMITS #
# MAY THE ART CREATED WITH THIS PROGRAM BRING PEACE TO THIS DOOMED WORLD #
# MADE IN BRASIL :D
#
#
#




import sys
import random
import io
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QComboBox, QProgressBar, QHBoxLayout, QSlider, QScrollArea
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image

class GlitchArtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = True
        self.initUI()   
        
    def initUI(self):
        self.setWindowTitle('GLITER 1.0 - GLITCH IMAGE TOOL.')
        self.setGeometry(100, 100, 570, 640)
        self.setStyleSheet("background-color: #ffffff;")  # Dark mode default
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Image display area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #1e1e1e;")
        
        self.image_widget = QLabel('Load an image to begin!', self)
        self.image_widget.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.image_widget)
        
        main_layout.addWidget(self.scroll_area, 1)  # Make the scroll area take up the space
        
        # Effect selector
        effect_layout = QHBoxLayout()
        self.effect_selector = QComboBox(self)
        self.effect_selector.addItems([
            "Simple Glitch", "Data Corruption", "Color Shift", "Pixel Shuffle", "Line Glitch",
            "Vertical Glitch", "Horizontal Glitch", "Static Noise", "Color Inversion",
            "Mirror Glitch", "Data Fragmentation", "Image Distortion", "Vertical Bars Glitch",
            "Horizontal Bars Glitch", "Random Pixelation"
        ])
        effect_layout.addWidget(self.effect_selector)
        
        # Intensity slider
        self.intensity_slider = QSlider(Qt.Horizontal, self)
        self.intensity_slider.setMinimum(1)
        self.intensity_slider.setMaximum(100)
        self.intensity_slider.setValue(50)
        self.intensity_slider.setTickPosition(QSlider.TicksBelow)
        self.intensity_slider.setTickInterval(5)
        effect_layout.addWidget(self.intensity_slider)
        
        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        effect_layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)
        button_layout.addWidget(self.load_button)
        
        self.glitch_button = QPushButton('Apply Glitch Effect', self)
        self.glitch_button.clicked.connect(self.apply_glitch)
        self.glitch_button.setEnabled(False)  # Disable until an image is loaded
        button_layout.addWidget(self.glitch_button)
        
        self.save_button = QPushButton('Save Glitched Image', self)
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)  # Disable until an image is glitched
        button_layout.addWidget(self.save_button)
        
        # Theme toggle button
        self.theme_toggle_button = QPushButton('Change Theme', self)
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        button_layout.addWidget(self.theme_toggle_button)
        
        # Add effects and buttons to layout
        main_layout.addLayout(effect_layout)
        main_layout.addLayout(button_layout)
        
        # Set main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    def load_image(self):
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
            if file_name:
                self.original_image = Image.open(file_name)
                self.display_image(self.original_image)
                self.glitch_button.setEnabled(True)  # Enable the glitch button
        except Exception as e:
            self.image_widget.setText(f"Failed to load image: {str(e)}")
    
    def apply_glitch(self):
        try:
            if hasattr(self, 'original_image'):
                selected_effect = self.effect_selector.currentText()
                intensity = self.intensity_slider.value()
                
                # Apply the selected glitch effect
                if selected_effect == "Simple Glitch":
                    glitched_image = self.simple_glitch(self.original_image.copy(), intensity)
                elif selected_effect == "Data Corruption":
                    glitched_image = self.data_corruption(self.original_image.copy(), intensity)
                elif selected_effect == "Color Shift":
                    glitched_image = self.color_shift(self.original_image.copy())
                elif selected_effect == "Pixel Shuffle":
                    glitched_image = self.pixel_shuffle(self.original_image.copy())
                elif selected_effect == "Line Glitch":
                    glitched_image = self.line_glitch(self.original_image.copy(), intensity)
                elif selected_effect == "Vertical Glitch":
                    glitched_image = self.vertical_glitch(self.original_image.copy(), intensity)
                elif selected_effect == "Horizontal Glitch":
                    glitched_image = self.horizontal_glitch(self.original_image.copy(), intensity)
                elif selected_effect == "Static Noise":
                    glitched_image = self.static_noise(self.original_image.copy(), intensity)
                elif selected_effect == "Color Inversion":
                    glitched_image = self.color_inversion(self.original_image.copy())
                elif selected_effect == "Mirror Glitch":
                    glitched_image = self.mirror_glitch(self.original_image.copy(), intensity)
                elif selected_effect == "Data Fragmentation":
                    glitched_image = self.data_fragmentation(self.original_image.copy(), intensity)
                elif selected_effect == "Image Distortion":
                    glitched_image = self.image_distortion(self.original_image.copy(), intensity)
                elif selected_effect == "Vertical Bars Glitch":
                    glitched_image = self.glitch_vertical_bars(self.original_image.copy(), intensity)
                elif selected_effect == "Horizontal Bars Glitch":
                    glitched_image = self.glitch_horizontal_bars(self.original_image.copy(), intensity)
                elif selected_effect == "Random Pixelation":
                    glitched_image = self.random_pixelation(self.original_image.copy(), intensity)
                
                self.display_image(glitched_image)
                self.save_button.setEnabled(True)  # Enable the save button
                self.glitched_image = glitched_image  # Store the glitched image
        except Exception as e:
            self.image_widget.setText(f"Failed to apply glitch: {str(e)}")
    
    def save_image(self):
        try:
            if hasattr(self, 'glitched_image'):
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;All Files (*)", options=options)
                if file_name:
                    self.glitched_image.save(file_name)
            else:
                self.image_widget.setText("No image to save.")
        except Exception as e:
            self.image_widget.setText(f"Failed to save image: {str(e)}")
    
    def display_image(self, image):
        try:
            # Convert PIL Image to QImage
            bytes_io = io.BytesIO()
            image.save(bytes_io, format='PNG')
            qimage = QImage.fromData(bytes_io.getvalue())
            pixmap = QPixmap.fromImage(qimage)
            
            # Scale pixmap while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(self.scroll_area.viewport().size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_widget.setPixmap(scaled_pixmap)
        except Exception as e:
            self.image_widget.setText(f"Failed to display image: {str(e)}")
    
    # Effect implementations here...
    
    def simple_glitch(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        for i in range(width):
            if random.random() > (1 - intensity / 100.0):
                offset = random.randint(0, height // 10)
                np_image[:, i] = np.roll(np_image[:, i], offset, axis=0)
        return Image.fromarray(np_image)
    
    def data_corruption(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        for i in range(width):
            for j in range(height):
                if random.random() > (1 - intensity / 100.0):
                    np_image[j, i] = [random.randint(0, 255) for _ in range(3)]
        return Image.fromarray(np_image)
    
    def color_shift(self, image):
        np_image = np.array(image)
        np_image = np_image[..., [2, 0, 1]]  # Shift colors from RGB to BGR
        return Image.fromarray(np_image)
    
    def pixel_shuffle(self, image):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        indices = [(x, y) for x in range(width) for y in range(height)]
        random.shuffle(indices)
        for (x1, y1), (x2, y2) in zip(indices[::2], indices[1::2]):
            np_image[y1, x1], np_image[y2, x2] = np_image[y2, x2], np_image[y1, x1]
        return Image.fromarray(np_image)
    
    def line_glitch(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        for i in range(height):
            if random.random() > (1 - intensity / 100.0):
                offset = random.randint(-width // 10, width // 10)
                np_image[i] = np.roll(np_image[i], offset, axis=0)
        return Image.fromarray(np_image)
    
    def vertical_glitch(self, image, intensity):
        np_image = np.array(image)
        width = np_image.shape[1]
        for i in range(width):
            if random.random() > (1 - intensity / 100.0):
                offset = random.randint(-width // 10, width // 10)
                np_image[:, i] = np.roll(np_image[:, i], offset, axis=0)
        return Image.fromarray(np_image)
    
    def horizontal_glitch(self, image, intensity):
        np_image = np.array(image)
        height = np_image.shape[0]
        for i in range(height):
            if random.random() > (1 - intensity / 100.0):
                offset = random.randint(-height // 10, height // 10)
                np_image[i] = np.roll(np_image[i], offset, axis=0)
        return Image.fromarray(np_image)
    
    def static_noise(self, image, intensity):
        np_image = np.array(image)
        noise = np.random.normal(0, intensity, np_image.shape)
        np_image = np.clip(np_image + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(np_image)
    
    def color_inversion(self, image):
        np_image = np.array(image)
        np_image = 255 - np_image
        return Image.fromarray(np_image)
    
    def mirror_glitch(self, image, intensity):
        np_image = np.array(image)
        width = np_image.shape[1]
        for i in range(width // 2):
            if random.random() > (1 - intensity / 100.0):
                np_image[:, i], np_image[:, width - i - 1] = np_image[:, width - i - 1], np_image[:, i]
        return Image.fromarray(np_image)
    
    def data_fragmentation(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        for i in range(height):
            if random.random() > (1 - intensity / 100.0):
                offset = random.randint(0, width // 10)
                np_image[i] = np.roll(np_image[i], offset, axis=0)
        return Image.fromarray(np_image)
    
    def image_distortion(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        for i in range(width):
            if random.random() > (1 - intensity / 100.0):
                offset = random.randint(-height // 10, height // 10)
                np_image[:, i] = np.roll(np_image[:, i], offset, axis=0)
        return Image.fromarray(np_image)
    
    def glitch_vertical_bars(self, image, intensity):
        np_image = np.array(image)
        width = np_image.shape[1]
        bar_width = max(1, int(width * intensity / 100.0))
        for i in range(0, width, bar_width):
            if random.random() > (1 - intensity / 100.0):
                np_image[:, i:i + bar_width] = np.random.randint(0, 256, (np_image.shape[0], bar_width, 3))
        return Image.fromarray(np_image)
    
    def glitch_horizontal_bars(self, image, intensity):
        np_image = np.array(image)
        height = np_image.shape[0]
        bar_height = max(1, int(height * intensity / 100.0))
        for i in range(0, height, bar_height):
            if random.random() > (1 - intensity / 100.0):
                np_image[i:i + bar_height, :] = np.random.randint(0, 256, (bar_height, np_image.shape[1], 3))
        return Image.fromarray(np_image)
    
    def random_pixelation(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        pixelation_size = max(1, int(min(width, height) * intensity / 100.0))
        for y in range(0, height, pixelation_size):
            for x in range(0, width, pixelation_size):
                if random.random() > (1 - intensity / 100.0):
                    color = np_image[y:y + pixelation_size, x:x + pixelation_size].mean(axis=(0, 1))
                    np_image[y:y + pixelation_size, x:x + pixelation_size] = color
        return Image.fromarray(np_image)
    
    def toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("background-color: #ffffff;")  # Light mode
            self.scroll_area.setStyleSheet("background-color: #ffffff;")
            self.image_widget.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.dark_mode = False
        else:
            self.setStyleSheet("background-color: #1e1e1e;")  # Dark mode
            self.scroll_area.setStyleSheet("background-color: #1e1e1e;")
            self.image_widget.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")
            self.dark_mode = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GlitchArtApp()
    ex.show()
    sys.exit(app.exec_())
