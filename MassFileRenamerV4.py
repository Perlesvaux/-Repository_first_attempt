import os
import tkinter as tk
from fpdf import FPDF
from PIL import Image
from pathlib import Path
import re

"""
All files are given a single name
which changes only in numeration
appended at the end of each filename
"""
class rebranded_dir(object):
    def __init__(self, root: str):
        self.root = root
        self.replacement:str = ''

    @property
    def sd_all(self): #These are all sub-folders. Sorted: x1, x10, x11, x2, x20, x21, x3, x4, x5, x6, x7, x8, x9, xx, xy, xz, yy...
        main_folder = os.scandir(Path(self.root))
        print("Mainfolder → Files and Directories in '% s':" % self.root)
        return [entry.path for entry in main_folder if entry.is_dir()]

    @property
    def sd_numbered(self): #These are all numbered sub-folders. Sorterd x1, x10, x11, x2, x20, x21,x3, x4, x5, x6, x7, x8, x9
        return [entry for entry in self.sd_all if re.findall(r'\d+', Path(entry).stem)]

    @property
    def files_all(self):  #These are all files. Sorted by folder
        return [y.path for x in [os.scandir(Path(y)) for y in [x.path for x in os.scandir(Path(self.root)) if x.is_dir()]] for y in x]

    @property
    def files_numbered(self): #All files. Listed as WindowsPath(s) → .parent .stem .suffix
        return[x for x in self.files_all if re.findall(r'\d+', Path(x).stem)]

    @property
    def ok(self): #makes sure raw input is valid so program can continue!
        if os.path.exists(self.root) is True:
            if self.sd_preview(0): return True
        else: return False


    def sd_preview(self, option:int): #Choose whether you wanna keep just the number OR add a title next to it. 0 or 1
        if option == 0: # Numbers only: x1 → 001
            sorted_sub_folders = []
            for sub_folder in self.sd_numbered:
                temp_matches = re.findall(r'\d+', Path(sub_folder).stem)
                temp_list = [f"{'{:03d}'.format(int(entry))}" for entry in temp_matches]
                every_num = '-'.join(temp_list)
                sorted_sub_folders.append(f"{Path(sub_folder).parent}\\{every_num}")
            return sorted_sub_folders

        elif option == 1: #Titled: x1 → NewName001
            sorted_sub_folders = []
            for sub_folder in self.sd_numbered:
                temp_matches = re.findall(r'\d+', Path(sub_folder).stem)
                temp_list = [f"{'{:03d}'.format(int(entry))}" for entry in temp_matches]
                every_num = '-'.join(temp_list)
                sorted_sub_folders.append(f"{Path(sub_folder).parent}\\{self.replacement}{every_num}")  # {sub_folder.suffix}
            return sorted_sub_folders

    def sd_commit(self, option:int): #Confirms changes based on preview. 0 or 1
        numbered_folders = self.sd_numbered
        numbers_only = self.sd_preview(0)
        renamed = self.sd_preview(1)

        if option == 0: #i.e.: C:\Users\CHICO\Desktop\Manga 13 → C:\Users\CHICO\Desktop\013
            for x in range(len(self.sd_numbered)):
                os.rename(self.sd_numbered[x], numbers_only[x])

        elif option == 1: #i.e.: C:\Users\CHICO\Desktop\Manga 13 → C:\Users\CHICO\Desktop\Comic 013
            for x in range(len(numbered_folders)):
                os.rename(numbered_folders[x], renamed[x])



    def preview_files(self, option: int): #Replaces text with either '' or a 'new title'. 0 or 1
        sorted_pages = []
        if option == 0:  # List of ONLY reformatted NUMBERS x3 → 003
            for files in self.files_numbered:
                temp_matches = re.findall(r'\d+', Path(files).stem)
                temp_list = [f"{'{:03d}'.format(int(entry))}" for entry in temp_matches]
                every_num = '-'.join(temp_list)
                sorted_pages.append(f"{Path(files).parent}\\{every_num}{Path(files).suffix}")
            return sorted_pages


        elif option == 1:
            for files in self.files_numbered:
                temp_matches = re.findall(r'\d+', Path(files).stem)
                temp_list = [f"{'{:03d}'.format(int(entry))}" for entry in temp_matches]
                every_num = '-'.join(temp_list)
                sorted_pages.append(f"{Path(files).parent}\\{self.replacement}{every_num}{Path(files).suffix}")
            return sorted_pages



    def commit_files(self, option:int):
#        numbers_only = r'\d+'
#        numbered_filenames = []
#        for dir in self.sd_all:  # each sub-dir in path

#            for files in os.scandir(dir):  # each file in each subdir.
#                temp_path = Path(files)
#                temp_matches = re.findall(numbers_only, temp_path.stem)
#                if temp_matches:
#                    numbered_filenames.append(temp_path)
        numbered_files = self.files_numbered
        numbers_only = self.preview_files(0)
        renamed = self.preview_files(1)

        if option ==0:
            #corrected_filenames = self.preview_files(0)
            for x in range(len(numbers_only)):
                try:
                    print(f"{numbered_files[x]}↓\n{numbers_only[x]}")
                    os.rename(numbered_files[x], numbers_only[x])
                except FileExistsError: print ('repeated directory', numbers_only[x])#os.rename(numbered_filenames[x], f'zzz{corrected_filenames}')

        elif option ==1:
            #corrected_and_rebranded = self.preview_files(1)
            for x in range(len(renamed)):
                try:
                    print(f"{numbered_files[x]}↓\n{renamed[x]}")
                    os.rename(numbered_files[x], renamed[x])
                except FileExistsError: print('Repeated directory!', renamed[x])



def preview_SD():
    # Create an instance of a 'rebranded_dir' class.
    # Parse GUI input data into its constructor.
    # Parse GUI input data as a replacement name appended to each rebranded filename.

    reb_dir = rebranded_dir(PATH_entry.get()) #, REBRAND_entry.get())
    reb_dir.replacement = RSY_input.get()

    try:

        if reb_dir.ok:
            OUTPUT_box.insert(tk.END, f'Path exists & directories therein contain numbers:\n\n')

            for entry in reb_dir.sd_preview(R_selection.get()):
                OUTPUT_box.insert(tk.END, f'{entry}\n')
        else: OUTPUT_box.insert(tk.END, f'Path may not exist or there may be no numbers on any directory name\n')

    except:
        ValueError(OUTPUT_box.insert(tk.END, 'Revise: Path or methods: self.sd_all, self.sd_numbered, sd_preview '))

def commit_SD():
    try:
        reb_dir = rebranded_dir(PATH_entry.get())#, REBRAND_entry.get())
        reb_dir.replacement = RSY_input.get()
        OUTPUT_box.insert(tk.END, f'{reb_dir.ok}\n')


        if reb_dir.ok is True:
            reb_dir.sd_commit(R_selection.get())
            OUTPUT_box.insert(tk.END, f'****** Operation Successful ******\n')

    except: ValueError(OUTPUT_box.insert(tk.END, '(Path loaded Correctly! check methods: self.sd_all, self.sd_numbered, sd_preview'))



def  preview_f():
    reb_dir = rebranded_dir(PATH_entry.get())#, REBRAND_entry.get())
    reb_dir.replacement = SSY2_input.get()

    #try:
    if reb_dir.ok is True:
        for entry in reb_dir.preview_files(S_selection.get()):
            OUTPUT_box.insert(tk.END, f'{entry}\n')
    else:
        OUTPUT_box.insert(tk.END, f'Path may not exist or there may be no numbers on any directory name\n')
    #except:
    #    ValueError(OUTPUT_box.insert(tk.END, 'Revise: Path!\n\n'))

def commit_f():
    try:
        reb_dir = rebranded_dir(PATH_entry.get())#, REBRAND_entry.get())
        reb_dir.replacement = SSY2_input.get()
        OUTPUT_box.insert(tk.END, f'{reb_dir.ok}\n')

        if reb_dir.ok is True:
            reb_dir.commit_files(S_selection.get())
            OUTPUT_box.insert(tk.END, f'****** Operation Successful ******\n')

    except: ValueError(OUTPUT_box.insert(tk.END, '(Path loaded Correctly! Revise: self.sd_all, self.sd_numbered, sd_preview)'))



if __name__ == '__main__':
    #F.R.O.N.T.E.N.D

    #Setting up widgets!
    mainwindow= tk.Tk() #Generic Window or root

    PATH_prompt = tk.Label(mainwindow, text= f'THIS path contains all sub-directories to rename!')
    PATH_entry = tk.Entry(mainwindow)

    REBRAND_prompt = tk.Label(mainwindow, text= f'Remove THIS pattern from each sub-directory name')
    REBRAND_entry = tk.Entry(mainwindow)

    OUTPUT_box = tk.Text(mainwindow, height = 20, width = 60)

    Preview = tk.Button(mainwindow, text='Preview Sub-folders', command= preview_SD)
    PRINTED = tk.Label(mainwindow) #initializing this shit; blank space appears first


    REPLACE = tk.LabelFrame(mainwindow, text='Reformatting Sub-directories')
    R_selection = tk.IntVar(REPLACE)
    RS_no= tk.Radiobutton(REPLACE, text="I just need the numbers", variable=R_selection, value=0) #.pack() #, command=sel
    RS_yes = tk.Radiobutton(REPLACE, text="Add this title", variable=R_selection, value=1) # command= SETTER
    RSY_input = tk.Entry(REPLACE)

    REBRAND_commit = tk.Button(mainwindow, text='Commit Sub-folders!', command = commit_SD)


    SUBSTITUTE = tk.LabelFrame(mainwindow, text='Re-formatting files')
    S_selection = tk.IntVar(SUBSTITUTE)
    SS_no = tk.Radiobutton(SUBSTITUTE, text='keep numbers only', variable=S_selection, value=0)
    #SS_yes1 = tk.Radiobutton(SUBSTITUTE, text='Yes, keep numbers only', variable=S_selection, value=1)
    SS_yes2 = tk.Radiobutton(SUBSTITUTE, text='Yes, add title below to each file', variable=S_selection, value=1)
    SSY2_input = tk.Entry(SUBSTITUTE)

    Peek = tk.Button(mainwindow, text='Preview files', command = preview_f)
    SUBSTITUTE_commit = tk.Button(mainwindow, text='Commit files!', command= commit_f)





    #Positioning Widgets!
    PATH_prompt.pack()
    PATH_entry.pack()

    REPLACE.pack()
    RS_no.pack()
    RS_yes.pack()
    RSY_input.pack()

    Preview.pack()
    REBRAND_commit.pack()

    PRINTED.pack()

    SUBSTITUTE.pack()
    SS_no.pack()
    #SS_yes1.pack()
    SS_yes2.pack()
    SSY2_input.pack()

    Peek.pack()
    SUBSTITUTE_commit.pack()


    OUTPUT_box.pack(fill=tk.X)














    mainwindow.mainloop()

# return [f"{self.root}\\{'{:03d}'.format(int(leaf))}" for tree in
#           [re.findall(numbers_only, Path(entry).stem) for entry in self.sd_numbered if
#            re.findall(numbers_only, Path(entry).stem)] for leaf in tree]

# return [f"{self.root}\\{self.replacement}{'{:03d}'.format(int(leaf))}" for tree in
#           [re.findall(numbers_only, Path(entry).stem) for entry in self.sd_numbered if
#            re.findall(numbers_only, Path(entry).stem)] for leaf in tree]
