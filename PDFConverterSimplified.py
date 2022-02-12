from fpdf import FPDF
from PIL import Image

import os
import tkinter as tk
from pathlib import Path



#Model a PDF_object and call it... PoDoFo
class PoDoFo(object):
    def __init__(self, title, all_files):
        self.title = title #Name of the PDF once ready :)
        self.all_files = all_files #List of all image files to be inserted into PDF


#gets a list of ALL files inside a given directory
def get_list_of_files(ROOT):
    return [str(Path(element)) for element in [entry for entry in os.scandir(Path(ROOT)) if entry.is_file()]]

#gets a list of all files and sorts them by directory
def get_list_of_files_invasive(ROOT):####best so far
    l3 = []
    for x in [os.scandir(Path(y)) for y in [x.path for x in os.scandir(Path(ROOT)) if x.is_dir()]]:
        for y in x:
            l3.append(y.path)
    return l3


#Gets a list of all subfolders (of a given folder)
def folderseparator(ROOT):

    obj = os.scandir(Path(ROOT))

    list_of_dir = []
    print("Files and Directories in '% s':" % ROOT)
    for entry in obj:
        if entry.is_dir():
            list_of_dir.append(entry.path)

    return list_of_dir





def transform_this(Book):

    pdf = FPDF("p", "pt", (2055,1500))

    # imagelist is the list with all image filenames


    for image_file in Book.all_files:
        with Image.open(image_file) as im:
            pdf.add_page("p", (im.width, im.height))
            pdf.image(image_file, 0, 0, im.width, im.height)
            #print(f"{im.width} + {im.height}"

    #pdf.output(f"{Book.title}.pdf", dest="C:\\Users\\CHICO\\Desktop\\Akira pdf\\Complete")
    #pdf.output(f"C:\\Users\\CHICO\\Desktop\\Akira pdf\\Complete\\{Book.title}.pdf", "F") #Works as espected! ✔1
    pdf.output(f"D:\\BACKUP-D\\Downloads - Backup\\Provisional Manga Manager\\PDFConverterSimplified_Output\\{Book.title}.pdf", "F")  # Works as espected! ✔1
    #pdf.output(f"C:\\Users\\CHICO\\Desktop\\Akira pdf\\Completeeeee\\{Book.title}.pdf", "F")  # Works as espected! ✔2
    #"D:\\BACKUP-D\\Downloads - Backup\\Provisional Manga Manager\\PDFConverterSimplified_Output"

def OUTPUT_preview():
    if os.path.exists(PATH_entry.get()) is True and os.path.exists(PATH_entry.get()) != "":
        OUTPUT_box.insert(tk.END, f"{REBRAND_entry.get()}\n\n")
        for entry in get_list_of_files(PATH_entry.get()):
            OUTPUT_box.insert(tk.END, f"{entry}\n")
    else: OUTPUT_box.insert(tk.END, f"{REBRAND_entry.get()} & some invalid path!\n")



def OUTPUT_preview_invasive():
    if os.path.exists(PATH_entry.get()) is True and os.path.exists(PATH_entry.get()) != "":
        OUTPUT_box.insert(tk.END, f"{REBRAND_entry.get()}\n\n")
        for entry in get_list_of_files_invasive(PATH_entry.get()):
            OUTPUT_box.insert(tk.END, f"{entry}\n")
    else: OUTPUT_box.insert(tk.END, f"{REBRAND_entry.get()} & some invalid path!\n")









def load(): #Returns a PoDoFo Object. This function ensures constructor is filled-in with valid parameters only
    if os.path.exists(PATH_entry.get()) is True and os.path.exists(PATH_entry.get()) != "":
        return PoDoFo(REBRAND_entry.get(), get_list_of_files(PATH_entry.get()))

def load_auto_title(): #Same as above BUT uses the name of the folder to name the PDF file
    if os.path.exists(PATH_entry.get()) is True and os.path.exists(PATH_entry.get()) != "":
        p=Path(PATH_entry.get())
        return PoDoFo(p.name, get_list_of_files(PATH_entry.get()))

def load_invasive(): #same as above BUT uses all files within folders. Not only files in selected directory and uses Folder name to name PDF.
    if os.path.exists(PATH_entry.get()) is True and os.path.exists(PATH_entry.get()) != "":
        p = Path(PATH_entry.get())
        return PoDoFo(p.name, get_list_of_files_invasive(PATH_entry.get()))

def load2(path): #most important! Used to process multiple folders at once!
    p=Path(path)
    if os.path.exists(path) is True and os.path.exists(path) != "":
        return PoDoFo(p.name, get_list_of_files(path))




def commit():
    try:
        Libro = load()
    except AttributeError: OUTPUT_box.insert(tk.END, "Invalid parameter PoDoFo(ok, *wrong*)\n")

    try:
        transform_this(Libro)
        OUTPUT_box.insert(tk.END, f'***** Operation Successful *****\n')
    except AttributeError:
        OUTPUT_box.insert(tk.END, f'Invalid input! Path may be wrong\n')

def commit_auto():

    try:
        Libro = load_auto_title()
    except AttributeError:
        OUTPUT_box.insert(tk.END, "Invalid parameter PoDoFo(ok, *wrong*)\n")

    try:
        transform_this(Libro)
        OUTPUT_box.insert(tk.END, f'***** Operation Successful *****\n')
    except AttributeError:
        OUTPUT_box.insert(tk.END, f'Invalid input! Path may be wrong\n')

def commit_invasive():

    try:
        Libro = load_invasive()
    except AttributeError:
        OUTPUT_box.insert(tk.END, "Invalid parameter PoDoFo(ok, *wrong*)\n")

    try:
        transform_this(Libro)
        OUTPUT_box.insert(tk.END, f'***** Operation Successful *****\n')
    except AttributeError:
        OUTPUT_box.insert(tk.END, f'Invalid input! Path may be wrong\n')



def commit_separated():
    try:
        for entry in folderseparator(PATH_entry.get()):
            libro = load2(entry)
            transform_this(libro)

        OUTPUT_box.insert(tk.END, f'***** Operation Successful *****\n')
    except AttributeError: OUTPUT_box.insert(tk.END, f'Invalid input! Path may be wrong\n')








#"""

#F.R.O.N.T.E.N.D
mainwindow= tk.Tk() #Generic Window or root
mainwindow.title('Image to PDF 📸📜')

OUTPUT_box = tk.Text(mainwindow, height=20, width=60)

PATH_prompt = tk.Label(mainwindow, text= f'Turn all image files on THIS path into PDF!')
PATH_prompt.pack()

PATH_entry = tk.Entry(mainwindow)
PATH_entry.pack()

REBRAND_prompt = tk.Label(mainwindow, text= f'<BRAND> your PDF however you like!')
REBRAND_prompt.pack()

REBRAND_entry = tk.Entry(mainwindow)
REBRAND_entry.pack()



#-----Click them to display a preview-----
Preview = tk.Button(mainwindow, text='click to preview', command=OUTPUT_preview)
Preview.pack()

Preview_invasive = tk.Button(mainwindow, text='*PREVIEW INVASION*', command=OUTPUT_preview_invasive)
Preview_invasive.pack()



#-----Screen displaying all output-----
OUTPUT_box.pack(fil=tk.X)


#-----The end approaches-----
#REBRAND_commit = tk.Button(mainwindow, text='Commit <BRAND>', command = commit)
#REBRAND_commit.pack()

#REBRAND_commit_auto = tk.Button(mainwindow, text='*Use folder name to rename output file*', command = commit_auto)
#REBRAND_commit_auto.pack()

#REBRAND_commit_invasive = tk.Button(mainwindow, text='*COMMIT INVASION*', command = commit_invasive)
#REBRAND_commit_invasive.pack()

REBRAND_commit_separated = tk.Button(mainwindow, text='<Use individual folders on input path>', command = commit_separated)
REBRAND_commit_separated.pack()


#-----Keep the program alive-----
mainwindow.mainloop()

#"""

