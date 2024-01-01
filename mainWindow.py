from PyQt6.QtWidgets import *
# from subclass_UI import Tabs
from compareTab import Comparator
from generateTab import Generator


class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main App Window')

        tab_widget = QTabWidget()
        tab_widget.addTab(Comparator(), "Tab 1")
        tab_widget.addTab(Generator(), "Tab 2")

        self.setCentralWidget(tab_widget)
