import csv
import dropbox

def source_read(file_name_entry):
    '''Reads data into lists from the source file_name_entry.csv file 
    uploaded by the user to the project folder on dropbox. 
    Creates modified source __source_mod.csv file with only needed data.
    Creates empty __temp.csv file if it does not exist.'''

    csv_file_path = "/" + file_name_entry.get() + ".csv"
    with open('key.txt', 'r') as file:
        key = file.read() 

    dbx = dropbox.Dropbox(key)
    result = dbx.files_list_folder('')

    for val in result.entries:
            if val.name == file_name_entry.get() + ".csv":
                _, response = dbx.files_download(csv_file_path)
                csv_content = response.content.decode('utf-8')
                row_count=0
                csv_reader = csv.reader(csv_content.splitlines())
                for row in csv_reader:
                    row_count += 1                
                transaction_ammounts = [None] * (row_count-1)
                transaction_dates = [None] * (row_count-1)
                transaction_names = [None] * (row_count-1)

                csv_reader = csv.reader(csv_content.splitlines(), delimiter = ';')

                next(csv_reader, None)
                            
                for i in range(row_count-1):
                    next_row = next(csv_reader)
                    
                    transaction_dates[i] = next_row[0]
                    transaction_names[i] = next_row[5]
                    transaction_ammounts[i] = next_row[2]
                    transaction_ammounts[i] = transaction_ammounts[i].replace(',', '.')
                    transaction_ammounts[i] = float(transaction_ammounts[i])

                source_mod = file_name_entry.get() + "_source_mod.csv"
                
                with open(source_mod, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)

                    for i in range(row_count-1):
                        row = [i, transaction_dates[i], transaction_names[i], transaction_ammounts[i], 0, 0, 0, 0, 0, 0,]
                        csv_writer.writerow(row)
                with open(source_mod, 'rb') as file:
                    dbx.files_upload(file.read(), f'/{source_mod}', mode=dropbox.files.WriteMode.overwrite)
                #create empty temp if it does not exist
                temp_csv_file_name = file_name_entry.get() + "_temp.csv"
                re=True
                b=[]
                for val2 in result.entries:
                    b.append(val2.name) 
                for elem in b:
                    if elem == temp_csv_file_name:
                        re=False
                if re:
                    with open(temp_csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
                            csv_writer = csv.writer(csvfile)
                            csv_writer.writerow([])
                    with open(temp_csv_file_name, 'rb') as file:
                        dbx.files_upload(file.read(), f'/{temp_csv_file_name}')
                result = 1
                return result
            else:
                result = 0
                return result
            
def output_read(file_name_entry):
    '''Reads data into lists from __output.csv file.'''
    output_csv_file_path = "/" + file_name_entry.get() + "_output.csv"
    
    with open('key.txt', 'r') as file:
        key = file.read()

    dbx = dropbox.Dropbox(key)
    _, response = dbx.files_download(output_csv_file_path)
    csv_content = response.content.decode('utf-8')
    row_count=0
    csv_reader = csv.reader(csv_content.splitlines())
    for row in csv_reader:
        row_count += 1                
    transaction_numbers = [None] * (row_count)
    transaction_dates = [None] * (row_count)
    transaction_names = [None] * (row_count)
    transaction_ammounts = [None] * (row_count)

    csv_reader = csv.reader(csv_content.splitlines(), delimiter = ';')

    for i in range(row_count):
        next_row = next(csv_reader)
        next_row = next_row[0].split(',')
        transaction_numbers[i] = next_row[0]
        transaction_dates[i] = next_row[1]
        transaction_names[i] = next_row[2]
        transaction_ammounts[i] = float(next_row[3])
    return transaction_dates, transaction_names, transaction_ammounts, row_count, transaction_numbers



               