from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QStackedWidget, QPushButton, QScrollArea, \
    QLineEdit, QFileDialog, QCheckBox, QComboBox
from instruments import *


class Generator(QWidget):
    mapping_addresses = []
    table_column_name = ''
    names_column_name = ''
    type_column_name = ''
    decimal_column_name = ''
    source_column_name = ''

    def __init__(self):
        super().__init__()

        self.payload = 0
        excel_file = "C:/Users/Capit/Desktop/test_mapping.xlsx"
        self.excel_df = mapping_df(excel_file, 'G,U,V,Z,AA')  # Replace with actual user input
        # self.excel_df = pd.DataFrame
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.line_edits = []

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        self.switch_screen_btn = QPushButton("Switch Screen")
        self.current_screen_index = 0
        # self.connect_line_edit_signals()

        self.init_screen()

    def init_screen(self):
        first_screen = QScrollArea()  # Create a scroll area for the first screen

        self.stacked_widget.addWidget(first_screen)

        inner_widget = QWidget()  # Create an inner widget for the scroll area
        layout = QGridLayout()
        inner_widget.setLayout(layout)

        first_screen.setWidgetResizable(True)
        first_screen.setWidget(inner_widget)

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

        decimals_additional_text = QLabel(self)
        decimals_additional_text.setText("Fill in letters of length column:")
        decimals_additional_text_value = QLineEdit(self)
        decimals_additional_text_value.setText('')
        decimals_additional_text_value.textChanged.connect(
            lambda: self.change_text(decimals_additional_text_value.text(), 'decimal'))

        payload_text = QLabel(self)
        payload_text.setText("Add payload?")
        payload_checkbox = QCheckBox()
        payload_checkbox.stateChanged.connect(lambda: self.add_payload(payload_checkbox))

        layout.addWidget(mapping_selection_text, 0, 0)
        layout.addWidget(mapping_selection_value_text, 0, 1)
        layout.addWidget(mapping_selection, 0, 2)
        layout.addWidget(source_name_text, 1, 0)
        layout.addWidget(source_name_value_text, 1, 1)
        layout.addWidget(table_name_text, 2, 0)
        layout.addWidget(table_name_value_text, 2, 1)
        layout.addWidget(column_name_text, 3, 0)
        layout.addWidget(column_name_value_text, 3, 1)
        layout.addWidget(dtype_name_text, 4, 0)
        layout.addWidget(dtype_name_value_text, 4, 1)
        layout.addWidget(decimals_additional_text, 5, 0)
        layout.addWidget(decimals_additional_text_value, 5, 1)
        layout.addWidget(payload_text, 6, 0)
        layout.addWidget(payload_checkbox, 6, 1)

        # self.switch_screen_btn.clicked.connect(self.set_excel_df)
        self.switch_screen_btn.clicked.connect(self.add_screens)
        self.switch_screen_btn.clicked.connect(self.switch_screen)

        layout.addWidget(self.switch_screen_btn)

    def add_screens(self):
        for index, dataframe in enumerate(split_df(self.excel_df).values(), start=1):
            screen_widget = QScrollArea()  # Create a scroll area for each screen
            self.stacked_widget.addWidget(screen_widget)

            inner_widget = QWidget()  # Add an inner widget to each scroll area
            layout = QGridLayout()
            inner_widget.setLayout(layout)

            screen_widget.setWidgetResizable(True)
            screen_widget.setWidget(inner_widget)

            table_name = dataframe['mapping_tbl_name'].values[0]
            for j, row in enumerate(dataframe.itertuples(), start=1):
                source_label = QLabel(f"Source name: ")
                if self.payload == 0:
                    source_line_edit = QLineEdit(str(row[1]), parent=screen_widget)
                else:
                    source_line_edit = QLineEdit(add_payload_link(str(row[1])), parent=screen_widget)
                target_label = QLabel(f"Target name: ")
                target_line_edit = QLineEdit(str(row[3]), parent=screen_widget)
                dtype_label = QLabel(f"Target dtype: ")
                dtype_line_edit = QLineEdit(str(row[4]), parent=screen_widget)
                length_label = QLabel(f"Target length: ")
                length_line_edit = QLineEdit(str(row[5]), parent=screen_widget)
                # source_line_edit.textChanged.connect(lambda: self.update_data(source_line_edit.text()))
                # target_line_edit.textChanged.connect(lambda: self.update_data(target_line_edit))
                # dtype_line_edit.textChanged.connect(lambda: self.update_data(dtype_line_edit))
                # length_line_edit.textChanged.connect(lambda: self.update_data(length_line_edit))
                self.line_edits.append(source_line_edit)
                self.line_edits.append(target_line_edit)
                self.line_edits.append(dtype_line_edit)
                self.line_edits.append(length_line_edit)
                layout.addWidget(source_label, j, 0)
                layout.addWidget(source_line_edit, j, 1)
                layout.addWidget(target_label, j, 2)
                layout.addWidget(target_line_edit, j, 3)
                layout.addWidget(dtype_label, j, 4)
                layout.addWidget(dtype_line_edit, j, 5)
                layout.addWidget(length_label, j, 6)
                layout.addWidget(length_line_edit, j, 7)

            load_type_label = QLabel(f"Target table name: ")
            load_type_dropmenu = self.add_load_type(screen_widget)
            pre_filter_label = QLabel(f"Prefilter condition: ")
            pre_filter_line_edit = QLineEdit('value like \'%meta_:{_Class_:_%\'', parent=screen_widget)
            post_filter_label = QLabel(f"Postfilter condition: ")
            post_filter_line_edit = QLineEdit('meta.Class = \'\'', parent=screen_widget)
            increment_value_label = QLabel(f"Increment value: ")
            increment_value_line_edit = QLineEdit('hdp_processed_dttm', parent=screen_widget)
            target_table_label, target_table_name = self.load_type('scd0append',
                                                                            target_table_name=table_name,
                                                                            screen_widget=screen_widget)

            layout.addWidget(load_type_label, 0, 0)
            layout.addWidget(load_type_dropmenu, 0, 1)
            layout.addWidget(pre_filter_label, j + 1, 0)
            layout.addWidget(pre_filter_line_edit, j + 1, 1)
            layout.addWidget(post_filter_label, j + 2, 0)
            layout.addWidget(post_filter_line_edit, j + 2, 1)
            layout.addWidget(increment_value_label, j + 3, 0)
            layout.addWidget(increment_value_line_edit, j + 3, 1)
            layout.addWidget(target_table_label, j + 4, 0)
            layout.addWidget(target_table_name, j + 4, 1)


            switch_screen_btn = QPushButton("Switch Screen")
            layout.addWidget(switch_screen_btn)
            switch_screen_btn.clicked.connect(self.switch_screen)
            switch_screen_btn.clicked.connect(self.update_data)
            # for line_edit in self.line_edits:
            #     line_edit.textChanged.connect(lambda text, line_edit=line_edit: self.update_data(text, line_edit))
            switch_screen_btn.clicked.connect(self.collect_data)
            self.stacked_widget.addWidget(screen_widget)

    def switch_screen(self):
        self.current_screen_index += 1
        if self.current_screen_index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(self.current_screen_index)
        else:
            print("No more screens to switch to")

    @classmethod
    def open_mapping_dialog(cls):
        fname = QFileDialog.getOpenFileNames(
            QWidget(),
            "Open File",
            "",
            "Excel Files (*.xlsx)",
        )
        cls.mapping_addresses = fname[0]

    def update_text(self, attr, text_string):
        attr.setText(text_string)

    def add_payload(self, checkbox):
        if checkbox.isChecked():
            self.payload = 1
        else:
            self.payload = 0

    def collect_data(self):
        current_screen = self.stacked_widget.currentWidget()  # Get the current scroll area

        inner_widget = current_screen.widget()  # Get the inner widget of the scroll area
        line_edits = inner_widget.findChildren(QLineEdit)
        # current_line_edits = [line_edit for line_edit in self.line_edits if line_edit in line_edits]

        data = {}
        for line_edit in line_edits:
            field_name = line_edit.parent().layout().itemAt(
                line_edit.parent().layout().indexOf(line_edit) - 1).widget().text()
            text = line_edit.text()
            if field_name in ['Source name: ', 'Target name: ', 'Target dtype: ', 'Target length: ']:
                if field_name in data:
                    data[field_name].append(text)
                else:
                    data[field_name] = [text]
        data_df = pd.DataFrame.from_dict(data)
        resulting_string = prepare_parsed_column(data_df)
        print(resulting_string)
        return resulting_string

    @classmethod
    def prepare_excel(cls):

        columns_string = cls.source_column_name.upper() + ',' + cls.table_column_name.upper() + ',' \
                         + cls.names_column_name.upper() + ',' \
                         + cls.type_column_name.upper()
        if cls.decimal_column_name:
            columns_string = columns_string + ',' + cls.decimal_column_name.upper()
        print(columns_string)
        mappings_dict = {}
        for i in range(len(cls.mapping_addresses)):
            mappings_dict[f'df_{i + 1}'] = mapping_df(cls.mapping_addresses[i], columns_string)

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

        return df_mappings

    def set_excel_df(self):
        self.excel_df = self.prepare_excel()

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

    def update_data(self):
        for line_edit in self.line_edits:
            line_edit.setText(line_edit.text())

    def load_type(self, load_type, **kwargs):
        match load_type.lower():
            case 'scd0append':
                target_table_label = QLabel(f"Target table name: ")
                target_table_line_edit = QLineEdit(str(kwargs['target_table_name']), parent=kwargs['screen_widget'])
                return target_table_label, target_table_line_edit
            case 'scd1distinct':
                pass
            case 'scd2migration':
                pass
    def add_load_type(self, parent):
        load_type_dropmenu = QComboBox(parent=parent)
        load_type_dropmenu.addItems(['Scd0Append', 'Scd1Distinct', 'Scd2Migration'])
        return load_type_dropmenu
