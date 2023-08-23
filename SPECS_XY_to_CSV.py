import os
import time
import csv
import tkinter as tk
from tkinter import filedialog

def ensure_module_import(module_name):
    try:
        __import__(module_name)
    except ImportError:
        import pip
        pip.main(['install', module_name])
        __import__(module_name)

ensure_module_import('pandas')
ensure_module_import('matplotlib.pyplot')
ensure_module_import('sqlite3')
ensure_module_import('math')

def xy_to_csv(output_directory_name):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    if not file_path:
        print("No file selected.")
        return

    # Create an output directory
    try:
        os.makedirs(output_directory_name)
        print("Data folder created.")
    except FileExistsError:
        print("Data folder already exists.")
        return

    with open(file_path, 'r') as csvfile:
        plots = list(csv.reader(csvfile, delimiter=' '))

    k = 1
    file_name_prefix = "Measurement_"
    current_file = None

    print("Start")
    starttime = time.time()

    for plot in plots:
        if plot and plot[0] == "#":
            if len(plot) > 1 and plot[1] == "Region:":
                if current_file:
                    current_file.close()

                suffix = "_".join(filter(None, plot[2:]))
                file_name = os.path.join(output_directory_name, f"{file_name_prefix}{k}_{suffix}.csv")
                current_file = open(file_name, 'w')
                current_file.write("Binding Energy,Intensity\n")
                current_file.write("eV,cps\n")
                k += 1
        elif plot:
            current_file.write(",".join(filter(None, plot)) + "\n")

    if current_file:
        current_file.close()

    stoptime = time.time()
    runtime = stoptime - starttime
    print("Finished")
    print(f"Total time: {runtime}")

xy_to_csv("Test")
