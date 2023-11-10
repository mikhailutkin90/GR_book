import dropbox
from dropbox.oauth import DropboxOAuth2FlowNoRedirect
import tkinter as tk
from tkinter import ttk

def get_key():
    auth_code = auth_code_entry.get()
    x = auth_flow.finish(auth_code)
    access_token = x.access_token
    with open('key.txt', 'w') as file:
        file.write(access_token)

    import subprocess
    subprocess.Popen(["python", "GR_book.py"])
    root.quit()

with open("appkey.txt", 'r') as file:
    APP_KEY = file.readline().strip()
    APP_SECRET = file.readline().strip()

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
authorize_url = auth_flow.start()

root = tk.Tk()
root.title("GR_book")

tk.Label(root, text="GR_book app login window:").grid(row=0, column=0, sticky=tk.W)
tk.Label(root, text="Copy link to the browser").grid(row=1, column=0, sticky=tk.W)
url = ttk.Entry(root, width=85)
url.insert(0, authorize_url)
url.grid(row=1, column=1, sticky=tk.W)
tk.Label(root, text="Login to Dropbox and press allow").grid(row=2, column=0, sticky=tk.W)
tk.Label(root, text="Enter the auth code here: ").grid(row=3, column=0, sticky=tk.W)
auth_code_entry = ttk.Entry(root, width=85)
auth_code_entry.grid(row=3, column=1, sticky=tk.W)
ttk.Button(root, text="Log in", command=get_key).grid(row=4, column=0, sticky=tk.W)

root.mainloop()


