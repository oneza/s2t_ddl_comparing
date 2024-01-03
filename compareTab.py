from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QGridLayout, \
    QFileDialog, QMessageBox
from instruments import *


class Comparator(QWidget):
    mapping_addresses = []
    ddl_addr = ''
    folder_addr = ''
    column_names = ''
    names_column_name = ''
    type_column_name = ''
    table_column_name = ''
    decimal_column_name = ''

    def __init__(self):
        super().__init__()

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
        self.setLayout(check_page_layout)

    def set_visible(self, checkbox, *args):
        if checkbox.isChecked():
            for arg in args:
                arg.setVisible(True)
        else:
            for arg in args:
                arg.setVisible(False)

    def run_button_dialog(self):
        dlg = QMessageBox(self)
        dlg.setText("All done!")
        dlg.setWindowTitle("")
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            self.close()

    def update_text(self, attr, text_string):
        attr.setText(text_string)

    @classmethod
    def open_dialog(cls):
        fname = QFileDialog.getOpenFileName(
            QWidget(),
            "Open File",
            "",
            "Text Files (*.txt)",
        )
        cls.ddl_addr = fname[0]
        # print(fname)

    @classmethod
    def open_mapping_dialog(cls):
        fname = QFileDialog.getOpenFileNames(
            QWidget(),
            "Open File",
            "",
            "Excel Files (*.xlsx)",
        )
        cls.mapping_addresses = fname[0]
        # print(fname)

    @classmethod
    def save_file_dialog(cls):
        cls.folder_addr, _ = QFileDialog.getSaveFileName(QWidget(), "QFileDialog.getSaveFileName()", "",
                                                         "Excel Files (*.xlsx)")
        # if cls.folder_addr:
        #     print(cls.folder_addr)

    #   OK actually I found a way for it to work
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
        else:
            pass

    @classmethod
    def main_function(cls):

        columns_string = cls.table_column_name.upper() + ',' + cls.names_column_name.upper() + ',' \
                         + cls.type_column_name.upper()
        if cls.decimal_column_name:
            columns_string = columns_string + ',' + cls.decimal_column_name.upper()
        print(columns_string)
        mappings_dict = {}
        for i in range(len(cls.mapping_addresses)):
            mappings_dict[f'df_{i + 1}'] = mapping_df(cls.mapping_addresses[i], columns_string)

        # print(mappings_dict)

        if len(cls.mapping_addresses) > 1:
            df_mappings = pd.concat(mappings_dict.values(), ignore_index=True)
        else:
            df_mappings = mappings_dict['df_1']

        df_mappings['mapping_tbl_name'] = [beautify_string(_) for _ in df_mappings['mapping_tbl_name'].values]
        df_mappings['mapping_column_name'] = [beautify_string(_) for _ in df_mappings['mapping_column_name'].values]
        if len(columns_string.split(',')) == 4:
            df_mappings['mapping_column_type'] = [beautify_string(_[0]) + beautify_decimals(_[1]) for _ in
                                                  zip(df_mappings['mapping_column_type'].values,
                                                      df_mappings['mapping_column_length'].values)]
            df_mappings = df_mappings.drop(['mapping_column_length'], axis=1)
        else:
            df_mappings['mapping_column_type'] = [beautify_string(_) for _ in df_mappings['mapping_column_type'].values]

        df_ddls = pd.DataFrame(set_ddl_df(get_ddl_data(cls.ddl_addr)), columns=['ddl_tbl_name',
                                                                                'ddl_column_name',
                                                                                'ddl_column_type'])

        merge_result = pd.merge(df_mappings, df_ddls,
                                how='outer',
                                left_on=['mapping_tbl_name', 'mapping_column_name'],
                                right_on=['ddl_tbl_name', 'ddl_column_name'])
        merge_result['tbl_name_ok'] = [1 if _[0] == _[1] else 0 for _ in
                                       merge_result[['mapping_tbl_name', 'ddl_tbl_name']].values]
        merge_result['column_name_ok'] = [1 if _[0] == _[1] else 0 for _ in
                                          merge_result[['mapping_column_name', 'ddl_column_name']].values]
        merge_result['column_type_ok'] = [1 if _[0] == _[1] else 0 for _ in
                                          merge_result[['mapping_column_type', 'ddl_column_type']].values]

        df_res = merge_result.style.apply(highlight, axis=1)

        df_res.to_excel(cls.folder_addr, index=False)