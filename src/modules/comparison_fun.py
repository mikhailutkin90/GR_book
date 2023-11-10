import csv
import dropbox

def save_to_cum_input(file_name_entry, data_to_add):
    '''Opens the _cum_input.csv file and adds rows filled by the user to it'''
    cum_input_file = "/" + file_name_entry.get() + "_cum_input.csv"
    with open('key.txt', 'r', encoding='utf-8') as file:
        key = file.read()  

    dbx = dropbox.Dropbox(key)

    _, res = dbx.files_download(cum_input_file)
    file_content = res.content.decode('utf-8')

    csv_data = []
    csv_reader = csv.reader(file_content.splitlines())
    for row in csv_reader:
        csv_data.append(row)

    new_rows = []
    row_count = 0
    for row in data_to_add:
        if row[7] != 0: #row[7] is a mandatory nonzero transaction code 
            new_rows.append(row)
        if row[6] == 1: #row[6] marks data as manual entry 
            new_rows.append(row)

    csv_data.extend(new_rows)

    for row in csv_data:
        row_count += 1

    modified_content = '\n'.join([','.join(map(str, row)) for row in csv_data])
    dbx.files_upload(modified_content.encode('utf-8'), 
                     cum_input_file, mode=dropbox.files.WriteMode('overwrite'))

def comp(file_name_entry):
    '''Compares data from the _cum_input.csv file to the data from _source_mod.csv file
    and writes unique rows to the _remain_source.csv file.
    _remain_source.csv contains the remaining rows to be filled by user'''
    source_mod = "/" + file_name_entry.get() + "_source_mod.csv"
    cum_input_file = "/" + file_name_entry.get() + "_cum_input.csv"
    remain_source = file_name_entry.get() + "_remain_source.csv"
    with open('key.txt', 'r', encoding='utf-8') as file:
        key = file.read()  

    dbx = dropbox.Dropbox(key)

    _, response = dbx.files_download(source_mod)
    csv_content = response.content.decode('utf-8')
    file1_rows = set()
    csv_reader = csv.reader(csv_content.splitlines())
    for row in csv_reader:
        if row:  
            row = row[0].split(',')
            row_number = int(row[0])
            file1_rows.add(row_number)

    _, response = dbx.files_download(cum_input_file)
    csv_content = response.content.decode('utf-8')
    file2_rows = set()
    csv_reader = csv.reader(csv_content.splitlines())
    for row in csv_reader:
        if row:  
            row = row[0].split(',')
            row_number = int(row[0])  
            file2_rows.add(row_number)

    unique_rows = file1_rows - file2_rows
    remaining_rows = len(unique_rows)
    with open(remain_source, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        _, response = dbx.files_download(source_mod)
        csv_content = response.content.decode('utf-8')
        csv_reader = csv.reader(csv_content.splitlines())
        for row in csv_reader:
            if row and int(row[0]) in unique_rows:
                csv_writer.writerow(row)
    with open(remain_source, 'rb') as file:
        dbx.files_upload(file.read(), f'/{remain_source}',
                          mode=dropbox.files.WriteMode.overwrite)
    return remaining_rows
