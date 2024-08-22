import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel,
                             QHBoxLayout, QLineEdit, QGroupBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DataPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Data Plotter')
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create and add widgets
        self.browse_button = QPushButton('Browse and Open File(s)')
        self.browse_button.clicked.connect(self.open_files)
        self.layout.addWidget(self.browse_button)

        self.plot_button = QPushButton('Plot Data')
        self.plot_button.clicked.connect(self.plot_data)
        self.plot_button.setEnabled(False)  # Disable initially
        self.layout.addWidget(self.plot_button)

        self.rescale_button = QPushButton('Rescale and Plot Data')
        self.rescale_button.clicked.connect(self.rescale_and_plot)
        self.rescale_button.setEnabled(False)  # Disable initially
        self.layout.addWidget(self.rescale_button)

        self.clear_button = QPushButton('Clear Plot')
        self.clear_button.clicked.connect(self.clear_plot)
        self.layout.addWidget(self.clear_button)

        self.status_label = QLabel('No file loaded.')
        self.layout.addWidget(self.status_label)

        # Add input fields for axes ranges
        self.create_axes_input()

        # Create Matplotlib figure and canvas
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.data_list = []  # To hold data from multiple files

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

        self.layout.addWidget(axes_group)

    def open_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Open Data Files", "",
                                                "All Files (*);;Text Files (*.txt);;CSV Files (*.csv)", options=options)
        short_file_names = [os.path.basename(file).split('/')[-1] for file in files]

        if files:
            self.data_list = [pd.read_csv(file) for file in files]
            self.status_label.setText(f'Loaded files: {", ".join(short_file_names)}')
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
        if self.data_list:
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            for data in self.data_list:
                if 'x' in data.columns and 'y' in data.columns:
                    ax.plot(data['x'], data['y'])
                else:
                    ax.text(0.5, 0.5, 'Invalid data format', ha='center', va='center')

            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title('Overlayed Data Plot')
            ax.legend()
            self.apply_axes_ranges(ax)
            self.canvas.draw()
        else:
            self.status_label.setText('No data to plot.')

    def rescale_and_plot(self):
        if self.data_list:
            self.figure.clear()
            ax = self.figure.add_subplot(111)

            for data in self.data_list:
                if 'y' in data.columns:
                    max_value = data['y'].max()
                    if max_value != 0:
                        data['y_rescaled'] = data['y'] / max_value
                        ax.plot(data['x'], data['y_rescaled'])
                    else:
                        self.status_label.setText('Max value is zero, cannot rescale.')
                else:
                    self.status_label.setText('No valid y data to rescale.')

            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis (Rescaled)')
            ax.set_title('Overlayed Rescaled Data Plot')
            ax.legend()
            self.apply_axes_ranges(ax)
            self.canvas.draw()

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
