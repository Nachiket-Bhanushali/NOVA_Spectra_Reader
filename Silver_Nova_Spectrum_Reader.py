import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel,
                             QHBoxLayout, QLineEdit, QGroupBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def parser(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()[1:]
    int_time = int(lines[0][9:-1])  # integration time in ms
    lines = lines[1:]
    parsed_data = lines
    for i in range(len(lines)):
        lines[i] = lines[i].strip().split(',')[0].split()
        parsed_data[i] = [float(s.strip()) for s in lines[i]]
    parsed_data.sort(key=lambda x: x[0])
    return int_time, parsed_data

class DataPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Silver NOVA Spectrum Reader')
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Create and add buttons in a horizontal layout
        button_layout = QHBoxLayout()

        # Create and add widgets
        self.browse_button = QPushButton('Browse and Open File(s)')
        self.browse_button.clicked.connect(self.open_files)
        button_layout.addWidget(self.browse_button)

        self.plot_button = QPushButton('Plot Data')
        self.plot_button.clicked.connect(self.plot_data)
        self.plot_button.setEnabled(False)  # Disable initially
        button_layout.addWidget(self.plot_button)

        self.rescale_button = QPushButton('Rescale and Plot Data')
        self.rescale_button.clicked.connect(self.rescale_and_plot)
        self.rescale_button.setEnabled(False)  # Disable initially
        button_layout.addWidget(self.rescale_button)

        self.clear_button = QPushButton('Clear Plot')
        self.clear_button.clicked.connect(self.clear_plot)
        button_layout.addWidget(self.clear_button)

        # Add the button layout to the main layout
        self.main_layout.addLayout(button_layout)

        self.status_label = QLabel('No file loaded.')
        self.main_layout.addWidget(self.status_label)

        # Add input fields for axes ranges
        self.create_axes_input()

        # Create Matplotlib figure and canvas
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.main_layout.addWidget(self.canvas)

        self.data_list = []  # To hold data from multiple files
        self.file_names = []
        self.short_file_names = []

    def create_axes_input(self):
        # Group box for axes ranges
        axes_group = QGroupBox("Set Axes Ranges")
        axes_layout = QHBoxLayout()
        axes_group.setLayout(axes_layout)

        # X-axis range inputs
        self.x_min_input = QLineEdit(self)
        self.x_min_input.setPlaceholderText("X Min")
        axes_layout.addWidget(QLabel("X Min:"))
        axes_layout.addWidget(self.x_min_input)

        self.x_max_input = QLineEdit(self)
        self.x_max_input.setPlaceholderText("X Max")
        axes_layout.addWidget(QLabel("X Max:"))
        axes_layout.addWidget(self.x_max_input)

        # Y-axis range inputs
        self.y_min_input = QLineEdit(self)
        self.y_min_input.setPlaceholderText("Y Min")
        axes_layout.addWidget(QLabel("Y Min:"))
        axes_layout.addWidget(self.y_min_input)

        self.y_max_input = QLineEdit(self)
        self.y_max_input.setPlaceholderText("Y Max")
        axes_layout.addWidget(QLabel("Y Max:"))
        axes_layout.addWidget(self.y_max_input)

        self.main_layout.addWidget(axes_group)

    def open_files(self):
        options = QFileDialog.Options()
        self.file_names, _ = QFileDialog.getOpenFileNames(self, "Open Data Files", "",
                                                   "SSM Files (*.ssm);;All Files (*)", options=options)
        self.short_file_names = [os.path.basename(file).split('/')[-1] for file in self.file_names]
        if self.file_names:
            self.data_list = [parser(file)[1] for file in self.file_names]
            self.status_label.setText(f'Loaded files: {", ".join(self.short_file_names)}')
            self.plot_button.setEnabled(True)  # Enable plot button
            self.rescale_button.setEnabled(True)  # Enable rescale button

    def get_axes_ranges(self):
        try:
            x_min = float(self.x_min_input.text()) if self.x_min_input.text() else None
            x_max = float(self.x_max_input.text()) if self.x_max_input.text() else None
            y_min = float(self.y_min_input.text()) if self.y_min_input.text() else None
            y_max = float(self.y_max_input.text()) if self.y_max_input.text() else None
        except ValueError:
            self.status_label.setText('Invalid axis range input.')
            return None, None, None, None
        return x_min, x_max, y_min, y_max

    def apply_axes_ranges(self, ax):
        x_min, x_max, y_min, y_max = self.get_axes_ranges()
        if x_min is not None and x_max is not None:
            ax.set_xlim([x_min, x_max])
        if y_min is not None and y_max is not None:
            ax.set_ylim([y_min, y_max])

    def plot_data(self):
        if self.data_list is not None:
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            for i in range(len(self.data_list)):
                x, y = zip(*self.data_list[i])
                ax.plot(x, y, label=self.short_file_names[i])

            self.apply_axes_ranges(ax)
            ax.set_xlabel(r'$\lambda$ (nm)')
            ax.set_ylabel('Counts')
            ax.grid(True)
            ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center')
            self.figure.tight_layout()
            self.canvas.draw()
        else:
            self.status_label.setText('No data to plot.')

    def rescale_and_plot(self):
        if self.data_list is not None:
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            for i in range(len(self.data_list)):
                x, y = zip(*self.data_list[i])
                if max(y) != 0:
                    y_scaled = np.array(y) / max(y)
                    ax.plot(x, y_scaled, label=self.short_file_names[i])
                else:
                    self.status_label.setText('Max value is zero, cannot rescale.')

                ax.set_xlabel(r'$\lambda$ (nm)')
                ax.set_ylabel('Intensity (arb)')
                ax.grid(True)
                ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center')
                self.figure.tight_layout()
                self.apply_axes_ranges(ax)
                self.canvas.draw()

        else:
            self.status_label.setText('No data to plot.')

    def clear_plot(self):
        self.figure.clear()
        self.canvas.draw()
        self.data_list = []
        self.status_label.setText('Plot cleared. Ready to start over.')
        self.plot_button.setEnabled(False)
        self.rescale_button.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = DataPlotter()
    main_window.show()
    sys.exit(app.exec_())
