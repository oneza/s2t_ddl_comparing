from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QCheckBox, QTabWidget, QGridLayout


class Generator(QWidget):

    def __init__(self):
        super().__init__()

        some_text = QLabel(self)
        some_text.setText("KAVO????")

        another_some_text = QLabel(self)
        another_some_text.setText("DAB DAB DAB")

        gen_page_layout = QGridLayout()
        gen_page_layout.addWidget(some_text, 0, 0)
        gen_page_layout.addWidget(another_some_text, 1, 0)

        self.setLayout(gen_page_layout)
