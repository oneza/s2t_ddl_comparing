import pandas as pd


def beautify_string(text):
    return text\
        .lower()\
        .strip()\
        .replace('с', 'c')\
        .replace('а', 'a')\
        .replace('е', 'e')


def beautify_decimals(text):
    if text:
        if '(' not in text:
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