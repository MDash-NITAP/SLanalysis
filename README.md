# Steps to Run the Software

## Approach- 1: Download Zip
   1. Go to the link https://github.com/MDash-NITAP/SLanalysis.git
   2. Select Download Zip option from the drop-down menu for Code<>
   3. For downloading the "SLanalysis.exe" file:
      a. Select the exe file
      b. Download Raw from the top-right corner of the panel, giving descriptions of the file.
   4. Extract the Zip folder
   5. Replace the ( Zip folder -> application file )  with the downloaded Raw exe file.



## Approach- 2: Cloning Git Repository link
This repository contains an application file larger than 100MB. To download the Git repository containing large files, please make sure that Git-LFS was installed beforehand. Otherwise, the repository you cloned will only contain the shortcuts of the large files. Installing Git-LFS after the repository is cloned will not help. git pull and git fetch will not automatically replace the shortcuts to large files for you. If you have already cloned the repository, just delete the repository, make sure Git-LFS is correctly installed, and clone again. In this way, the large files will be cloned correctly.
 
   1. Download and install GitHub for the local system from https://git-scm.com/downloads
      (Ignore if Git already installed in local system.)
   3. Download and install “Git Large File Storage”  in local system from Git’s official website- https://git-lfs.com/
      (Ignore if Git-lfs already installed in local system.)
   4. Prepare a folder in the local storage for "git clone":
        1. Make a new folder
        2. Click on "Git Bash Here" from the right mouse Click Drop-down while being inside the folder
        3. Execute below commands one-by-one in the Git-Bash
           
           1. $ git init
           2. $ git lfs install
           3. $ git lfs env
           4. $ git lfs clone https://github.com/MDash-NITAP/SLanalysis.git
              
   5. Run the application after successful cloning       
   6. The application opens up within a minute, creating a new folder named "Supplimentary".

# SLanalysis
This software evaluates ti/tv values for both the stem and loop region of SARS-CoV-2 genome sequence, as described in the paper "Madhusmita Dash et al. 2023, Higher transition to transversion ratio in the secondary structure stem motifs than the loops in the SARS-CoV-2 un-translated regions"

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


    ### First Section:
    
    'Upload' Button (gene file) - 
        Uploads a gene file in fasta/text format.        
        Checks if the file is in fasta format, i.e. starts with '>strain-name' 
        if not in fasta-format, gives a message to give input a fasta file again
        
    'Upload' Button (stem-loop file) - 
        It gets activated only after uploading the gene-file.
        Checks if the file is in dot-bracket format, i.e. having '....(..)....' 
        if not having dot-bracket notation, gives a message to give input a dot-bracket file again
        
    'Execute' Button -
    The execute button calculates the ti/tv ratio in below few steps. 
        1. Generates a csv file named'sequence_file.csv' from the given sequence file.
        2. calculates the total number of A, T(U), G, C to find the consensus sequence for the given sequence file.
        3. Generates a csv file named'stem_loop.csv' from the given stem-loop annotation file, downloaded from NCBI.
        4. Appending 3 to 2, consensus.csv is generated.
        4. Mutations and Normalized Mutations are calculated as described in the paper.
        5. ti/tv ratio is calculated for stem and loop regions separately from normalized mutations.
    Execution Button-click activetes the Result Section        
                                                                                    
                                                                        |
                                                                        |
                            -------------------------------------------------------------------------
                            |                                                                       |
                        New Button -                                                           Add File Button -
        
            1. It can be used to calculate ti/tv for a single file.             1. This button adds the execution result of another pair 
            2. It starts over from the beginning by clearing                    of sequence file and stem-loop file.
            any existing results.                                               2. It prompts you to upload another pair of files.   
                                                                                3. After execution, the result will be added to the 
                                                                                existing results.
    'Clear' Button -
        The button clears the text box entries so that the user can upload again.


        
    ### Second Section:
    
    All the buttons in this section are to visualize the results.
    These gets activated only after the 'Execution' Button Click.
    If more than one sequence files will be entered , by 'Add File' Button
    The output displayed in the result section will be the combination of all the indivisual results.
    
    'Consensus Sequence' Button -
        It displays total number of A,  T, G, C count along with the Consensus Sequence and the Stem_Loop anotation for the respective           secondary structure.
        for more than one sequence file entry, the above information for different files will be appended, followed by a line.
    
    'Normalised Frequency' Button -
        It displays the normalised frequencies for all 12 mutations in the secondary structures of stem(S) and loop(L).
    
    'ti/tv in Stem & Loop' Button -
        It displays the ti/tv ratio in stem(S) and loop(L) structures separately.
        
        *** To visualize the comparison in a graph for ti/tv_stem vs ti/tv_loop
            Select two different columns from the 'Result Table for ti/tv' holding CTRL from the keyboard.
                i.e. stem_ti/tv & loop_ti/tv
            From the side panel, select the 'Plot Selected' icon, which shows a line graph as icon picture.
            A 'Plot Viewer' window will open-up.
            Click the 'Plot Type' drop-down under 'Base Options' and 'general'
            Select 'bar' from the drop-down list.
            Click on 'Plot current data(first icon) or 'Refresh plot with current options (second icon) under the visualization panel.
    
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
        It contains the Normalised Mutations for all 12 types of transitions(ti) and transversion(tv) type of mutations in stem and loop         regions.
        
    NFcombined.csv-
        If there are more than one entries found, the result for indivisual entries are summed up to generate this supplimentary file.
        This will be displayed by the 'Normalized Frequency' Button under Second Section(Visualization Panel) of the tool. 
    


For any questions or issues, please refer to the paper or contact madhusmita.dash81@gmail.com/ madhusmita.phd@nitap.ac.in.
