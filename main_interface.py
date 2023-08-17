import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os, pandas as pd
from configparser import ConfigParser
import main

# TODO add startup_function for reading the previously selected options, if there were any

working_dir = os.getcwd()

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)


    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Open run program",
                  command=lambda: master.switch_frame(RunProgram)).pack()
        tk.Button(self, text="Open page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()


class RunProgram(tk.Frame):
    def __init__(self, master):
        """
        Interace function, will include all the original stuff from the program but with a convienient interface for use and
        interaction
        :return:
        """
        tk.Frame.__init__(self, master)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).grid(row=5, column=0, padx=5, pady=5)

        # define our StringVar to get out of the function into our main analysis function
        fpm_filepath_var = tk.StringVar(master=self, value="")
        txt_filepath_var = tk.StringVar(master=self, value="")
        losses_filepath_var = tk.StringVar(master=self, value="")
        startup_params_filepath_var = tk.StringVar(master=self, value="")

        # if the vars were run before, use the previous values
        config_object = ConfigParser()
        config_object.read("config.ini")

        list_of_vars = [fpm_filepath_var, txt_filepath_var, losses_filepath_var, startup_params_filepath_var]
        count = 0
        for key in config_object["DEFAULTS"]:
            if len(config_object["DEFAULTS"][key]) != 0:
                list_of_vars[count].set(config_object["DEFAULTS"][key])
                count = count+1

        # todo adding saved values for the interface, not complete
        # def update_config(*args):
        #     fpm_data = fpm_filepath_var.get() # reading file selection
        #     txt_data = txt_filepath_var.get()
        #     losses_data = losses_filepath_var.get()
        #     startup_data = startup_params_filepath_var.get()
        #
        #     # each time the update_config command is fired, the config.txt will update
        #     config_object = ConfigParser
        #     config_object["DEFAULTS"] = {
        #         "fpm" : fpm_data,
        #         "txt" : txt_data,
        #         "losses" : losses_data,
        #         "startup_params" : startup_data
        #     }
        #     with open('config.ini', 'w') as conf:
        #         config_object.write(conf)


        def select_file_fpm():
            # this will update a global variable of fpm_filepath with a selected file
            # this is not the right way to do this, but I can't figure out a better way for now
            filetypes = (
                ('text files', '*.fpm'),
                ('All files', '*.*')
            )
            cwd = os.getcwd()
            fpm_filepath_var.set(fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.join(cwd, "inputs"),
                filetypes=filetypes))

            # add conditional label for if fpm_filepath has a value
            if not len(fpm_filepath_var.get()) == 0:
                label = tk.Label(self, textvariable=fpm_filepath_var)
                label.grid(row=0, column=1, padx=5, pady=5)

        def select_file_losses():
            # this will update a global variable of fpm_filepath with a selected file
            # this is not the right way to do this, but I can't figure out a better way for now
            filetypes = (
                ('text files', '*.ini'),
                ('All files', '*.*')
            )
            cwd = os.getcwd()
            losses_filepath_var.set(fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.join(cwd, "inputs"),
                filetypes=filetypes))

            # add conditional label for if fpm_filepath has a value
            if not len(losses_filepath_var.get()) == 0:
                label = tk.Label(self, textvariable=losses_filepath_var)
                label.grid(row=1, column=1, padx=5, pady=5)


        def select_file_startup_params():
            # this will update a global variable of fpm_filepath with a selected file
            # this is not the right way to do this, but I can't figure out a better way for now
            filetypes = (
                ('text files', '*.ini'),
                ('All files', '*.*')
            )
            cwd = os.getcwd()
            startup_params_filepath_var.set(fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.join(cwd, "inputs"),
                filetypes=filetypes))

            # add conditional label for if fpm_filepath has a value
            if not len(startup_params_filepath_var.get()) == 0:
                label = tk.Label(self, textvariable=startup_params_filepath_var)
                label.grid(row=2, column=1, padx=5, pady=5)


        def select_file_txt():
            # this will update a global variable of fpm_filepath with a selected file
            # this is not the right way to do this, but I can't figure out a better way for now
            filetypes = (
                ('text files', '*.txt'),
                ('All files', '*.*')
            )
            cwd = os.getcwd()
            txt_filepath_var.set(fd.askopenfilename(
                title='Open a file',
                initialdir=os.path.join(cwd, "inputs"),
                filetypes=filetypes))

            # add conditional label for if fpm_filepath has a value
            if not len(txt_filepath_var.get()) == 0:
                label = tk.Label(self, textvariable=txt_filepath_var)
                label.grid(row=3, column=1, padx=5, pady=5)

        def run_8760():
            # run 8760 command
            if len(fpm_filepath_var.get()) != 0 and len(losses_filepath_var.get()) != 0 and \
                    len(startup_params_filepath_var.get()) != 0 and len(txt_filepath_var.get()) != 0:
                tk.messagebox.showinfo(title="Running", message="running successfully")
                main.main(fpm_filepath_var.get(), losses_filepath_var.get(), startup_params_filepath_var.get(),
                          txt_filepath_var.get(), True, working_dir)
                tk.messagebox.showinfo(title="Program Complete", message="8760 run successfully")
            else:
                tk.messagebox.showerror(title="Failed to Start Program", message="Missing File")

        def run_pwts():
            # run pwts command
            if len(fpm_filepath_var.get()) != 0 and len(losses_filepath_var.get()) != 0 and \
                    len(startup_params_filepath_var.get()) != 0 and len(txt_filepath_var.get()) != 0:
                tk.messagebox.showinfo(title="Running", message="running successfully")
                main.main(fpm_filepath_var.get(), losses_filepath_var.get(), startup_params_filepath_var.get(),
                          txt_filepath_var.get(), False, working_dir)
                tk.messagebox.showinfo(title="Program Complete", message="PwTS run successfully")
            else:
                tk.messagebox.showerror(title="Failed to Start Program", message="Missing File")

        # file selector for fpm file
        select_file_fpm = tk.Button(self, text="Select FPM File", command=select_file_fpm)
        select_file_fpm.grid(row=0, column=0, padx=5, pady=5)

        # file selector for losses.ini file
        select_file_losses = tk.Button(self, text="Select Losses File", command=select_file_losses)
        select_file_losses.grid(row=1, column=0, padx=5, pady=5)

        # file selector for startup_params.ini file
        select_file_startup_params = tk.Button(self, text="Select Startup Paramaters File", command=select_file_startup_params)
        select_file_startup_params.grid(row=2, column=0, padx=5, pady=5)

        # file selector for txt file
        select_file_txt = tk.Button(self, text="Select Windographer Data File", command=select_file_txt)
        select_file_txt.grid(row=3, column=0, padx=5, pady=5)

        # run 8760 button
        run = tk.Button(self, text="Run 8760 Program!", command=run_8760)
        run.grid(row=4, column=0,columnspan = 2, sticky = tk.W+tk.E, padx=5, pady=5)

        # run pwts button
        run = tk.Button(self, text="Run PwTS Program!", command=run_pwts)
        run.grid(row=5, column=0, columnspan=2, sticky=tk.W + tk.E, padx=5, pady=5)

        # trace the vars set here for use in the next run
        # fpm_filepath_var.trace("w", update_config)


if __name__ == "__main__":
    app = SampleApp()
    app.title("8760/PwTS App")
    app.geometry("700x300")
    app.mainloop()