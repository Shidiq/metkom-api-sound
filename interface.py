import os
import subprocess

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QImageReader, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Filter GUI")
        self.setGeometry(200, 200, 800, 600)

        # Main Layout
        main_layout = QVBoxLayout()

        # File Selector
        self.file_path_label = QLabel("Choose a WAV file:")
        self.file_path = QLineEdit()
        self.file_path.setReadOnly(True)
        self.file_button = QPushButton("Browse")
        self.file_button.clicked.connect(self.browse_file)

        # Parameters
        self.cutoff_label = QLabel("Cutoff Frequency (Hz):")
        self.cutoff = QSpinBox()
        self.cutoff.setRange(0, 10000)
        self.cutoff.setValue(1000)

        self.width_label = QLabel("Width:")
        self.width = QLineEdit("50")

        self.ripple_label = QLabel("Ripple (dB):")
        self.ripple = QLineEdit("60")

        # Process Button
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_audio)

        # Tab Widget for Plots
        self.tabs = QTabWidget()
        self.signal_tab = QWidget()
        self.amplitude_tab = QWidget()
        self.impulse_tab = QWidget()

        self.tabs.addTab(self.signal_tab, "Signal Plot")
        self.tabs.addTab(self.amplitude_tab, "Amplitude Response")
        self.tabs.addTab(self.impulse_tab, "Impulse Response")

        # Add widgets to layouts
        main_layout.addWidget(self.file_path_label)
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(self.file_button)
        main_layout.addLayout(file_layout)

        main_layout.addWidget(self.cutoff_label)
        main_layout.addWidget(self.cutoff)
        main_layout.addWidget(self.width_label)
        main_layout.addWidget(self.width)
        main_layout.addWidget(self.ripple_label)
        main_layout.addWidget(self.ripple)
        main_layout.addWidget(self.process_button)
        main_layout.addWidget(self.tabs)

        # Set up each plot tab layout
        self.signal_layout = QVBoxLayout()
        self.signal_image = QLabel()
        self.signal_layout.addWidget(self.signal_image)
        self.signal_tab.setLayout(self.signal_layout)

        self.amplitude_layout = QVBoxLayout()
        self.amplitude_image = QLabel()
        self.amplitude_layout.addWidget(self.amplitude_image)
        self.amplitude_tab.setLayout(self.amplitude_layout)

        self.impulse_layout = QVBoxLayout()
        self.impulse_image = QLabel()
        self.impulse_layout.addWidget(self.impulse_image)
        self.impulse_tab.setLayout(self.impulse_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select WAV file", "", "Audio Files (*.wav)"
        )
        if file_path:
            self.file_path.setText(file_path)

    def process_audio(self):
        file_path = self.file_path.text()
        cutoff = self.cutoff.value()
        width = self.width.text()
        ripple_db = self.ripple.text()

        if not file_path:
            return

        # Run curl command for audio processing
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "filtered.wav")
        subprocess.run(
            [
                "curl",
                "-X",
                "POST",
                "-F",
                f"file=@{file_path}",
                "-F",
                f"cutoff={cutoff}",
                "-F",
                f"width={width}",
                "-F",
                f"ripple_db={ripple_db}",
                "http://127.0.0.1:5000/filter",
                "--output",
                output_file,
            ]
        )

        # Fetch and display plots
        self.fetch_plot("plot_signal.svg", self.signal_image)
        self.fetch_plot("plot_amplitude_response.svg", self.amplitude_image)
        self.fetch_plot("plot_impulse_response.svg", self.impulse_image)

    def fetch_plot(self, plot_name, image_label):
        output_dir = "output"
        plot_path = os.path.join(output_dir, plot_name)

        # Run curl command to fetch plot
        subprocess.run(
            [
                "curl",
                f"http://127.0.0.1:5000/{plot_name.replace('.svg', '')}",
                "--output",
                plot_path,
            ]
        )

        # Display the plot in the respective tab
        if os.path.exists(plot_path):
            reader = QImageReader(plot_path)
            reader.setScaledSize(QSize(1000, 500))
            high_res_pixmap = QPixmap.fromImage(reader.read())
            image_label.setPixmap(high_res_pixmap)
            image_label.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
