from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QStackedWidget, QPushButton, QLineEdit
from instruments import *


class Generator(QWidget):
    table_column_name = ''
    names_column_name = ''
    type_column_name = ''
    decimal_column_name = ''
    source_column_name = ''

    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        mapping_selection_text = QLabel(self)
        mapping_selection_text.setText("Select mapping files: ")
        mapping_selection_value_text = QLabel(self)
        mapping_selection_value_text.setText('')
        mapping_selection = QPushButton(self)
        mapping_selection.setText("...")
        mapping_selection.clicked.connect(lambda: self.open_mapping_dialog())
        mapping_selection.clicked.connect(
            lambda: self.update_text(mapping_selection_value_text, f'{self.mapping_addresses}'))

        source_name_text = QLabel(self)
        source_name_text.setText("Fill in letters of source attributes column: ")
        source_name_value_text = QLineEdit(self)
        source_name_value_text.setText('')
        source_name_value_text.textChanged.connect(lambda: self.change_text(source_name_value_text.text(), 'source'))

        table_name_text = QLabel(self)
        table_name_text.setText("Fill in letters of table name column: ")
        table_name_value_text = QLineEdit(self)
        table_name_value_text.setText('')
        table_name_value_text.textChanged.connect(lambda: self.change_text(table_name_value_text.text(), 'table'))

        column_name_text = QLabel(self)
        column_name_text.setText("Fill in letters of column name column: ")
        column_name_value_text = QLineEdit(self)
        column_name_value_text.setText('')
        column_name_value_text.textChanged.connect(lambda: self.change_text(column_name_value_text.text(), 'name'))

        dtype_name_text = QLabel(self)
        dtype_name_text.setText("Fill in letters of data type name column: ")
        dtype_name_value_text = QLineEdit(self)
        dtype_name_value_text.setText('')
        dtype_name_value_text.textChanged.connect(lambda: self.change_text(dtype_name_value_text.text(), 'dtype'))

        layout.addWidget(source_name_text, 0, 0)
        layout.addWidget(source_name_value_text, 0, 1)
        layout.addWidget(table_name_text, 1, 0)
        layout.addWidget(table_name_value_text, 1, 1)
        layout.addWidget(column_name_text, 2, 0)
        layout.addWidget(column_name_value_text, 2, 1)
        layout.addWidget(dtype_name_text, 3, 0)
        layout.addWidget(dtype_name_value_text, 3, 1)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.switch_screen_btn = QPushButton("Switch Screen")
        layout.addWidget(self.switch_screen_btn)
        self.switch_screen_btn.clicked.connect(self.switch_screen)

    def switch_screen(self, num_of_mappings):
        num_screens = num_of_mappings + 1  # Replace with actual user input

        current_screen_count = self.stacked_widget.count()

        if num_screens > current_screen_count:
            for i in range(num_screens - current_screen_count):
                self.stacked_widget.addWidget(ScreenWidget())
        elif num_screens < current_screen_count:
            for i in range(current_screen_count - num_screens):
                self.stacked_widget.removeWidget(self.stacked_widget.widget(0))
        # Change the current screen as needed, for example: self.stacked_widget.setCurrentIndex(0)

    @classmethod
    def change_text(cls, text, column_name):
        if column_name == 'table':
            cls.table_column_name = text
        elif column_name == 'name':
            cls.names_column_name = text
        elif column_name == 'dtype':
            cls.type_column_name = text
        elif column_name == 'decimal':
            cls.decimal_column_name = text
        elif column_name == 'source':
            cls.source_column_name = text
        else:
            pass


class ScreenWidget(QWidget):
# Define the content of each screen here
    pass