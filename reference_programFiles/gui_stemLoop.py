import os
import sys
import pandas as pd
from tkinter import *
import tkinter as tk
import colorama
from tkinter import ttk
import subprocess
import gui_stemLoop_mut
from PIL import ImageTk, Image
from pandastable import Table
from tkinter import filedialog, messagebox, scrolledtext

class Page:
    def __init__(self,root,*args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)
        #frame_welcome.grid_forget()

        # Label for file upload
        #Label(root, text = "Uploaded file is :", width=20, height=2).grid(sticky = "w",row = 1, column = 1, padx =5)
        #Label(root, text = "Uploaded file is :", width=20, height=2).grid(sticky = "w",row = 2, column = 1, padx =5)

        # - row1
        Label(root, text="Genome Sequence File\n(Fasta/txt)", bg="lightgrey", pady=20,
              font=("Times", 15, "bold")).grid(sticky="w", row=1, column=0)

        self.gene_file_text = Text(root, width=18, height=2)  # Row1
        self.gene_file_text.grid(sticky="w", row=1, column=1, padx=5)

        self.gene_upload = Button(root, text="Upload", font=("Helvetica", 12), borderwidth="4",
                                  relief=RAISED,command=self.upload)
        self.gene_upload.grid(sticky = "e",row = 1, column = 2,padx =10, pady =2)

        self.calculate_button = Button(root, text="Execute", font=("Helvetica", 12), bd='3', state=tk.DISABLED, relief=RAISED)
        self.calculate_button.bind("<Button-1>", self.bind_button_status)
        self.calculate_button.grid(row=1, column=3, sticky="e") #split button declaration 2 lines to avoid NONType error while calling .config

        # -row2
        Label(root, text="Stem-loop Anotation File\n(Fasta/txt)", bg="lightgrey", pady=20, font=("Times", 15, "bold")).grid(sticky="w", row=2, column=0)

        self.stemLoop_file_text = Text(root, width=18, height=2)
        self.stemLoop_file_text.grid(sticky="w", row=2, column=1, padx=5)

        self.stemLoop_upload = Button(root, text="Upload", font=("Helvetica", 12), borderwidth="4", relief=RAISED,
                                      command=self.stemLoop_upload, state=tk.DISABLED)
        self.stemLoop_upload.grid(sticky="e", row=2, column=2, padx=10, pady=2)

        self.new = Button(root, text="Add File", font=("Helvetica", 12), borderwidth="4", relief=RAISED, command = self.add_file, state=tk.DISABLED)
        self.new.grid(row=2, column=3, sticky="e")

        # Blank rows - rows3,4
        Label(root, bg="lightgrey").grid(row=3, column=0)

        self.clear = Button(root, text="Clear", font=("Helvetica", 12), borderwidth="4", relief=RAISED, command = self.clear)
        self.clear.grid(row=3, column=3, sticky="e")

        Label(root, text = "Display Result", bg="lightgrey", font = ("Times", 15)).grid(row=4, column = 1, columnspan = 2)

        #separator - row5
        self.separator = ttk.Separator(root, orient='horizontal')
        self.separator.grid(row=5, sticky="ew", columnspan = 6)

        # -row6
        Label(root, bg="lightgrey").grid(row=6)

        # -row7
        self.atgc = Button(root, text="Consensus Sequence", font=("Helvetica", 12), borderwidth="4", relief=RAISED,
                             command=self.atgc, state=tk.DISABLED)
        self.atgc.grid(row=7, column=0,sticky = "w",padx = 20 )
        #self.mutation = Button(root, text="Observed\n Mutations", font=("Helvetica", 12), borderwidth="4", relief=RAISED,
                             #command=self.mutation_button_click).grid(row=7, column=1,sticky = "w")
        self.n_frequency = Button(root, text="Normalized Frequency", font=("Helvetica", 12), borderwidth="4", relief=RAISED,
                             command=self.n_frequency, state=tk.DISABLED)
        self.n_frequency.grid(row=7, column=1, columnspan = 2)
        self.titv_result_btn = Button(root, text="ti/tv in Stem & Loop", font=("Helvetica", 12), borderwidth="4", relief=RAISED,
                             command=self.titv_result, state=tk.DISABLED)
        self.titv_result_btn.grid(row=7, column=3,sticky = "e")

        # -row8
        Label(root, bg="lightgrey").grid(row=8)

        #status_bar - row9
        self.label_status = Label(root,bg="grey",fg = "white",height = 2, width = 1, bd = 1, anchor = "nw",  font = ("Helvetica", 12, "bold"),relief = FLAT)
        self.label_status.grid(row=9, columnspan =6,sticky = "ew")

        self.parent_path = os.getcwd()
        self.dir_sample = 'sample_inputFiles'
        if self.dir_sample not in os.listdir():
            os.mkdir(self.dir_sample)
        self.add_file()
        os.chdir(self.parent_path)


    # Upload file
    def is_fasta_format(self, file_path):
        with open(file_path, 'r') as file:
            line = file.readline()
            if line.startswith('>'):
                return True
            else:
                return False

    def upload(self):
        self.path_sample = os.path.join(self.parent_path, self.dir_sample)
        os.chdir(self.path_sample)
        #self.file_text.delete("1.0", tk.END)
        self.files = []
        filepaths = filedialog.askopenfilenames(initialdir=self.path_sample, title="Select A Fasta/text File",
                                                      filetypes=(("All Files", "*.*"),)) #("Text Files", "*.txt"),("All Files", "*.*")
        if len(filepaths) >=1:
            filepath = filepaths[-1]
            filename = os.path.basename(filepath)
            if self.is_fasta_format(filepath):
                self.files.append(filepath)
                self.gene_file_text.delete("1.0", "end")
                self.gene_file_text.insert(INSERT, filename)  # insert at the beginning of textbox

                # print(self.files)
            else:
                messagebox.showwarning("Invalid File",
                                       f"{filename} is not in FASTA format. Please upload files in FASTA format only.")

            self.stemLoop_upload.config(state=tk.NORMAL)
        else:
            pass

        self.gene_file_text.config(state=tk.DISABLED)


    def is_stem_loop(self, file_path):
        line_f_sl = file_path
        with open(line_f_sl, 'r') as fp:
            N1 = len(fp.readlines())  # count number of strains *2
            #print('Total lines:', N1)
        sf = open(line_f_sl, 'r')
        lines = sf.readlines()
        for l in range(N1):
            t_f = ""
            if l % 2 != 0:
                for char in lines[l]:
                    #print(char, lines[l])
                    if char == '.' or char == '(' or char == ')':
                        t_f = 'T'
                    else:
                        t_f = 'F'
                if t_f == 'T':
                    return True
                else:
                    return False

    def stemLoop_upload(self):
        #self.current_path = os.getcwd()
        stemLoop_filepaths = filedialog.askopenfilenames(initialdir= self.path_sample, title="Select A Text File",
                                                filetypes=(("Text Files", "*.txt"),))

        if len(stemLoop_filepaths) >= 1:
            stemLoop_filepath = stemLoop_filepaths[-1]
            stemLoop_filename = os.path.basename(stemLoop_filepath)
            if self.is_stem_loop(stemLoop_filepath):
                self.files.append(stemLoop_filepath)
                self.stemLoop_file_text.delete("1.0", "end")
                self.stemLoop_file_text.insert(tk.END, stemLoop_filename)

            # print(self.files)
            else:
                messagebox.showwarning("Invalid File",
                                       f"{stemLoop_filename} is not in Dot-Bracket format. Please upload stem-loop files in Dot-Bracket format only.")
        else:
            pass

        if self.files:
            self.calculate_button.config(command = self.on_calculate_button_click, state=tk.NORMAL)

        self.stemLoop_file_text.config(state=tk.DISABLED)

    #Binding Statusbar to button click event for calculate Button
    def bind_button_status(self,event):
        self.label_status.configure(text="Please Wait! Processing........ ")

    def on_calculate_button_click(self): # Current working Dir - Supplimentary
        #try:
        self.df_consensus, self.frequency_result, self.titv_result = gui_stemLoop_mut.process(self.files,self.parent_path)
        self.label_status.configure(text="You Can Visualize The Results Now...  ")

        if os.path.exists('Supplimentary_Files.csv'):
            self.new.config(state=tk.NORMAL)
            self.atgc.config(state=tk.NORMAL)
            self.n_frequency.config(state=tk.NORMAL)
            self.titv_result_btn.config(state=tk.NORMAL)
            self.stemLoop_upload.config(state=tk.DISABLED)
            self.gene_upload.config(state=tk.DISABLED)
        self.calculate_button.config(state=tk.DISABLED)

        os.chdir(self.parent_path)

        #except Exception as e:
        #    messagebox.showwarning("Error...",f"{e} ")
            #print("An error occurred:", e)

    def clear(self):
        self.gene_file_text.config(state=tk.NORMAL)
        self.stemLoop_file_text.config(state=tk.NORMAL)
        self.gene_file_text.delete("1.0", "end")
        self.stemLoop_file_text.delete("1.0", "end")
        self.gene_upload.config(state=tk.NORMAL)
        self.stemLoop_upload.config(state=tk.DISABLED)
        self.calculate_button.config(state=tk.DISABLED)

    def add_file(self):
        self.dir_suppl = 'supplimentary'
        if self.dir_suppl not in os.listdir():
            os.mkdir(self.dir_suppl)
        self.path_suppl = os.path.join(self.parent_path, self.dir_suppl)
        os.chdir(self.path_suppl)

        if os.path.exists('Supplimentary_Files.csv'):
            df_sup = pd.read_csv('Supplimentary_Files.csv', index_col=0)
            files = df_sup.shape[0]
            if messagebox.askyesno("Sequence Files Found",
                                   f"{files} Gene Sequences Already Present. \nDo you want to Add Seuence with Previous Ones?"):
                #messagebox.showinfo("Information", "Please upload a pair of file")
                self.gene_file_text.config(state=tk.NORMAL)
                self.stemLoop_file_text.config(state=tk.NORMAL)
                self.gene_file_text.delete("1.0", "end")
                self.stemLoop_file_text.delete("1.0", "end")
                self.gene_upload.config(state=tk.NORMAL)
                self.stemLoop_upload.config(state=tk.DISABLED)
                self.calculate_button.config(state=tk.DISABLED)
            else:
                pass
        else:
                self.gene_file_text.config(state=tk.NORMAL)
                self.stemLoop_file_text.config(state=tk.NORMAL)
                self.gene_file_text.delete("1.0", "end")
                self.stemLoop_file_text.delete("1.0", "end")
                self.gene_upload.config(state=tk.NORMAL)
                self.stemLoop_upload.config(state=tk.DISABLED)
                self.calculate_button.config(state=tk.DISABLED)
                '''
                try:
                    for file in os.listdir():
                        #print(f"inside add_file-- {file} removed")
                        os.remove(file)
                    self.gene_file_text.delete("1.0", "end")
                except Exception as e:
                    messagebox.showwarning("Error...", f"{e} ")
                '''
        os.chdir(self.parent_path)


    #atgc count
    def atgc(self):
        top_level = tk.Toplevel()
        top_level.title("Result Table for Consensus Sequence")
        top_level_width = 800
        top_level.geometry(f"{top_level_width}x400")

        frame = tk.Frame(top_level)
        frame.pack(fill='both', expand=True)

        table = Table(frame, dataframe=self.df_consensus, showtoolbar=True, showstatusbar=True)
        table.show()

    '''
    def mutation_button_click(self):
        # Display the result_df table using pandastable
        top_level = tk.Toplevel()
        top_level.title("Result Table for Mutations")
        top_level_width = 800
        top_level.geometry(f"{top_level_width}x400")

        frame = tk.Frame(top_level)
        frame.pack(fill='both', expand=True)

        table = Table(frame, dataframe=self.df_separatedMutation, showtoolbar=True, showstatusbar=True)
        table.show()
    '''

    def n_frequency(self):
        # Display the result_df table using pandastable
        top_level = tk.Toplevel()
        top_level.title("Result Table for Gene Given Sequence(s)")
        top_level_width = 800
        top_level.geometry(f"{top_level_width}x400")

        frame = tk.Frame(top_level)
        frame.pack(fill='both', expand=True)

        table = Table(frame, dataframe=self.frequency_result, showtoolbar=True, showstatusbar=True)
        table.show()

    def titv_result(self):
        # Display the result_df table using pandastable
        top_level = tk.Toplevel()
        top_level.title("Result Table for Gene Given Sequence(s)")
        top_level_width = 800
        top_level.geometry(f"{top_level_width}x400")
        frame = tk.Frame(top_level)
        frame.pack(fill='both', expand=True)
        table = Table(frame, dataframe=self.titv_result, showtoolbar=True, showstatusbar=True)
        table.show()

# Acknowledgement of Developer
class about(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super(about, self).__init__(*args, **kwargs)
        self.iconbitmap(resource_path('sl.ico'))
        self.title("About The Software")
        self.geometry("550x250")

        # inserting some text
        frame_about = Frame(self)
        frame_about.pack(anchor="center", fill=BOTH, expand=1)
        content = "'SLanalysis' is a software, \nwhich calculates the mutations and ti/tv ratio " \
                  "\nin both stem and loop regions obtained from \nthe 3' and 5' ends of " \
                  "\nSARS CoV2 genome sequence"
        self.l1 = Label(self, text = content, bg= "lightgrey",padx = 10, font = ("Times", 20, "bold"))
        self.l1.pack(anchor="n", expand=1, fill=BOTH)
        # Status bar about the Developers
        self.labelAbout = Label(self,
                      text = "Developed by Madhusmita Dash, NIT Arunachal Pradesh, as a part of Research Work "
                             "\nin collaboration with Dept of MBBT, Tezpur University").pack(expand=1, fill=BOTH)

#How to use Window
def open_how_to_use():
    how_to_use_text = """

# What is SLanalysis:
The objective of this software is to calculate ti/tv ratio in the secondary structure sequence file.

# How it works:
One or more than one pair of files gets uploaded to the software., i.e.
    1. Gene file, 
    2. Respective stem-loop anotation file, from NCBI
    
Upon execution, the result section activates and the software gives three outputs as display options where user can visualize ti/tv ratio as an output.

# How to use:
On running 'SLanalysis' software, a window opens-up within a minute.
It has two sections, consisting of several buttons and text-boxes.
In the first section, files can be uploaded, executed and cleared from the text (input) boxes.
In the second section, the results can be visualized by interacting with their respective buttons.
By default, the Result Section will be deactive. It will be activated with availability of the result files in the program's present working directory.
Both of the sections' work is as follows:
    First Section: 
    'Upload' Button (gene file) - 
        Uploads a gene file in fasta/text format.        
        Checks if the file is in fasta format, i.e. starts with '>strain-name' 
        if not in fasta-format, gives a message to give input a fasta file again
        
    'Upload' Button (stem-loop file) - 
        It gets activated only after uploading the gene-file.
        Checks if the file is in dot-bracket format, i.e. having '....(..)....' 
        if not having dot-bracket notation, gives a message to give input a dot-bracket file again
        
    'Execute' Button -
    The execute button calculates ti/tv ratio in below few steps. 
        1. Generates a csv file, named 'sequence_file.csv' from the given sequence file.
        2. calculates total number of A, T(U), G, C to find the consensus sequence for the given sequence file.
        3. Generates a csv file, named 'stem_loop.csv' from given stem-loop anotation file, downloaded from  NCBI.
        4. Appending 3 to 2, consensus.csv is generated.
        4. Mutations and Normalized Mutations are calculated as described in the paper.
        5. ti/tv ratio is calculated for stem and loop regions separately as from normalized mutations.
    Execution Button click activetes the Result Section        
                                                                                    
                                                                        |
                                                                        |
                            -------------------------------------------------------------------------
                            |                                                                                           |
                        New Button -                                                                      Add File Button -
        
            1. It can be used to calculate ti/tv for a single file.             1. This button adds the execution result of another pair of 
            2. It starts over from the beginning by clearing                    sequence file and stem-loop file.
            any existing results.                                                           \t2. It prompts to upload anoter pair of files.   
                                                                                                      \t\t\t3. After execution, the result will be added to the existing results.
    'Clear' Button -
        The button clears the text box entries so that the user can upload again.
        
    Second Section:
    All the buttons in this section are to visualize the results.
    These gets activated only after the 'Execution' Button Click.
    If more than one sequence files will be entered , by 'Add File' Button
        the output displayed in the result section will be the combination of all the indivisual results.
    
    'Consensus Sequence' Button -
        It displays total number of A,  T, G, C count along with the Consensus Sequence and the Stem_Loop anotation for the respective secondary structure.
        for more than one sequence file entry,
            the above information for different files will be appended followed by a line.
    
    'Normalised Frequency' Button -
        It displays the normalised frequencies for all 12 mutations in the secondary structures of stem(S) and loop(L).
    
    'ti/tv in Stem & Loop' Button -
        It displays the ti/tv ratio in stem(S) and loop(L) structures separately.
        
        *** To visualize the comparision in a graph for ti/tv_stem vs ti/tv_loop
            Select two diffrent columns from the 'Result Table for ti/tv' holding CTRL from key-board. 
                i.e. stem_ti/tv & loop_ti/tv
            From the side panel, select 'Plot Selected' icon showing a line graph as icon picture.
            A 'Plot Viewer' window will open-up.
            Click the 'Plot Type' drop down under 'Base Options' and 'general'
            Select 'bar' from the drop down list.
            Click on 'Plot current data'(first icon) or 'Refresh plot with current options'(second icon) under the visualization panel.
    
    'Exit' Menu - 
        On exit, all the result files and the secondary files will be deleted only after the user's confirmation.
        The user can copy the required file to a different location for any further use.
        
Supplimentary files:
All the supporting files required to verify the generated result, can be available in the Present Working Directory for the Program.
                    
    The supporting/Supplimentary files are-
    Supplimentary_Files.csv-
        This file keeps a track of how many sequence files and stem-loop files gets added to generate one result.
    
    sequence_file1.csv-
        This is the .csv format of entered fasta/text sequence file. 
        The number after the name of the file indicates the sequence of executed files. 
        i.e. for a single entry, it will show sequence_file1.csv, 
        and for two entries, it will show sequence_file1.csv for first entry & sequence_file2.csv for the second entry.
    
    stem_loop1.csv-
        This is the .csv format of given stem-loop anotation file.
        The number after the name of the file indicates the sequence of executed files. 
        i.e. for a single entry, it will show stem_loop1.csv, 
        and for two entries, it will show stem_loop1.csv for first entry & stem_loop2.csv for the second entry.

    Consensus1.csv-
        this is the file with total counts of A, T, G, C,
                              Consensus Sequence and
                              the stem-loop anotation
        The number after the name of the file indicates the sequence of executed files. 
        i.e. for a single entry, it will show Consensus1.csv, 
        and for two entries, it will show Consensus1.csv for first entry & Consensus2.csv for the second entry.
        
    nonZeroMutations1.csv-
        This file gives the information about the postion of mutation, nucleaotide before mutation and the nucleaotide after mutation.
        It doesn't contain any information about the postions where there is no mutations has been obsered.
    
    normalisedFrequency_File1.csv-
        It contains the Normalised Mutations for all 12 types of transitions(ti) and transversion(tv) type of mutations in stem and loop regions.
        
    NFcombined.csv-
        If there are more than one entries found, the result for indivisual entries are summed up to generate this supplimentary file.
        This will be displayed by the 'Normalized Frequency' Button under Second Section(Visualization Panel) of the tool. 
    


For any questions or issues, please refer to the paper or contact madhusmita.dash81@gmail.com/ madhusmita.phd@nitap.ac.in.
"""
    how_to_use_window = tk.Toplevel()
    how_to_use_window.title("How to Use")
    how_to_use_window.iconbitmap(resource_path('sl.ico'))

    text_widget = scrolledtext.ScrolledText(how_to_use_window, wrap=tk.WORD, font=("Helvetica", 12), width=100,
                                                height=20)
    text_widget.insert(tk.END, how_to_use_text)
    text_widget.config(state=tk.DISABLED)
    text_widget.pack(expand =1, fill = BOTH)

def new():
    os.chdir(parent_path)
    dir_suppl = 'supplimentary'
    if dir_suppl in os.listdir():
        path_suppl = os.path.join(parent_path, dir_suppl)
        os.chdir(path_suppl)
        if os.path.exists('Supplimentary_Files.csv'):
            if messagebox.askyesno("Want to Start-Over?","If YES, All Existing Supplimentary Files Will be Lost"):
                files = os.listdir()
                for file in files:
                    os.remove(file)
                os.chdir(parent_path)
                page = lambda: Page(sl_root)
                page()
            else:
                pass


    os.chdir(parent_path)



def on_closing():
    #print("in on_closing",parent_path)
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        os.chdir(parent_path)
        dir_suppl = 'supplimentary'
        path_suppl = os.path.join(parent_path, dir_suppl)
        os.chdir(path_suppl)
        #print("in on_closing", os.getcwd())
        if os.path.exists('Supplimentary_Files.csv'):
            if messagebox.askyesno("Remove Supplimentary Files?", "On YES,\nAll Supplimentary Files Will Be Deleted Permanately.\n "
                                                                 "Make Sure to Keep a Copy of Required File"):
                files = os.listdir()
                for file in files:
                    os.remove(file)
        sl_root.destroy()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
'''
def resource_path(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )
'''


if __name__ == "__main__":
    # root page
    sl_root = Tk()
    # set window background color
    sl_root.configure(bg='lightgray')
    # root icon
    sl_root.iconbitmap(resource_path('sl.ico'))
    # Window title
    sl_root.title('SLanalysis')
    # Window geometry
    width = sl_root.winfo_screenwidth()
    height = sl_root.winfo_screenheight()
    #sl_root.attributes('-fullscreen', True)
    # sl_root.geometry("%dx%d" % (width, height-90))
    # sl_root.resizable(False, False)
    sl_root.geometry("704x560")
    sl_root.maxsize(704,560)
    sl_root.minsize(704,560)

    # Inserting image into root through Label
        # opens image into image object
    img = Image.open(resource_path('sars cov2 image2.jpg'))
        # resize the image
    img_resize = img.resize((700, 200))
        # resized image as ImageTk object
    my_img = ImageTk.PhotoImage(img_resize)
        # bind image to label
    my_lbl = Label(height = 200, image=my_img)
        # grid label to root
    my_lbl.grid(row=0, column= 0, columnspan = 6, sticky = "ew")
    #my_lbl.pack(anchor = "center", expand = 1, fill = BOTH)

    #frame_welcome = Frame(sl_root, bg="lightgrey", borderwidth=10, relief=SUNKEN, padx=30, pady=15)
    #frame_welcome.grid(row =1,column = 0, rowspan = 100,columnspan=6,ipady= 20, sticky = "nw",ipadx = 23)
    #frame_welcome.pack(anchor = "center",expand = 1, fill = BOTH)
    #label_welcome = Label(frame_welcome, bg="lightgrey", fg="grey",
                               #text="Please Select any\n Desired Option \nfrom \nthe Menu",
                               #font="Lexend 30 bold italic").grid(ipadx=117, ipady=4, rowspan = 100,sticky = "nw")

    page = lambda: Page(sl_root)
    page()
    parent_path = os.getcwd()

    # Creating Menubar
    menubar = Menu(sl_root)

    menubar.add_command(label='New', command=new)
    menubar.add_command(label='How to Use', command=open_how_to_use)
    menubar.add_command(label='About', command=about)
    menubar.add_command(label='Exit', command= on_closing)
    # starting the menu
    sl_root.config(menu=menubar)

    #Window close event handled
    sl_root.protocol("WM_DELETE_WINDOW", on_closing)

    sl_root.mainloop()
