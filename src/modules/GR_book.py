import read_data
import update_workbook
import comparison_fun
import data_dict
import tkinter as tk
from tkinter import ttk

global file_name_entry

def validate_input(P):
    '''allows the user to enter only numbers'''
    return P.isdigit()

def clear_widgets():
    '''clears widgets, is used every time the main table is updated'''
    for widget in frame.grid_slaves():
        info = widget.grid_info()
        if info["row"] > 1 and info["column"] < 8:
            widget.grid_remove()
        if info["row"] == 0 and info["column"] == 5:
            widget.grid_remove()
        if info["row"] == 0 and info["column"] == 6:
            widget.grid_remove()

def make_table():
    '''Reads the data from _remain_source.csv and makes 
    coresponding entry fields for the user in the GUI.
    Calls data_check function'''
    clear_widgets()
    global row_count
    transaction_dates = read_data.remain_source_read(file_name_entry)[0]
    transaction_names = read_data.remain_source_read(file_name_entry)[1]
    transaction_ammounts = read_data.remain_source_read(file_name_entry)[2]
    row_count = read_data.remain_source_read(file_name_entry)[3]
    transaction_numbers = read_data.remain_source_read(file_name_entry)[4]
    checkbox_state_vat24 = [tk.IntVar() for _ in range(row_count)]
    checkbox_state_vat0 = [tk.IntVar() for _ in range(row_count)]
    for_manual_check = [tk.IntVar() for _ in range(row_count)]
    code_entry = [0] * (row_count)

    def data_check():
        '''Checks the data entered by the user and calls recursion'''

        def input_recursion():
            '''Saves data entered by user data in the current cycle to save_to_cum_input.csv.
            Calls comparison function.
            Makes a cycle by calling make_table function'''
            comparison_fun.save_to_cum_input(file_name_entry, data_to_add)
            comparison_fun.comp(file_name_entry)
            remaining_rows = comparison_fun.comp(file_name_entry)
            make_table()
            if remaining_rows == 0:
                style = ttk.Style()
                style.configure("Green.TButton", foreground="green")
                ttk.Button(frame, text="Update_workbook", command=lambda: update_workbook.update_workbook(file_name_entry),
                        style="Green.TButton").grid(row=30, column=7)
                tk.Label(frame, text="Data updated successfully", foreground = "green").grid(row=30, column=8)

        data_to_add = []
        row = []
       
        for i in range(row_count):
            row = [transaction_numbers[i], transaction_dates[i], transaction_names[i], transaction_ammounts[i], (checkbox_state_vat24[i].get()), 
                   (checkbox_state_vat0[i].get()), (for_manual_check[i].get()), int(code_entry[i].get())]
            data_to_add.append(row)
        
        i = 1
        err = 0
        for row in data_to_add:
            if row[4] !=0 and row[5] !=0:
                #vat can be only 24 or 0, else choose for_manual_entry
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=7)
                err += 1
            elif ((row[4] or row[5]) !=0) and row[7] == 0:
                #if vat is entered then code should be entered
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=7)
                err += 1
            elif row[7] != 0 and ((row[4] or row[5]) == 0):
                #if vat is entered then code should be entered
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=7)
                err += 1
            elif row[6] == 1 and ((row[4] or row[5] or row[7]) != 0):
                #if manual entry then all other values should be = 0
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=7)
                err += 1
            elif (9999 < row[7]) or ((0 < row[7]) and (row[7] < 1000)):
                #if code entered is in acceptable value range
                tk.Label(frame, text="***", foreground = "red").grid(row=(i+1), column=7)
                err += 1   
            else:
                tk.Label(frame, text="   ").grid(row=(i+1), column=7)
            if err > 0:
                tk.Label(frame, text="Correct lines marked: ***", foreground = "red").grid(row=(0), column=5)
            else: 
                tk.Label(frame, text="   Input data is correct   ", foreground = "green").grid(row=(0), column=5)  
            i += 1

        ttk.Button(frame, text="Save and update the table", command=input_recursion).grid(row=0, column=6)
        

    for i in range((row_count)):
        tk.Label(frame, text=transaction_dates[i]).grid(row=(i+2), column=0)
        tk.Label(frame, text=transaction_names[i]).grid(row=(i+2), column=1)
        tk.Label(frame, text=transaction_ammounts[i]).grid(row=(i+2), column=2)
        tk.Checkbutton(frame, variable=checkbox_state_vat24[i]).grid(row=i+2, column=3)
        tk.Checkbutton(frame, variable=checkbox_state_vat0[i]).grid(row=i+2, column=4)
        tk.Checkbutton(frame, variable=for_manual_check[i]).grid(row=i+2, column=5)
        code_entry[i] = ttk.Entry(frame, validate="key", validatecommand=(validate_input_command, "%P"))
        code_entry[i].insert(0, "0")
        code_entry[i].grid(row=i+2, column=6)
    ttk.Button(frame, text="Check data", command=data_check).grid(row=0, column=4)
           
def valid_run():
    '''Validates if the file uploaded by the user exists and runs the GUI data table creation'''
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
canvas = tk.Canvas(root, width=1500, height=800)
canvas.grid(row=0, column=0)
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

tk.Label(frame, text="Date").grid(row=1, column=0)
tk.Label(frame, text="Name").grid(row=1, column=1)
tk.Label(frame, text="Ammount").grid(row=1, column=2)
tk.Label(frame, text="VAT24%").grid(row=1, column=3)
tk.Label(frame, text="VAT 0%").grid(row=1, column=4)
tk.Label(frame, text="For manual check").grid(row=1, column=5)
tk.Label(frame, text="Enter code").grid(row=1, column=6)
tk.Label(frame, text="Enter file name eg.: august_2023").grid(row=0, column=0)
file_name_entry = ttk.Entry(frame)
file_name_entry.grid(row=0, column=1)
file_button = ttk.Button(frame, text="Import data", command=valid_run).grid(row=0, column=2)


codes = data_dict.code_dict()
i = 0
for x, y in codes.items():
    codes_label=tk.Label(frame, text= (x + " " + y))
    if i < 25:
        codes_label.grid(row=(i+1), column=8, sticky=tk.W)
    else:
        codes_label.grid(row=(i-24), column=9, sticky=tk.W)
    i += 1

v_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
v_scrollbar.grid(row=0, column=10)
canvas.configure(yscrollcommand=v_scrollbar.set)

frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))


root.mainloop()