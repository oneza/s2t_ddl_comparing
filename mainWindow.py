from PyQt6.QtWidgets import *
from compareTab import Comparator
from generateTab import Generator


class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main App Window')

        # excel_file_path = "C:/Users/Capit/Desktop/test_mapping.xlsx"  # Replace with actual path to the excel file
        # tab2 = Generator(excel_file_path)
        tab2 = Generator()
        tab_widget = QTabWidget()
        tab_widget.addTab(Comparator(), "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")

        self.setCentralWidget(tab_widget)
        self.setFixedWidth(820)
        # self.setFixedHeight(700)
        self.setWindowTitle("Some useful app")