import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os, pandas as pd

from main_interface import StartPage

fpm_filepath, txt_filepath, losses_filepath, startup_params_filepath = "", "", "", ""


"""
This file is depreciated and only used for testing purposes now
"""


class RunProgram(tk.Frame):
    def __init__(self, master):
        """
        Interace function, will include all the original stuff from the program but with a convienient interface for use and
        interaction
        :return:
        """
        tk.Frame.__init__(self, master)
        # fpm_filepath = tk.StringVar()
        # txt_filepath = tk.StringVar()
        # startup_params_filepath = tk.StringVar()

        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(row=5, column=0, padx=5, pady=5)

        def select_file_fpm():
            # this will update a global variable of fpm_filepath with a selected file
            # this is not the right way to do this, but I can't figure out a better way for now
            filetypes = (
                ('text files', '*.fpm'),
                ('All files', '*.*')
            )
            cwd = os.getcwd()
            global fpm_filepath
            fpm_filepath = fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.join(cwd, "inputs"),
                filetypes=filetypes)

            # add conditional label for if fpm_filepath has a value
            if not len(fpm_filepath) == 0:
                var = tk.StringVar()
                var.set(str(fpm_filepath))
                label = tk.Label(self, textvariable=var)
                label.grid(row=0, column=1, padx=5, pady=5)


            # import the fpm file and show as example in dataframe, for testing purpose
            # windfarmer_df = pd.read_csv(fpm_filepath, sep="\t", header=9)

        def select_file_losses():
            # this will update a global variable of fpm_filepath with a selected file
            # this is not the right way to do this, but I can't figure out a better way for now
            filetypes = (
                ('text files', '*.ini'),
                ('All files', '*.*')
            )
            cwd = os.getcwd()
            global losses_filepath
            losses_filepath = fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.join(cwd, "inputs"),
                filetypes=filetypes)

            # add conditional label for if fpm_filepath has a value
            if not len(losses_filepath) == 0:
                var = tk.StringVar()
                var.set(str(losses_filepath))
                label = tk.Label(self, textvariable=var)
                label.grid(row=1, column=1, padx=5, pady=5)


        def select_file_startup_params():
            # this will update a global variable of fpm_filepath with a selected file
            # this is not the right way to do this, but I can't figure out a better way for now
            filetypes = (
                ('text files', '*.ini'),
                ('All files', '*.*')
            )
            cwd = os.getcwd()
            global startup_params_filepath
            startup_params_filepath = fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.join(cwd, "inputs"),
                filetypes=filetypes)

            # add conditional label for if fpm_filepath has a value
            if not len(startup_params_filepath) == 0:
                var = tk.StringVar()
                var.set(str(startup_params_filepath))
                label = tk.Label(self, textvariable=var)
                label.grid(row=2, column=1, padx=5, pady=5)


        def select_file_txt():
            # this will update a global variable of fpm_filepath with a selected file
            # this is not the right way to do this, but I can't figure out a better way for now
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )
            cwd = os.getcwd()
            global txt_filepath
            txt_filepath = fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.join(cwd, "inputs"),
                filetypes=filetypes)

            # add conditional label for if fpm_filepath has a value
            if not len(txt_filepath) == 0:
                var = tk.StringVar()
                var.set(str(txt_filepath))
                label = tk.Label(self, textvariable=var)
                label.grid(row=3, column=1, padx=5, pady=5)

        def run_program():
            # placeholder for run program command
            if len(fpm_filepath) != 0 and len(losses_filepath) != 0 and len(startup_params_filepath) != 0 and len(
                    txt_filepath) != 0:
                tk.messagebox.showinfo(title="Running", message="ran successfully")
            else:
                tk.messagebox.showerror(title="Failed to Start Program", message="Missing File")

        # start of mainloop function (depreciated for class variable)
        # self.title('Tkinter Open File Dialog')
        # self.resizable(True, True)
        # self.geometry('700x200')
        # code to add widgets will go here
        # file selector for fpm file
        select_file_fpm = tk.Button(self, text="Select FPM File", command=select_file_fpm)
        # select_file_fpm.pack()
        select_file_fpm.grid(row=0, column=0, padx=5, pady=5)

        # file selector for losses.ini file
        select_file_losses = tk.Button(self, text="Select Losses File", command=select_file_losses)
        # select_file_losses.pack()
        select_file_losses.grid(row=1, column=0, padx=5, pady=5)

        # file selector for startup_params.ini file
        select_file_startup_params = tk.Button(self, text="Select Startup Paramaters File", command=select_file_startup_params)
        # select_file_params.pack()
        select_file_startup_params.grid(row=2, column=0, padx=5, pady=5)

        # file selector for txt file
        select_file_txt = tk.Button(self, text="Select Windographer Data File", command=select_file_txt)
        # select_file_txt.pack()
        select_file_txt.grid(row=3, column=0, padx=5, pady=5)

        # Check if all filepath vars are not empty, then add a run button
        run = tk.Button(self, text="Run Program!", command=run_program)
        run.grid(row=4, column=0, padx=5, pady=5)


        # TODO add text viewer and editor for this file

        # TODO add text viewer and editor for this file

        # TODO add text viewer for this file

        # root.mainloop()