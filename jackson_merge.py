import os
import tkinter

import pandas as pd
import logging
import calendar
import time
import pysftp as sftp
import pgpy
import dill
import tkinter as tk
from tkinter import filedialog

# IMPORTANT NOTE #
#  If you want to use this file, you need to have the files "Directory file.csv"
# and "Manually maintained file.csv" in the same level that this file.
# After running the file it will create 2 new files, the log and the result file with the
# updated information ready.

# Libraries need it:
# - pandas
# - logging
# - calendar
# - time
# - pysftp
# - tkinter
# - pyinstaller (only if you are going to create the exe file)

# Open files and create a variable to dont run on errors

gmt = time.gmtime()
ts = calendar.timegm(gmt)
logging.basicConfig(filename=f"logs_{ts}.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
main_filename_root = ""
photo_filename_root = ""


def mainbrowseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    global main_filename_root
    main_filename_root = filename
    window.destroy()

def photobrowseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    global photo_filename_root
    photo_filename_root = filename
    window.destroy()



#Main file
# Create the root window
window = tk.Tk()

# Set window title
window.title('File Explorer')

# Set window size
window.geometry("200x200")

# Set window background color
window.config(background="white")

# Create a File Explorer label
label_file_explorer = tk.Label(window,
                               text="Select the main file",
                               width=25, height=4,
                               fg="blue")
button_explore = tk.Button(window,
                           text="Browse File",
                           command=mainbrowseFiles)
button_exit = tk.Button(window,
                        text="Exit",
                        command=exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=1, row=1)
button_explore.grid(column=1, row=2)
button_exit.grid(column=1, row=3)

# Let the window wait for any events
window.mainloop()


#Photo file
# Create the root window
window = tk.Tk()

# Set window title
window.title('File Explorer')

# Set window size
window.geometry("200x200")

# Set window background color
window.config(background="white")

# Create a File Explorer label
label_file_explorer = tk.Label(window,
                               text="Select the photo file",
                               width=25, height=4,
                               fg="blue")
button_explore = tk.Button(window,
                           text="Browse File",
                           command=photobrowseFiles)
button_exit = tk.Button(window,
                        text="Exit",
                        command=exit)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column=1, row=1)
button_explore.grid(column=1, row=2)
button_exit.grid(column=1, row=3)

# Let the window wait for any events
window.mainloop()

## Merging process

main_file = pd.read_csv(main_filename_root, index_col=0)
photo_file = pd.read_csv(photo_filename_root, index_col=0, header=None)
non_existing_index = []

for index, row in photo_file.iterrows():
    if not index == '**Trailer**':
        index_to_use = index
        try:
            main_file._get_value(index=index_to_use, col='Photo')
        except:
            if isinstance(index_to_use, str):
                index_to_use = int(index_to_use)
            else:
                index_to_use = str(index_to_use)
        try:
            main_file._get_value(index=index_to_use, col='Photo')
            main_file._set_value(index=index_to_use, col='Photo', value=row[1])
        except KeyError as e:
            print(f'Index {index_to_use} dont exist')
            non_existing_index.append(index_to_use)
        except ValueError as e:
            print(f'Value {index_to_use} its an invalid literal')

main_file.to_csv("jackson_result.csv")

# Creating the root window
root = tk.Tk()
root.title('Index that dont exist')
root.geometry("400x400")

# Creating a Listbox and
# attaching it to root window
listbox = tk.Listbox(root)

# Adding Listbox to the left
# side of root window
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Creating a Scrollbar and
# attaching it to root window
scrollbar = tk.Scrollbar(root)

# Adding Scrollbar to the right
# side of root window
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

# Insert elements into the listbox
for values in non_existing_index:
    listbox.insert(tk.END, values)

# Attaching Listbox to Scrollbar
# Since we need to have a vertical
# scroll we use yscrollcommand
listbox.config(yscrollcommand=scrollbar.set)

# setting scrollbar command parameter
# to listbox.yview method its yview because
# we need to have a vertical view
scrollbar.config(command=listbox.yview)

button_upload = tk.Button(root,text="Upload File!", command=root.quit)

button_exit = tk.Button(root,
                        text="Exit",
                        command=exit)
button_exit.pack(side=tk.BOTTOM)
button_upload.pack(side=tk.BOTTOM)

root.mainloop()

pubKey, _ = pgpy.PGPKey.from_file('demo-appengineering_pub.gpg')
# filename_parts = filename_root.split("/")
# filename_root = filename_parts[::-1][0]
file_message = pgpy.PGPMessage.new('jackson_result.csv', file=True)
encryptedData = pubKey.encrypt(file_message)

with open('result_upload.gpg', 'wb') as file:
    dill.dump(encryptedData, file)

logging.info("Uploading file")

FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')
cnopts = sftp.CnOpts()
cnopts.hostkeys = None

with sftp.Connection(host=FTP_HOST, username=FTP_USER, password=FTP_PASS, cnopts=cnopts) as sftp:
    #   A 'You will need to explicitly load HostKeys' warning it's going to trigger,
    # for now just ignore it, this will be solved once that we decide how to store
    # credentials
    logging.info("Connection successfully established ... ")
    sftp.put('result_upload.gpg')
    logging.info("File uploaded successfully")

# Closes the connection
sftp.close()

logging.info("Upload finished, press Enter to close this window!")

window = tk.Tk()
window.title('CSV Upload')
window.geometry("300x100")
label_columns = tk.Label(text="File its ready and uploaded on the server!", anchor='n')
label_columns.pack()

var = tk.IntVar()
button = tk.Button(window, text="Close", command=lambda: var.set(1))
button.place(relx=.5, rely=.5, anchor="s")
button.wait_variable(var)

window.destroy()

logging.info("Closing CSV Upload")

import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = os.getenv('SENDER_EMAIL')
password = os.getenv('SENDER_PASS')
receiver_email = os.getenv('RECEIVER_EMAIL')

message = """\
Subject: File encripted

This message is sent to notify that the file has being encrypted and uploaded to the server."""

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Can be omitted
    server.starttls(context=context)  # Secure the connection
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()
