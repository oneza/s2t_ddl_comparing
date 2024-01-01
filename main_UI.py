from PyQt6.QtWidgets import *
from subclass_UI import Tabs


class UI(QMainWindow):

    def __init__(self):
        super().__init__()

        table_widget = Tabs(self)

        layout = QGridLayout()
        layout.addWidget(table_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
