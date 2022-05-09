import pandas as pd
import logging
import calendar
import time
import inquirer

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

## Check manually file for duplicates

duplicateRowsManually = manually_file[manually_file.duplicated()]
if len(duplicateRowsManually) > 0:
    logging.warning("Found duplicates on manually file, please check the next IDs")
    logging.warning(list(duplicateRowsManually['ID']))

## Check if manually have invalid IDs

manually_file_ids = list(manually_file['ID'])
directory_file_ids = list(directory_file['ID'])
invalid_ids_on_manually = set(manually_file_ids).symmetric_difference(directory_file_ids)
if len(invalid_ids_on_manually) > 0:
    logging.warning("Found invalid IDs on manually file, please check the next IDs")
    logging.warning(list(invalid_ids_on_manually))

if not any_fatal_error:
    # Checking columns that user wants to update

    columns_in_manual_file = list(manually_file.columns)[1::]

    questions = [inquirer.Checkbox(
        'columns',
        message="Select with an X the columns that you "
                "dont want to update using arrows and SPACE key."
                " Then press ENTER",

        choices=columns_in_manual_file,
    )]

    answers = inquirer.prompt(questions)
    columns_after_user_choise = answers['columns']

    for column_name in columns_after_user_choise:
        manually_file.drop(column_name, axis=1, inplace=True)

    # Updating the file
    directory_file.set_index('ID', inplace=True)
    manually_file.set_index('ID', inplace=True)
    directory_file.update(manually_file)
    directory_file = directory_file.reset_index()

    directory_file.to_csv("result.csv", index=False)

logging.info("Closing CSV Merge")
print("Closing CSV Merge")
