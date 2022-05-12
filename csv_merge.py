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

manually_file = pd.read_csv("Manually maintained file.csv")
directory_file = pd.read_csv("Directory file.csv")
any_fatal_error = False

# Create Logs logic

gmt = time.gmtime()
ts = calendar.timegm(gmt)
logging.basicConfig(filename=f"logs_{ts}.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running CSV Merge")

# Checking for errors

## Check directory file for duplicates

duplicateRowsDirectory = directory_file[directory_file.duplicated()]
if len(duplicateRowsDirectory) > 0:
    logging.warning("Found duplicates on directory file, please check the next IDs")
    logging.warning(list(duplicateRowsDirectory['ID']))
directory_file.drop_duplicates(inplace=True)

## Check manually file for duplicates

duplicateRowsManually = manually_file[manually_file.duplicated()]
if len(duplicateRowsManually) > 0:
    logging.warning("Found duplicates on manually file, please check the next IDs")
    logging.warning(list(duplicateRowsManually['ID']))
manually_file.drop_duplicates(inplace=True)

## Check if manually have invalid IDs

manually_file_ids = list(manually_file['ID'])
directory_file_ids = list(directory_file['ID'])
invalid_ids_on_manually = set(manually_file_ids).symmetric_difference(directory_file_ids)
if len(invalid_ids_on_manually) > 0:
    logging.warning("Found invalid IDs on manually file, please check the next IDs")
    logging.warning(list(invalid_ids_on_manually))
manually_file.set_index("ID", inplace=True)
manually_file.drop(invalid_ids_on_manually, inplace=True)
manually_file.reset_index(inplace=True)

if not any_fatal_error:
    # Checking columns that user wants to update

    columns_in_manual_file = list(manually_file.columns)[1::]

    # Creating the UI

    window = tk.Tk()
    window.title('CSV Merge')
    sb = tk.Scrollbar(orient="vertical")
    text = tk.Text(window, width=40, height=20, yscrollcommand=sb.set)
    sb.config(command=text.yview)
    sb.pack(side="right", fill="y")
    text.pack(side="top", fill="both", expand=True)
    label_columns = tk.Label(text="Select the column that you want to override")
    label_columns.pack()

    options_list = {}

    for x in range(len(columns_in_manual_file)):
        check_value = tkinter.IntVar()
        checkbox = tk.Checkbutton(window, text=columns_in_manual_file[x], variable=check_value,
                                  padx=0,pady=0,bd=0)
        text.window_create("end", window=checkbox)
        text.insert("end", "\n")
        checkbox.toggle()
        options_list[columns_in_manual_file[x]] = check_value

    var = tk.IntVar()
    button = tk.Button(window, text="Create Result", command=lambda: var.set(1))
    button.place(relx=.5, rely=.5, anchor="w")

    button.wait_variable(var)

    window.destroy()

    columns_after_user_choise = []
    for key, value in options_list.items():
        if not value.get():
            columns_after_user_choise.append(key)

    # Outdated code for console use

    # questions = [inquirer.Checkbox(
    #     'columns',
    #     message="Select with an X the columns that you "
    #             "dont want to update using arrows and SPACE key."
    #             " Then press ENTER",
    #
    #     choices=columns_in_manual_file,
    # )]
    #
    # answers = inquirer.prompt(questions)
    # columns_after_user_choise = answers['columns']

    for column_name in columns_after_user_choise:
        manually_file.drop(column_name, axis=1, inplace=True)

    # Updating the file
    directory_file.set_index('ID', inplace=True)
    manually_file.set_index('ID', inplace=True)
    directory_file.update(manually_file)
    directory_file = directory_file.reset_index()

    directory_file.to_csv("result.csv", index=False)

logging.info('Encrypting file')

pubKey, _ = pgpy.PGPKey.from_file('test-scotiabankjamaica_pub.gpg')
file_message = pgpy.PGPMessage.new('result.csv', file=True)
encryptedData = pubKey.encrypt(file_message)

with open('result.pkl', 'wb') as file:
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
    sftp.put('result.pkl')
    logging.info("File uploaded successfully")

# Closes the connection
sftp.close()

window = tk.Tk()
window.title('CSV Merge')
window.geometry("300x100")
label_columns = tk.Label(text="File its ready and uploaded on the server!", anchor='n')
label_columns.pack()

var = tk.IntVar()
button = tk.Button(window, text="Close", command=lambda: var.set(1))
button.place(relx=.5, rely=.5, anchor="s")
button.wait_variable(var)

window.destroy()

logging.info("Closing CSV Merge")
