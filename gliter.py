import sys
import random
import io
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QComboBox, QProgressBar, QHBoxLayout, QSlider, QScrollArea, QDialog
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About GLITER 1.0")
        self.setGeometry(200, 200, 300, 300)  # Adjusted size to fit additional content
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Application information
        about_text = (
            "<b>GLITER 1.0 - GLITCH IMAGE TOOL</b><br><br>"
            "Developed by mtz in collaboration with ChatGPT.<br>"
            "Version: 1.0.2<br><br>"
            "TO HELP PEOPLE CREATE WITHOUT LIMITS.<br><br>"
            "MAY THE ART CREATED WITH THIS PROGRAM BRING PEACE TO THIS DOOMED WORLD<br><br>"
            "MADE IN BRASIL :D<br><br>"
            "Follow:<br>"
            '<a href="https://x.com/mtz_treze">Twitter: @mtz.treze</a><br>'
            '<a href="https://www.instagram.com/empty.mtz">Instagram: @empty.mtz</a><br>'
        )
        
        about_label = QLabel(about_text, self)
        about_label.setWordWrap(True)
        about_label.setOpenExternalLinks(True)  # Allow links to be clickable
        
        layout.addWidget(about_label)
        
        # Close button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

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
            "Simple Glitch", "Data Corruption", "Line Glitch",
            "Static Noise", "Data Fragmentation", "Image Distortion",
            "Random Pixelation", "RGB Shift", "Wave Distortion", "Glitch Strips"
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
        
        # About button
        self.about_button = QPushButton('About', self)
        self.about_button.clicked.connect(self.show_about_dialog)
        button_layout.addWidget(self.about_button)
        
        # Add effects and buttons to layout
        main_layout.addLayout(effect_layout)
        main_layout.addLayout(button_layout)
        
        # Set main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    def show_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec_()
    
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
                glitched_image = self.apply_effect(self.original_image.copy(), selected_effect, intensity)
                
                self.display_image(glitched_image)
                self.save_button.setEnabled(True)  # Enable the save button
                self.glitched_image = glitched_image  # Store the glitched image
        except Exception as e:
            self.image_widget.setText(f"Failed to apply glitch: {str(e)}")
    
    def apply_effect(self, image, effect_name, intensity):
        effects = {
            "Simple Glitch": self.simple_glitch,
            "Data Corruption": self.data_corruption,
            #"Color Shift": self.color_shift,
            "Line Glitch": self.line_glitch,
            "Static Noise": self.static_noise,
            "Data Fragmentation": self.data_fragmentation,
            "Image Distortion": self.image_distortion,
            "Random Pixelation": self.random_pixelation,
            "RGB Shift": self.rgb_shift,
            "Wave Distortion": self.wave_distortion,
            "Glitch Strips": self.glitch_strips
        }
        
        if effect_name in effects:
            return effects[effect_name](image, intensity)
        return image
    
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
    
    # Effect implementations
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
    
    #def color_shift(self, image):
        np_image = np.array(image)
        np_image = np_image[..., [2, 0, 1]]  # Shift colors from RGB to BGR
        return Image.fromarray(np_image)
    
    def line_glitch(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        for i in range(height):
            if random.random() > (1 - intensity / 100.0):
                offset = random.randint(-width // 10, width // 10)
                np_image[i] = np.roll(np_image[i], offset, axis=0)
        return Image.fromarray(np_image)
    
    def static_noise(self, image, intensity):
        np_image = np.array(image)
        noise = np.random.normal(0, intensity, np_image.shape)
        np_image = np.clip(np_image + noise, 0, 255).astype(np.uint8)
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
    
    def random_pixelation(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        pixel_size = random.randint(5, 20)  # Size of pixelation blocks
        for i in range(0, width, pixel_size):
            for j in range(0, height, pixel_size):
                color = np_image[j:j+pixel_size, i:i+pixel_size].mean(axis=(0, 1))
                np_image[j:j+pixel_size, i:i+pixel_size] = color
        return Image.fromarray(np_image)
    
    def rgb_shift(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        shift = intensity // 10  # Shift amount based on intensity
        r_shift = random.randint(-shift, shift)
        g_shift = random.randint(-shift, shift)
        b_shift = random.randint(-shift, shift)
        r_channel = np.roll(np_image[:, :, 0], r_shift, axis=1)
        g_channel = np.roll(np_image[:, :, 1], g_shift, axis=1)
        b_channel = np.roll(np_image[:, :, 2], b_shift, axis=1)
        np_image[:, :, 0] = r_channel
        np_image[:, :, 1] = g_channel
        np_image[:, :, 2] = b_channel
        return Image.fromarray(np_image)
    
    def wave_distortion(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        for i in range(width):
            offset = int(np.sin(i / 20.0) * intensity)
            np_image[:, i] = np.roll(np_image[:, i], offset, axis=0)
        return Image.fromarray(np_image)
    
    def glitch_strips(self, image, intensity):
        np_image = np.array(image)
        height, width, _ = np_image.shape
        num_strips = max(1, int(width * intensity / 100))  # Garantir pelo menos 1 tira

        min_width = 5
        min_height = 5

        for _ in range(num_strips):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            max_w = width - x
            max_h = height - y
            
            if max_w <= min_width or max_h <= min_height:
                continue
            
            w = random.randint(min_width, min(20, max_w))
            h = random.randint(min_height, min(20, max_h))

            # Verificar se o retângulo está dentro dos limites da imagem
            x_end = min(x + w, width)
            y_end = min(y + h, height)
            
            if x_end <= x or y_end <= y:
                continue

            np_image[y:y_end, x:x_end] = np.random.randint(0, 256, (y_end - y, x_end - x, 3), dtype=np.uint8)
        
        return Image.fromarray(np_image)

    def toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("background-color: #ffffff;")
            self.scroll_area.setStyleSheet("background-color: #e0e0e0;")
            self.image_widget.setStyleSheet("background-color: #ffffff;")
            self.dark_mode = False
        else:
            self.setStyleSheet("background-color: #1e1e1e;")
            self.scroll_area.setStyleSheet("background-color: #1e1e1e;")
            self.image_widget.setStyleSheet("background-color: #1e1e1e;")
            self.dark_mode = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GlitchArtApp()
    ex.show()
    sys.exit(app.exec_())
