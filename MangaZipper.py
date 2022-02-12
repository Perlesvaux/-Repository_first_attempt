import tkinter as tk
import zipfile
import os


#B.A.C.K.E.N.D
#This app: zips each SUB-DIRECTORY individually.
#i.e.: creates a zipfile per SUB-DIRECTORY; all files contained thereat are copied therein.

#Here, we enter the DIRECTORY (that contains the SUB-DIRECTORIES we intend to zip).
#returns a list with all folders to zip
#i.e.: string input→ 'D:\BACKUP-D\Dororo'
#i.e.: list output→ ['D:\BACKUP-D\Dororo\cap01', 'D:\BACKUP-D\Dororo\cap02'...]

def get_sub_directories_from(Directory): #i.e.: 'D:\BACKUP-D\Dororo'
    ALL_SUB_DIRECTORIES = []  #List  of all folders to be individually zipped

    #crawling through directory & subdirectories
    for root, directories, files in os.walk(Directory):
        for directoryName in directories:
            #Join the two strings to get the full SUB-DIRECTORY path
            directoryPath = os.path.join(root, directoryName)
            ALL_SUB_DIRECTORIES.append(directoryPath)
    return ALL_SUB_DIRECTORIES

#Here, we intend to enter EACH SUB-DIRECTORY
#Returns a list with all FILES to be compressed
#i.e.: string input→  'D:\BACKUP-D\Dororo\cap03'
#i.e.: list output→ ['D:\BACKUP-D\Dororo\cap03\image.jpg', 'D:\BACKUP-D\Dororo\cap03\page00.jpg'...]

def get_all_file_paths(directory):

    FILE_PATHS = [] #List of all files found (i.e.: .jpg, .pdf, .mp3, etc.) and the paths thereto.

    #crawling through directory & subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            #Join the two strings to get the full FILE path
            filepath = os.path.join(root, filename)
            FILE_PATHS.append(filepath)

    return FILE_PATHS

#This one here makes the app run...
def main():
    Input = CompressThis.get()
    #Input = 'D:\BACKUP-D\Golden Boy' ### ← Enter desired folder name here
    Output = ReBranding.get()  ### ← This will be the name of each... chapter, let's say
    #Chapter = 0  # This fella here helps branding the output zip file with the
    Chapter= firstChapter.get()
    #if StartsOnD_flag.get() is True: Chapter = firstChapter.set(int(firstChapterEx_input.get()))
    #elif StartsOnD_flag.get() is False: Chapter = firstChapter.get()
    zeroes = how_many_zeroes.get()
    if how_many_zeroes.get() == "": zeroes = 3

    #this serves as a separator.
    #This list 'EACH_SUB_DIRECTORY' will help us isolate EACH SUB-DIRECTORY, see the FOR loop below
    EACH_SUB_DIRECTORY = []

    #This list 'sub_directories' stores the path to EACH SUB-DIRECTORY
    sub_directories = get_sub_directories_from(Input) ### ← Enter desired folder name here

    #For EACH SUB-DIRECTORY, we get the path to EACH FILE therein.
    #i.e.: There's an iteration per sub-directory.
    for x in sub_directories:
        EACH_SUB_DIRECTORY.append(get_all_file_paths(x))

    #printing the list of all files to be zipped

    for folder in EACH_SUB_DIRECTORY:
        print(folder)

    ###so far so good :)

    #----Writing files to a ZIP file

    #track = 0

    #Time to get the job done!
    for each_sub_directory in EACH_SUB_DIRECTORY: #scan through each 'get_all_file_paths'

        #Zipping each folder individually
        #with zipfile.ZipFile(f'{Output}{(formater(int(zeroes)).format(Chapter))}.cbz', 'w') as zip:
        with zipfile.ZipFile(f'D:\\BACKUP-D\\Downloads - Backup\\Provisional Manga Manager\\MangaZipper_Output\\{Output}{(formater(int(zeroes)).format(Chapter))}.cbz', 'w') as zip:
            for EachFile in each_sub_directory:
                #zip.write(EachFile, f'pag{track}{EachFile[-4:]}')
                zip.write(EachFile, f'{os.path.basename(EachFile)}')
                #track += 1
        Chapter += 1




def formater (inserteNumeroAqui):
    if how_many_zeroes.get() == "": return '{:03d}'
    else: return'{'+f':0{inserteNumeroAqui}d'+'}'

#F.R.O.N.T.E.N.D
root= tk.Tk() #Generic Window

# S1: Create canvas
canvas1 = tk.Canvas(root, width = 400, height = 500, cursor='heart', bd=2, bg='dark red')
canvas1.pack()

# S2: Add the entry box
# An entry box can be used to get the user's
# input. You can specify the position where
# the entry box would be placed on our Canvas
# (currently the position is set to 200,140)
#the display into which the 'entry' is inserted is in parentheses

Prompt2Compress = tk.Label(root, text= f'Paste here the path to compress!', bg='dark red', foreground='white')
canvas1.create_window(200, 50, window=Prompt2Compress)

CompressThis = tk.Entry(root)
canvas1.create_window(200, 75, window=CompressThis)

Prompt2Rebrand = tk.Label(root, text= f'Re-name it as you want!', bg='dark red', foreground='white')
canvas1.create_window(200, 100, window=Prompt2Rebrand)

ReBranding = tk.Entry(root)
canvas1.create_window(200, 125, window=ReBranding)

How_many_zeroes_prompt = tk.Label(root, text= f'How many digits? (defaults to 3 if left blank)')
canvas1.create_window(200, 160, window=How_many_zeroes_prompt)

how_many_zeroes = tk.Entry(root,  width=5)
how_many_zeroes.place(x=185, y=175)
#how_many_zeroes.insert(0, int(3))





###Cool Callback stuff that may come in handy later
#sv=tk.StringVar()
#def my_callback(var, indx, mode):
#    print (f"Traced variable {sv.get()}")
#sv.trace_add('write', my_callback)
#firstChapterEx_input = tk.Entry(root, textvariable=sv)






def SetChapter():

    try:
        #firstChapter.set(int(firstChapterEx.get()))
        firstChapter.set(int(firstChapterEx_input.get()))
    except ValueError:
        print('Invalid input. please try only numbers')
    #print(ReBranding.get())


def sel():
    zeroes = how_many_zeroes.get()
    if how_many_zeroes.get() == "": zeroes = 3
    selection = tk.Label(text=f"\"{ReBranding.get()}{(formater(int(zeroes)).format(firstChapter.get()))}\"", width=60, height=2, bg='light green')
    #selection.pack(fill=tk.X)
    canvas1.create_window(200, 360, window=selection)







TypesOfFirstChapter = tk.LabelFrame(root, text='Where does it begin from?')#.pack()
canvas1.create_window(200,250, window=TypesOfFirstChapter, height=90)


firstChapter = tk.IntVar(TypesOfFirstChapter)

StartsOn0 = tk.Radiobutton(TypesOfFirstChapter, text="Starts from Chapter 0", variable=firstChapter, value=0).pack() #, command=sel
StartsOn1 = tk.Radiobutton(TypesOfFirstChapter, text="Starts from Chapter 1", variable=firstChapter, value=1).pack() #, command=sel



firstChapterEx = tk.StringVar(TypesOfFirstChapter)
firstChapterEx_prompt = tk.Label(TypesOfFirstChapter, text="Start from:").place(x=0,y=50)

#firstChapterEx_input = tk.Entry(TypesOfFirstChapter,textvariable=firstChapterEx,  width=5).place(x=65,y=50)

firstChapterEx_input = tk.Entry(TypesOfFirstChapter,  width=5)
firstChapterEx_input.place(x=65,y=50)


firstChapterEx_set = tk.Button(TypesOfFirstChapter, text="Set", bg="light green", command=SetChapter).place(x=100,y=50)







Preview = tk.Button(text='Preview', command=sel)
canvas1.create_window(200,325,window=Preview)





# S3: Include a function



def run():

    #print(CompressThis.get())
    if os.path.exists(CompressThis.get()) is True:
        main()
        Resultado=tk.Label(root, text= f'Compression successful!', bg='green', foreground='white', width=60, height=3)
        canvas1.create_window(200,460, window=Resultado)
    else: print('This directory doesn\'t exist. Please try again')




'''
def run():
    main()
    Resultado=tk.Label(root, text= f'Compression successful!', bg='green', foreground='white')
    canvas1.create_window(200,460, window=Resultado)
    print('This directory doesn\'t exist. Please try again')
'''


button1 = tk.Button(text='Compress this path now!', command=run)
canvas1.create_window(200,425,window=button1)




root.mainloop()




