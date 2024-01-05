from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QStackedWidget, QPushButton, QScrollArea, \
    QLineEdit
from instruments import *


class Generator(QWidget):

    def __init__(self, excel_file):
        super().__init__()

        self.excel_df = self.mapping_df(excel_file, 'U,V,Z,AA') # Replace with actual user input
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        self.switch_screen_btn = QPushButton("Switch Screen")
        self.current_screen_index = 0

        self.init_screen(excel_file)

    def init_screen(self, excel_file):
        first_screen = QScrollArea()  # Create a scroll area for the first screen

        self.stacked_widget.addWidget(first_screen)

        inner_widget = QWidget()  # Create an inner widget for the scroll area
        layout = QVBoxLayout()
        inner_widget.setLayout(layout)

        first_screen.setWidgetResizable(True)
        first_screen.setWidget(inner_widget)

        # Create fields for user to fill information
        for i in range(5):
            label = QLabel(f"Field {i + 1}: ")
            line_edit = QLineEdit()
            layout.addWidget(label)
            layout.addWidget(line_edit)

        self.switch_screen_btn.clicked.connect(self.add_screens)
        self.switch_screen_btn.clicked.connect(self.switch_screen)
        current_screen_count = self.stacked_widget.count()

        layout.addWidget(self.switch_screen_btn)

    def add_screens(self):
        # current_screen_count = self.stacked_widget.count()
        for index, dataframe in enumerate(split_df(self.excel_df).values(), start=1):
            screen_widget = QScrollArea()  # Create a scroll area for each screen
            self.stacked_widget.addWidget(screen_widget)

            inner_widget = QWidget()  # Add an inner widget to each scroll area
            # layout = QVBoxLayout()
            layout = QGridLayout()
            inner_widget.setLayout(layout)

            screen_widget.setWidgetResizable(True)
            screen_widget.setWidget(inner_widget)

            for j, row in enumerate(dataframe.itertuples()):
                # for value in row:
                source_label = QLabel(f"Source name: ")
                source_line_edit = QLineEdit(str(row[1]), parent=screen_widget)
                target_label = QLabel(f"Source name: ")
                target_line_edit = QLineEdit(str(row[1]), parent=screen_widget)
                dtype_label = QLabel(f"Source name: ")
                dtype_line_edit = QLineEdit(str(row[1]), parent=screen_widget)
                length_label = QLabel(f"Source name: ")
                length_line_edit = QLineEdit(str(row[1]), parent=screen_widget)
                layout.addWidget(source_label, j, 0)
                layout.addWidget(source_line_edit, j, 1)
                layout.addWidget(target_label, j, 2)
                layout.addWidget(target_line_edit, j, 3)
                layout.addWidget(dtype_label, j, 4)
                layout.addWidget(dtype_line_edit, j, 5)
                layout.addWidget(length_label, j, 6)
                layout.addWidget(length_line_edit, j, 7)

            switch_screen_btn = QPushButton("Switch Screen")
            layout.addWidget(switch_screen_btn)
            switch_screen_btn.clicked.connect(self.switch_screen)
            self.stacked_widget.addWidget(screen_widget)

    def switch_screen(self):
        self.current_screen_index += 1

        if self.current_screen_index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(self.current_screen_index)
        else:
            print("No more screens to switch to")
