import read_data
import comparison_fun
import data_dict
import tkinter as tk
from tkinter import ttk

global file_name_entry

def validate_input(P):
    '''allows the user to enter only numbers'''
    return P.isdigit()

def make_table():
    '''Reads the data from __output.csv and makes 
    coresponding entry fields for the user in the GUI.
    Calls data_check function'''
    global row_count
    transaction_dates = read_data.output_read(file_name_entry)[0]
    transaction_names = read_data.output_read(file_name_entry)[1]
    transaction_ammounts = read_data.output_read(file_name_entry)[2]
    row_count = read_data.output_read(file_name_entry)[3]
    transaction_numbers = read_data.output_read(file_name_entry)[4]
    checkbox_state_vat24 = [tk.IntVar() for _ in range(row_count)]
    vat_entry1 = [None] * (row_count)
    vat_ammount_entry1 = [0] * (row_count)
    vat_entry2 = [0] * (row_count)
    vat_ammount_entry2 = [0] * (row_count)
    code_entry = [0] * (row_count)

    def data_check():
        '''Checks the data entered by the user and calls recursion'''

        def temp_recursion():
            '''Saves data entered by user in the current cycle to __temp.csv.
            Calls comparison function.
            Makes a cycle by calling make_table function'''
            comparison_fun.save_to_temp(file_name_entry, data_to_add)
            comparison_fun.compare(file_name_entry)
            make_table()

        data_to_add = []
        row = []
       
        for i in range(row_count):
            row = [transaction_numbers[i], transaction_dates[i], transaction_names[i], transaction_ammounts[i], (checkbox_state_vat24[i].get()), int(vat_entry1[i].get()), 
                float(vat_ammount_entry1[i].get()), int(vat_entry2[i].get()), float(vat_ammount_entry2[i].get()), int(code_entry[i].get())]
            data_to_add.append(row)
        
        i = 1
        err = 0
        for row in data_to_add:
            if row[4] !=0 and (row[5] or row[6] or row[7] or row[8]) !=0:
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=9)
                err += 1
            elif ((row[4] or row[5] or row[6] or row[7] or row[8]) !=0) and row[9] == 0:
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=9)
                err += 1
            elif (9999 < row[9]) or ((0 < row[9]) and (row[9] < 1763)):
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=9)
                err += 1   
            elif (row[5] != 0 and row[6] == 0) or (row[6] != 0 and row[5] == 0):
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=9)
                err += 1
            else:
                tk.Label(frame, text="   ").grid(row=(i+1), column=9)
            if err > 0:
                tk.Label(frame, text="Correct lines marked: ***", foreground = "red").grid(row=(0), column=5)
            else: 
                tk.Label(frame, text="   Input data is correct   ", foreground = "green").grid(row=(0), column=5)
                
            i += 1
        ttk.Button(frame, text="Save and update the table", command=temp_recursion).grid(row=0, column=6)
        

    for i in range((row_count)):
    
    
        def validate_input_vatammount(P):
            '''Validates user input in a Tkinter Entry widget
            to allow only valid numeric values and a single decimal point.'''
            return (P.replace('.', '', 1).isdigit() and P != "") or (P == "." and "." not in vat_ammount_entry1[i].get())
        

        def validate_input_vatammount2(P):
            '''Validates user input in a Tkinter Entry widget
            to allow only valid numeric values and a single decimal point.'''
            return (P.replace('.', '', 1).isdigit() and P != "") or (P == "." and "." not in vat_ammount_entry1[i].get())
        
        validate_input_command2 = root.register(validate_input_vatammount)
        validate_input_command3 = root.register(validate_input_vatammount2)

        tk.Label(frame, text=transaction_dates[i]).grid(row=(i+2), column=0)
        tk.Label(frame, text=transaction_names[i]).grid(row=(i+2), column=1)
        tk.Label(frame, text=transaction_ammounts[i]).grid(row=(i+2), column=2)
        tk.Checkbutton(frame, variable=checkbox_state_vat24[i]).grid(row=i+2, column=3)

        vat_entry1[i] = ttk.Entry(frame, validate="key", validatecommand=(validate_input_command, "%P"))
        vat_entry1[i].insert(0, "0")
        vat_entry1[i].grid(row=i+2, column=4)
        vat_ammount_entry1[i] = ttk.Entry(frame, validate="key", validatecommand=(validate_input_command2, "%P"))
        vat_ammount_entry1[i].insert(0, "0")
        vat_ammount_entry1[i].grid(row=i+2, column=5)
        vat_entry2[i] = ttk.Entry(frame, validate="key", validatecommand=(validate_input_command, "%P"))
        vat_entry2[i].insert(0, "0")
        vat_entry2[i].grid(row=i+2, column=6)
        vat_ammount_entry2[i] = ttk.Entry(frame, validate="key", validatecommand=(validate_input_command3, "%P"))
        vat_ammount_entry2[i].insert(0, "0")
        vat_ammount_entry2[i].grid(row=i+2, column=7)
        code_entry[i] = ttk.Entry(frame, validate="key", validatecommand=(validate_input_command, "%P"))
        code_entry[i].insert(0, "0")
        code_entry[i].grid(row=i+2, column=8)
    ttk.Button(frame, text="Check data", command=data_check).grid(row=0, column=4)
           
def valid_run():
    '''Validated if the file uploaded by the user exists and runs the GUI data table creation'''
    result= read_data.source_read(file_name_entry)
    if result > 0:
        tk.Label(frame, text="Data imported successfully", foreground = "green").grid(row=0, column=3)
        comparison_fun.comp(file_name_entry)
        make_table()
    else:
        tk.Label(frame, text="Wrong file name").grid(row=0, column=3)
    
root = tk.Tk()
root.title("Invoices")
validate_input_command = root.register(validate_input)
canvas = tk.Canvas(root, width=1700, height=800)
canvas.grid(row=0, column=0)
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

tk.Label(frame, text="Date").grid(row=1, column=0)
tk.Label(frame, text="Name").grid(row=1, column=1)
tk.Label(frame, text="Ammount").grid(row=1, column=2)
tk.Label(frame, text="VAT24%").grid(row=1, column=3)
tk.Label(frame, text="Vat1 in %").grid(row=1, column=4)
tk.Label(frame, text="Vat1 ammount").grid(row=1, column=5)
tk.Label(frame, text="Vat2 in %").grid(row=1, column=6)
tk.Label(frame, text="Vat2 ammount").grid(row=1, column=7)
tk.Label(frame, text="Enter code").grid(row=1, column=8)
tk.Label(frame, text="Enter file name eg.: august_2023").grid(row=0, column=0)
file_name_entry = ttk.Entry(frame)
file_name_entry.grid(row=0, column=1)
file_button = ttk.Button(frame, text="Import data", command=valid_run).grid(row=0, column=2)


codes = data_dict.code_dict()
i = 0
for x, y in codes.items():
    codes_label=tk.Label(frame, text= (x + " " + y))
    if i < 24:
        codes_label.grid(row=(i+1), column=10, sticky=tk.W)
    else:
        codes_label.grid(row=(i-23), column=11, sticky=tk.W)
    i += 1

v_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
v_scrollbar.grid(row=0, column=12)
canvas.configure(yscrollcommand=v_scrollbar.set)

frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))


root.mainloop()