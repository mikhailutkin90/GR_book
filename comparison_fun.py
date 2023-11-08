import csv
import dropbox

def save_to_temp(file_name_entry, data_to_add):
    '''Opens the __temp.csv file and adds rows filled by user to it'''
    temp_csv_file_name = "/" + file_name_entry.get() + "_temp.csv"
    with open('key.txt', 'r', encoding='utf-8') as file:
        key = file.read()  

    dbx = dropbox.Dropbox(key)

    _, res = dbx.files_download(temp_csv_file_name)
    file_content = res.content.decode('utf-8')

    csv_data = []
    csv_reader = csv.reader(file_content.splitlines())
    for row in csv_reader:
        csv_data.append(row)

    new_rows = []
    row_count = 0
    for row in data_to_add:
        if row[9] != 0: #row[9] is a mandatory nonzero transaction code 
            new_rows.append(row)

    csv_data.extend(new_rows)

    for row in csv_data:
        row_count += 1

    modified_content = '\n'.join([','.join(map(str, row)) for row in csv_data])
    dbx.files_upload(modified_content.encode('utf-8'), 
                     temp_csv_file_name, mode=dropbox.files.WriteMode('overwrite'))

def comp(file_name_entry):
    '''Compares data from the __temp.csv file to the data from the source: source_mod.csv file
    and writes unique rows to the __output.csv file'''
    source_mod = "/" + file_name_entry.get() + "_source_mod.csv"
    temp_csv_file_name = "/" + file_name_entry.get() + "_temp.csv"
    output_csv_file_name = file_name_entry.get() + "_output.csv"
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

    _, response = dbx.files_download(temp_csv_file_name)
    csv_content = response.content.decode('utf-8')
    file2_rows = set()
    csv_reader = csv.reader(csv_content.splitlines())
    for row in csv_reader:
        if row:  
            row = row[0].split(',')
            row_number = int(row[0])  
            file2_rows.add(row_number)

    unique_rows = file1_rows - file2_rows

    with open(output_csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        _, response = dbx.files_download(source_mod)
        csv_content = response.content.decode('utf-8')
        csv_reader = csv.reader(csv_content.splitlines())
        for row in csv_reader:
            if row and int(row[0]) in unique_rows:
                csv_writer.writerow(row)
    with open(output_csv_file_name, 'rb') as file:
        dbx.files_upload(file.read(), f'/{output_csv_file_name}',
                          mode=dropbox.files.WriteMode.overwrite)
