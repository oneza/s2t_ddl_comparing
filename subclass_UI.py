from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QCheckBox, QTabWidget, QGridLayout


class Tabs(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        mapping_selection_text = QLabel(self)
        mapping_selection_text.setText("Select mapping files: ")
        mapping_selection_value_text = QLabel(self)
        mapping_selection_value_text.setText('')
        mapping_selection = QPushButton(self)
        mapping_selection.setText("...")
        mapping_selection.clicked.connect(lambda: self.open_mapping_dialog())
        mapping_selection.clicked.connect(
            lambda: self.update_text(mapping_selection_value_text, f'{self.mapping_addresses}'))

        ddl_selection_text = QLabel(self)
        ddl_selection_text.setText("Select ddl file: ")
        ddl_selection_value_text = QLabel(self)
        ddl_selection_value_text.setText('')
        ddl_selection = QPushButton(self)
        ddl_selection.setText("...")
        ddl_selection.clicked.connect(lambda: self.open_dialog())
        ddl_selection.clicked.connect(lambda: self.update_text(ddl_selection_value_text, f'{self.ddl_addr}'))

        folder_selection_text = QLabel(self)
        folder_selection_text.setText("Select filename to save: ")
        folder_selection_value_text = QLabel(self)
        folder_selection_value_text.setText('')
        folder_selection = QPushButton(self)
        folder_selection.setText("...")
        folder_selection.clicked.connect(lambda: self.save_file_dialog())
        folder_selection.clicked.connect(lambda: self.update_text(folder_selection_value_text, f'{self.folder_addr}'))

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

        decimals_text = QLabel(self)
        decimals_text.setText("Are there decimals?")
        decimal_checkbox = QCheckBox()
        decimal_checkbox.stateChanged.connect(
            lambda: self.set_visible(decimal_checkbox, decimals_additional_text, decimals_additional_text_value))
        decimals_additional_text = QLabel(self)
        decimals_additional_text.setText("Fill in letters of length column:")
        decimals_additional_text.setVisible(False)
        decimals_additional_text_value = QLineEdit(self)
        decimals_additional_text_value.setText('')
        decimals_additional_text_value.textChanged.connect(
            lambda: self.change_text(decimals_additional_text_value.text(), 'decimal'))
        decimals_additional_text_value.setVisible(False)

        run_button = QPushButton(self)
        run_button.setText("Run")
        run_button.clicked.connect(lambda: self.main_function())
        run_button.clicked.connect(lambda: self.run_button_dialog())

        tab = QTabWidget()

        check_page = QWidget(tab)
        check_page_layout = QGridLayout()
        check_page_layout.addWidget(mapping_selection_text, 0, 0)
        check_page_layout.addWidget(mapping_selection_value_text, 0, 1)
        check_page_layout.addWidget(mapping_selection, 0, 2)
        check_page_layout.addWidget(ddl_selection_text, 1, 0)
        check_page_layout.addWidget(ddl_selection_value_text, 1, 1)
        check_page_layout.addWidget(ddl_selection, 1, 2)
        check_page_layout.addWidget(folder_selection_text, 2, 0)
        check_page_layout.addWidget(folder_selection_value_text, 2, 1)
        check_page_layout.addWidget(folder_selection, 2, 2)
        check_page_layout.addWidget(table_name_text, 4, 0)
        check_page_layout.addWidget(table_name_value_text, 4, 1)
        check_page_layout.addWidget(column_name_text, 5, 0)
        check_page_layout.addWidget(column_name_value_text, 5, 1)
        check_page_layout.addWidget(dtype_name_text, 6, 0)
        check_page_layout.addWidget(dtype_name_value_text, 6, 1)
        check_page_layout.addWidget(decimals_text, 7, 0)
        check_page_layout.addWidget(decimal_checkbox, 7, 1)
        check_page_layout.addWidget(decimals_additional_text, 7, 2)
        check_page_layout.addWidget(decimals_additional_text_value, 7, 3)

        check_page_layout.addWidget(run_button, 8, 0)
        check_page.setLayout(check_page_layout)

        tab.addTab(check_page, 'Compare')

        gen_page = QWidget(tab)
        gen_page_layout = QGridLayout()

        some_text = QLabel(self)
        some_text.setText("SEcond tab text")

        another_some_text = QLabel(self)
        another_some_text.setText("Some additional text")

        gen_page_layout.addWidget(some_text, 0, 0)
        gen_page_layout.addWidget(another_some_text, 1, 0)

        gen_page.setLayout(gen_page_layout)

        tab.addTab(gen_page, 'Generate')

        layout.addWidget(tab)
        self.setLayout(layout)

    def set_visible(self, checkbox, *args):
        if checkbox.isChecked():
            for arg in args:
                arg.setVisible(True)
        else:
            for arg in args:
                arg.setVisible(False)
