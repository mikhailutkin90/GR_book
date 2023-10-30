import csv
import dropbox

def save_to_temp(file_name_entry, data_to_add):
    temp_csv_file_name = "/" + file_name_entry.get() + "_temp.csv"
    with open('key.txt', 'r') as file:
        key = file.read() #get the access key for dropbox
    
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
        if row[9] != 0: 
            new_rows.append(row)
        
    csv_data.extend(new_rows)

    for row in csv_data:
        row_count +=1

    modified_csv_content = '\n'.join([','.join(map(str, row)) for row in csv_data])
    dbx.files_upload(modified_csv_content.encode('utf-8'), temp_csv_file_name, mode=dropbox.files.WriteMode('overwrite'))

    

def compmm(file_name_entry):

    mod_csv_file_name = "/" + file_name_entry.get() + "_mod.csv"
    temp_csv_file_name = "/" + file_name_entry.get() + "_temp.csv"
    output_csv_file_name = file_name_entry.get() + "_output.csv"
    with open('key.txt', 'r') as file:
        key = file.read() #get the access key for dropbox

    dbx = dropbox.Dropbox(key)

    _, response = dbx.files_download(mod_csv_file_name)
    # Read and decode the CSV content
    csv_content = response.content.decode('utf-8')
    # Read the rows from the mod CSV file into a set
    file1_rows = set()
    csv_reader = csv.reader(csv_content.splitlines())
    for row in csv_reader:
        if row:  # Skip empty rows
            row = row[0].split(',')
            row_number = int(row[0])  
            file1_rows.add(row_number)

    # Read the rows from the temp CSV file into a set
    _, response = dbx.files_download(temp_csv_file_name)
    csv_content = response.content.decode('utf-8')
    file2_rows = set()
    csv_reader = csv.reader(csv_content.splitlines())
    for row in csv_reader:
        if row:  # Skip empty rows
            row = row[0].split(',')
            row_number = int(row[0])  # Assuming the row number is in the first column
            file2_rows.add(row_number)

    # Find the rows that are unique to the first file
    
    unique_rows = file1_rows - file2_rows
    #make a new file with unique rows
    with open(output_csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:              
        csv_writer = csv.writer(csvfile)

        _, response = dbx.files_download(mod_csv_file_name)
        csv_content = response.content.decode('utf-8')
        csv_reader = csv.reader(csv_content.splitlines())
        for row in csv_reader:
            if row and int(row[0]) in unique_rows:
                csv_writer.writerow(row)

                # Upload the CSV file to Dropbox
    with open(output_csv_file_name, 'rb') as file:
        dbx.files_upload(file.read(), f'/{output_csv_file_name}', mode=dropbox.files.WriteMode.overwrite)
