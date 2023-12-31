from PyQt6.QtWidgets import *
import sys
import pandas as pd


def beautify_string(text):
    return text\
        .lower()\
        .strip()\
        .replace('с', 'c')\
        .replace('а', 'a')\
        .replace('е', 'e')


def beautify_decimals(text):
    if text and '(' not in text:
        text = '(' + text + ')'
    return text.replace('.', ',')


def mapping_df(mapping_file, columns_string):
    if len(columns_string.split(',')) == 4:
        df_mapping = pd.read_excel(mapping_file,
                                   sheet_name=4,
                                   header=1,
                                   usecols=columns_string,
                                   names=['mapping_tbl_name',
                                          'mapping_column_name',
                                          'mapping_column_type',
                                          'mapping_column_length'],
                                   converters={'mapping_column_length': str})\
            .fillna('')
    else:
        df_mapping = pd.read_excel(mapping_file,
                                   sheet_name=4,
                                   header=1,
                                   usecols=columns_string,
                                   names=['mapping_tbl_name', 'mapping_column_name', 'mapping_column_type'])
    return df_mapping


def get_ddl_data(file_name):
    with open(file_name) as f:
        data = f.read()

    data_splitted = [_.split('ROW FORMAT SERDE')[0].replace('|\n|', '').replace('-', '')
                     for _ in data.split('createtab_stmt')][1:]
    data_splitted = [_.replace('PARTITIONED BY (', '') if 'PARTITIONED BY (' in _ else _ for _ in data_splitted]
    data_splitted = [_.split('COMMENT')[0] if 'COMMENT' in _ else _ for _ in data_splitted]

    return data_splitted


def get_table_name(table_ddl):
    table_name = table_ddl\
        .split('(')[0]\
        .split('.')[1]\
        .replace('`', '')

    return table_name.lower()


def get_column_info(table_ddl):
    column_data = table_ddl \
        .split('(')
    if len(column_data) > 2:
        column_data_new = ''
        for substr in column_data[1:]:
            column_data_new += substr
    else:
        column_data_new = column_data[1]

    column_data_new = column_data_new \
        .replace(' ', '') \
        .replace('`', ' ') \
        .replace(')', ',') \
        .split(',')
    column_data_new = [_.lstrip() for _ in column_data_new if _ != '']

    return column_data_new


def set_ddl_df(ddl):
    tables_data = []
    for table in ddl:
        table_name = get_table_name(table)
        columns = get_column_info(table)
        columns_res = []
        k = 1
        for i in range(len(columns)):
            if len(columns[i]) == 1:
                columns_res[i-k] = columns_res[i-k].replace('decimal', 'decimal(') + ',' + columns[i] + ')'
                k += 1
            else:
                columns_res.append(columns[i])
        rows = [(table_name, _.split(' ')[0], _.split(' ')[1]) for _ in columns_res]

        tables_data += rows

    return tables_data


def highlight(s):
    if s.tbl_name_ok == 0 or s.column_name_ok == 0 or s.column_type_ok == 0:
        return ['background-color: yellow'] * len(s)
    else:
        return ['background-color: white'] * len(s)


class Main(QMainWindow):
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
        mapping_selection.clicked.connect(lambda: self.update_text(mapping_selection_value_text, f'{self.mapping_addresses}'))

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

        # tbl_name_text = QLabel(self)
        # tbl_name_text.setText("Fill in letters of columns: ")
        # tbl_name_value_text = QLineEdit(self)
        # tbl_name_value_text.setText('')
        # tbl_name_value_text.textChanged.connect(self.change_text)

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
        decimal_checkbox.stateChanged.connect(lambda: self.set_visible(decimal_checkbox, decimals_additional_text, decimals_additional_text_value))
        decimals_additional_text = QLabel(self)
        decimals_additional_text.setText("Fill in letters of length column:")
        decimals_additional_text.setVisible(False)
        decimals_additional_text_value = QLineEdit(self)
        decimals_additional_text_value.setText('')
        decimals_additional_text_value.textChanged.connect(lambda: self.change_text(decimals_additional_text_value.text(), 'decimal'))
        decimals_additional_text_value.setVisible(False)

        run_button = QPushButton(self)
        run_button.setText("Run")
        run_button.clicked.connect(lambda: self.main_function())
        run_button.clicked.connect(lambda: self.run_button_dialog())

        layout = QGridLayout()
        layout.addWidget(mapping_selection_text, 0, 0)
        layout.addWidget(mapping_selection_value_text, 0, 1)
        layout.addWidget(mapping_selection, 0, 2)
        layout.addWidget(ddl_selection_text, 1, 0)
        layout.addWidget(ddl_selection_value_text, 1, 1)
        layout.addWidget(ddl_selection, 1, 2)
        layout.addWidget(folder_selection_text, 2, 0)
        layout.addWidget(folder_selection_value_text, 2, 1)
        layout.addWidget(folder_selection, 2, 2)
        layout.addWidget(table_name_text, 4, 0)
        layout.addWidget(table_name_value_text, 4, 1)
        layout.addWidget(column_name_text, 5, 0)
        layout.addWidget(column_name_value_text, 5, 1)
        layout.addWidget(dtype_name_text, 6, 0)
        layout.addWidget(dtype_name_value_text, 6, 1)
        layout.addWidget(decimals_text, 7, 0)
        layout.addWidget(decimal_checkbox, 7, 1)
        layout.addWidget(decimals_additional_text, 7, 2)
        layout.addWidget(decimals_additional_text_value, 7, 3)

        layout.addWidget(run_button, 8, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setFixedWidth(600)

    def run_button_dialog(self):
        dlg = QMessageBox(self)
        dlg.setText("All done!")
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
            "${HOME}",
            "Text Files (*.txt)",
        )
        cls.ddl_addr = fname[0]
        # print(fname)

    @classmethod
    def open_mapping_dialog(cls):
        fname = QFileDialog.getOpenFileNames(
            QWidget(),
            "Open File",
            "${HOME}",
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

    def set_visible(self, checkbox, *args):
        if checkbox.isChecked():
            for arg in args:
                arg.setVisible(True)
        else:
            for arg in args:
                arg.setVisible(False)

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
            df_mappings['mapping_column_type'] = [beautify_string(_[0])+beautify_decimals(_[1]) for _ in
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_gui = Main()
    main_gui.show()
    sys.exit(app.exec())
