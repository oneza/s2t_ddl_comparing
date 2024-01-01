from PyQt6.QtWidgets import *
from comparator_UI import Comparator


class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        table_widget = Comparator(self)

        layout = QGridLayout()
        layout.addWidget(table_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
