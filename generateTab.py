from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QStackedWidget, QPushButton


class Generator(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.switch_screen_btn = QPushButton("Switch Screen")
        layout.addWidget(self.switch_screen_btn)
        self.switch_screen_btn.clicked.connect(self.switch_screen)

    def switch_screen(self):
        num_screens = 3  # Replace with actual user input

        current_screen_count = self.stacked_widget.count()

        if num_screens > current_screen_count:
            for i in range(num_screens - current_screen_count):
                self.stacked_widget.addWidget(ScreenWidget())
        elif num_screens < current_screen_count:
            for i in range(current_screen_count - num_screens):
                self.stacked_widget.removeWidget(self.stacked_widget.widget(0))
        # Change the current screen as needed, for example: self.stacked_widget.setCurrentIndex(0)


class ScreenWidget(QWidget):
# Define the content of each screen here
    pass