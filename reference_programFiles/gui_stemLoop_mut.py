import pandas as pd
import os
import csv
import math
from tkinter import messagebox
#from gui_stemLoop import Page
#gui = Page

#Finding the Consensus Sequence
def consensus(data_gene,supplimentaryFiles_row):
    # Reading From Input File
    df = data_gene
    df = df.drop('sl', axis = 1)
    df.fillna("_", inplace=True)
    data = df.iloc[:, 0:]  ##  or data=df.loc[:,'1':]

    lA = ['A']
    lT = ['T']
    lG = ['G']
    lC = ['C']

    x = data.shape[1]
    #print(x)
    for i in range(1, x):
        lA.append((data.iloc[:, i]).str.count('A').sum())
        lT.append((data.iloc[:, i]).str.count('T').sum())
        lG.append((data.iloc[:, i]).str.count('G').sum())
        lC.append((data.iloc[:, i]).str.count('C').sum())

    l = ['Total']
    for i in range(1, x):
        l.append(i)

    # Writting to csv WITH  csv Module
    atgc_file = 'Consensus' + str(supplimentaryFiles_row + 1) + '.csv'
    with open(atgc_file, "w") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(l)
        wr.writerow(lA)
        wr.writerow(lT)
        wr.writerow(lG)
        wr.writerow(lC)
    #print(f"\nTotal number of A, T, G, C added to File:{atgc_file}")

    # Reference Sequence
    lstR = ['Consensus Sequence']
    df = pd.read_csv(atgc_file, index_col=0)
    df = df.reset_index()

    for i in range(1, df.shape[1]):
        # print(df.iloc[:,i].argmax())
        series = pd.Series(df.iloc[:, i])
        s = series.argmax()  # .argmax returns the row number(indices) of the largest value in a Series
        # t=s.nlargest(1)
        # print(s)
        t = df.iloc[s, 0]
        # print(t)
        lstR.append(t)
    # print(lstR)
    with open(atgc_file, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(lstR)
    #print("The Consensus Sequence Generated As:\n")

    df_consensus = pd.read_csv(atgc_file, index_col=0)
    #print("COnsensus Sequence File- \n", df_consensus)
    return df_consensus                                                       #-----------------End of Consensus Functions

#Function for calculationg nonZeroMutations in stem and loop
def mutations_stemLoop(data_mutations_repeatedRows, data_sl,data_consensus,supplimentaryFiles_row):
    data_mutation = data_mutations_repeatedRows
    data_mutation = data_mutation.reset_index(drop = True)
    #print(f"data_mutations_repeatedRows \n{data_mutation}")

    data_slncbi = data_sl.set_index(0)
    #data_slncbi = data_slncbi.reset_index()
   #print(f"stem_loop ncbi\n {data_slncbi}")

    data_atgc = data_consensus
    #print(f"consensus data\n {data_atgc}")
    data_atgc = pd.DataFrame(data_atgc.iloc[-1, :])
    data_atgc = data_atgc.transpose()  # transpose dataframe
    data_atgc = data_atgc.reset_index()
    data_atgc.rename(columns={'index': 0}, inplace=True)
    data_atgc = data_atgc.set_index(0)
    #print(data_atgc)

    data_mutation = data_mutation.loc[:, ['Position', 'Source', 'Target']]
    #drop data with zero mutations
    data_mutation = data_mutation.drop(data_mutation[data_mutation['Position'] == 0].index)
    data_mutation = data_mutation.reset_index(drop=True)
    #data_mutation.to_csv(r'D:\self learning\programs\titv_stemloopDupl1.csv', index=False)

    # Removing repeated mutations at same position
    data_mutation = data_mutation.drop_duplicates()
    data_mutation = data_mutation.reset_index(drop=True)

    data_atgc.columns = data_slncbi.columns  # Columns were of different dataTypes
    data_ncbi_consensus = data_slncbi.append(data_atgc)
    #print("data_ncbi_consensus\n",data_ncbi_consensus.head())
    del data_slncbi,data_atgc       # deletes Dataframe

    col_pos = data_mutation.shape[1]
    data_mutation.insert(col_pos, 'Stem/loop', 0)

    for i in range(data_mutation.shape[0]):
        pos = math.floor(data_mutation.loc[i, 'Position'])
        if data_ncbi_consensus.at['Consensus Sequence', pos].upper() == data_mutation.at[i, 'Source']:
            S_L = data_ncbi_consensus.loc['SL_Structure', pos]
            if S_L == '.':
                data_mutation.loc[i, 'Stem/loop'] = 'L'
            elif S_L == '(' or S_L == ')':
                data_mutation.loc[i, 'Stem/loop'] = 'S'
            else:
                data_mutation.loc[i, 'Stem/loop'] = S_L
    #    else:
    #        data_mutation.loc[i,'Stem/loop'] = 'Source No Match'

    df_nonZeroMutation_stemloop = 'nonZeroMutations' + str(supplimentaryFiles_row + 1) + '.csv'
    data_mutation.to_csv(df_nonZeroMutation_stemloop, index=False)
    #print(data_mutation.shape)

    # Separating for stem and loop
    #nonZeroMutation_stemFile = 'stem_SupplimentaryFile' + str(supplimentaryFiles_row + 1) + '.csv'
    data_mutation_stem = data_mutation.drop(data_mutation[data_mutation['Stem/loop'] == 'L'].index)
    data_mutation_stem = data_mutation_stem.reset_index(drop = True)
    #data_mutation_stem.to_csv(nonZeroMutation_stemFile, index=False)

    #nonZeroMutation_loopFile = 'loop_SupplimentaryFile' + str(supplimentaryFiles_row + 1) + '.csv'
    data_mutation_loop = data_mutation.drop(data_mutation[data_mutation['Stem/loop'] == 'S'].index)
    data_mutation_loop = data_mutation_loop.reset_index(drop=True)
    #data_mutation_loop.to_csv(nonZeroMutation_loopFile, index=False)


                                                            #----------------------------------End of Separating stem loop files
#DataFrames required--- stem (data_mutation_stem)
                        #loop (data_mutation_loop)
                        #atgc (data_atgc) and stem_loop_ncbi (data_slncbi)----  (data_ncbi_consensus)

# For Loop-structure
    # combination Source & Target
    df_mutation_loop = data_mutation_loop
    df_mutation_loop['mutation'] = df_mutation_loop['Source'] + '->' + df_mutation_loop['Target']
    #print("df_mutation_loop\n",df_mutation_loop)

    #Duplicate Position Count
    duplicate_position = df_mutation_loop['Position'].value_counts() #Series
    #print( duplicate_position.index)
    duplicate_position = duplicate_position.sort_index()
    duplicate_positions = pd.DataFrame(duplicate_position)
    duplicate_positions = duplicate_positions.reset_index()
    duplicate_positions.columns = ['Duplicate_Position', 'Counts']
    duplicate_positions = duplicate_positions[duplicate_positions['Counts'] > 1]
    duplicate_positions = duplicate_positions.reset_index(drop = True)
    #print(duplicate_positions)

    # A, T, G,C counts in loop
    data_ncbi_consensus_T = data_ncbi_consensus.transpose()
    atgc_count_loop = data_ncbi_consensus_T[data_ncbi_consensus_T['SL_Structure'] == '.']
    atgc_count_loop = atgc_count_loop['Consensus Sequence'].value_counts()    #Series
    #print(atgc_count_loop)

    # A, T, G, C Count Adjustment --
    # 1. Search in duplivate_position, count>1  ->  Fetch the position number
    # 2. Match the position number in df_mutation_loop  ->  Fetch Source character
    # 3. Change the character value in atgc_count to 1 less than Duplicate_Position,counts
    for i in range(duplicate_positions.shape[0]):
        d_pos = duplicate_positions.loc[i,'Duplicate_Position']
        count = duplicate_positions.loc[i, 'Counts']
        df_mutation_loop_index = df_mutation_loop[df_mutation_loop['Position'] == d_pos].index
        df_mutation_loop_index = df_mutation_loop_index[0]
        source_base = df_mutation_loop.at[df_mutation_loop_index,'Source']
        atgc_count_loop[source_base] = atgc_count_loop[source_base] + (count-1)
        #print(atgc_count_loop)

    # Count of 12 different mutations separately
    mutation_count = df_mutation_loop['mutation'].value_counts()
    mut_lst = ['A->C', 'A->T', 'A->G', 'C->T', 'C->G', 'C->A', 'T->G', 'T->A', 'T->C', 'G->A', 'G->C', 'G->T']
    for i in mut_lst:
        if i not in mutation_count.index:
            mutation_count[i] = 0
    mutation_count = mutation_count.sort_index()
    mutation_counts = pd.DataFrame(mutation_count)
    mutation_counts = mutation_counts.reset_index()
    mutation_counts.columns = ['Mutations_L', 'Counts_L']

    mutation_counts.insert(mutation_counts.shape[1], "Normalized Frequency_L", 0)
    mutation_counts.insert(mutation_counts.shape[1], "Transition_L", 0)
    mutation_counts.insert(2, "Reference Neucleotide_L", 0)
    mutation_counts.insert(3, "Total Count of Ref Neucleotide_L", 0)

    for i in range(mutation_counts.shape[0]):
        if mutation_counts.loc[i, 'Mutations_L'][0] == 'A':
            if mutation_counts.loc[i, 'Mutations_L'][3] == 'G':
                mutation_counts.loc[i, 'Transition_L'] = 1
            else:
                mutation_counts.loc[i, 'Transition_L'] = 0
            mutation_counts.loc[i,'Reference Neucleotide_L'] = 'A'
            mutation_counts.loc[i,'Total Count of Ref Neucleotide_L'] = atgc_count_loop['A']
            mutation_counts.loc[i, 'Normalized Frequency_L'] = round(mutation_counts.loc[i, 'Counts_L'] / atgc_count_loop['A'],3)
        elif mutation_counts.loc[i, 'Mutations_L'][0] == 'T':
            if mutation_counts.loc[i, 'Mutations_L'][3] == 'C':
                mutation_counts.loc[i, 'Transition_L'] = 1
            else:
                mutation_counts.loc[i, 'Transition_L'] = 0
            mutation_counts.loc[i, 'Reference Neucleotide_L'] = 'T'
            mutation_counts.loc[i, 'Total Count of Ref Neucleotide_L'] = atgc_count_loop['T']
            mutation_counts.loc[i, 'Normalized Frequency_L'] = round(mutation_counts.loc[i, 'Counts_L'] / atgc_count_loop['T'],3)
        elif mutation_counts.loc[i, 'Mutations_L'][0] == 'G':
            if mutation_counts.loc[i, 'Mutations_L'][3] == 'A':
                mutation_counts.loc[i, 'Transition_L'] = 1
            else:
                mutation_counts.loc[i, 'Transition_L'] = 0
            mutation_counts.loc[i, 'Reference Neucleotide_L'] = 'G'
            mutation_counts.loc[i, 'Total Count of Ref Neucleotide_L'] = atgc_count_loop['G']
            mutation_counts.loc[i, 'Normalized Frequency_L'] = round(mutation_counts.loc[i, 'Counts_L'] / atgc_count_loop['G'],3)
        elif mutation_counts.loc[i, 'Mutations_L'][0] == 'C':
            if mutation_counts.loc[i, 'Mutations_L'][3] == 'T':
                mutation_counts.loc[i, 'Transition_L'] = 1
            else:
                mutation_counts.loc[i, 'Transition_L'] = 0
            mutation_counts.loc[i, 'Reference Neucleotide_L'] = 'C'
            mutation_counts.loc[i, 'Total Count of Ref Neucleotide_L'] = atgc_count_loop['C']
            mutation_counts.loc[i, 'Normalized Frequency_L'] = round(mutation_counts.loc[i, 'Counts_L'] / atgc_count_loop['C'],3)
    mutation_counts_loop = mutation_counts
    #print(mutation_counts_loop)

    mut_ti_loop = mutation_counts.drop(mutation_counts[mutation_counts['Transition_L'] == 0].index)
    ti_loop = mut_ti_loop['Normalized Frequency_L'].sum()
    #print(mut_ti_loop)

# For Stem
    # combination Source & Target
    df_mutation_stem = data_mutation_stem
    df_mutation_stem['mutation'] = df_mutation_stem['Source'] + '->' + df_mutation_stem['Target']
    # print("df_mutation_stem\n",df_mutation_stem)

    # Duplicate Position Count
    duplicate_position = df_mutation_stem['Position'].value_counts()  # Series
    # print( duplicate_position.index)
    duplicate_position = duplicate_position.sort_index()
    duplicate_positions = pd.DataFrame(duplicate_position)
    duplicate_positions = duplicate_positions.reset_index()
    duplicate_positions.columns = ['Duplicate_Position', 'Counts']
    duplicate_positions = duplicate_positions[duplicate_positions['Counts'] > 1]
    duplicate_positions = duplicate_positions.reset_index(drop=True)
    # print(duplicate_positions)

    # A, T, G,C counts in stem
    data_ncbi_consensus_T = data_ncbi_consensus.transpose()
    atgc_count_stem = data_ncbi_consensus_T.drop(data_ncbi_consensus_T[data_ncbi_consensus_T['SL_Structure'] == '.'].index)
    #atgc_count_stem = data_ncbi_consensus_T[data_ncbi_consensus_T['SL_Structure'] == '.']
    atgc_count_stem = atgc_count_stem['Consensus Sequence'].value_counts()  # Series
    # print(atgc_count_stem)

    # A, T, G, C Count Adjustment --
    # 1. Search in duplivate_position, count>1  ->  Fetch the position number
    # 2. Match the position number in df_mutation_loop  ->  Fetch Source character
    # 3. Change the character value in atgc_count to 1 less than Duplicate_Position,counts
    for i in range(duplicate_positions.shape[0]):
        d_pos = duplicate_positions.loc[i, 'Duplicate_Position']
        count = duplicate_positions.loc[i, 'Counts']
        df_mutation_stem_index = df_mutation_stem[df_mutation_stem['Position'] == d_pos].index
        df_mutation_stem_index = df_mutation_stem_index[0]
        source_base = df_mutation_stem.at[df_mutation_stem_index, 'Source']
        atgc_count_stem[source_base] = atgc_count_stem[source_base] + (count - 1)
        #print(atgc_count_stem)

    # Count of 12 different mutations separately
    mutation_count = df_mutation_stem['mutation'].value_counts()
    mut_lst = ['A->C', 'A->T', 'A->G', 'C->T', 'C->G', 'C->A', 'T->G', 'T->A', 'T->C', 'G->A', 'G->C', 'G->T']
    for i in mut_lst:
        if i not in mutation_count.index:
            mutation_count[i] = 0
    mutation_count = mutation_count.sort_index()
    mutation_counts = pd.DataFrame(mutation_count)
    mutation_counts = mutation_counts.reset_index()
    mutation_counts.columns = ['Mutations_S', 'Counts_S']

    #titv_counts_stemFile = 'titvCountsStem_SupplimentaryFile' + str(supplimentaryFiles_row + 1) + '.csv'
    #mutation_counts.to_csv(titv_counts_stemFile, index=False)

    mutation_counts.insert(mutation_counts.shape[1], "Normalized Frequency_S", 0)
    mutation_counts.insert(mutation_counts.shape[1], "Transition_S", 0)
    mutation_counts.insert(2, "Reference Neucleotide_S", 0)
    mutation_counts.insert(3, "Total Count of Ref Neucleotide_S", 0)

    for i in range(mutation_counts.shape[0]):
        if mutation_counts.loc[i, 'Mutations_S'][0] == 'A':
            if mutation_counts.loc[i, 'Mutations_S'][3] == 'G':
                mutation_counts.loc[i, 'Transition_S'] = 1
            else:
                mutation_counts.loc[i, 'Transition_S'] = 0
            mutation_counts.loc[i, 'Reference Neucleotide_S'] = 'A'
            mutation_counts.loc[i, 'Total Count of Ref Neucleotide_S'] = atgc_count_stem['A']
            mutation_counts.loc[i, 'Normalized Frequency_S'] = round(mutation_counts.loc[i, 'Counts_S'] / atgc_count_stem['A'],3)
        elif mutation_counts.loc[i, 'Mutations_S'][0] == 'T':
            if mutation_counts.loc[i, 'Mutations_S'][3] == 'C':
                mutation_counts.loc[i, 'Transition_S'] = 1
            else:
                mutation_counts.loc[i, 'Transition_S'] = 0
            mutation_counts.loc[i, 'Reference Neucleotide_S'] = 'T'
            mutation_counts.loc[i, 'Total Count of Ref Neucleotide_S'] = atgc_count_stem['T']
            mutation_counts.loc[i, 'Normalized Frequency_S'] = round(mutation_counts.loc[i, 'Counts_S'] / atgc_count_stem['T'],3)
        elif mutation_counts.loc[i, 'Mutations_S'][0] == 'G':
            if mutation_counts.loc[i, 'Mutations_S'][3] == 'A':
                mutation_counts.loc[i, 'Transition_S'] = 1
            else:
                mutation_counts.loc[i, 'Transition_S'] = 0
            mutation_counts.loc[i, 'Reference Neucleotide_S'] = 'G'
            mutation_counts.loc[i, 'Total Count of Ref Neucleotide_S'] = atgc_count_stem['G']
            mutation_counts.loc[i, 'Normalized Frequency_S'] = round(mutation_counts.loc[i, 'Counts_S'] / atgc_count_stem['G'],3)
        elif mutation_counts.loc[i, 'Mutations_S'][0] == 'C':
            if mutation_counts.loc[i, 'Mutations_S'][3] == 'T':
                mutation_counts.loc[i, 'Transition_S'] = 1
            else:
                mutation_counts.loc[i, 'Transition_S'] = 0
            mutation_counts.loc[i, 'Reference Neucleotide_S'] = 'C'
            mutation_counts.loc[i, 'Total Count of Ref Neucleotide_S'] = atgc_count_stem['C']
            mutation_counts.loc[i, 'Normalized Frequency_S'] = round(mutation_counts.loc[i, 'Counts_S'] / atgc_count_stem['C'],3)
    mutation_counts_stem = mutation_counts
    #print(mutation_counts_stem)

    #Joining two stem and loop dataFrames
    mut_analysis_sl_titv = mutation_counts_stem.join(mutation_counts_loop)
    mut_analysis_sl_titv1 = mut_analysis_sl_titv.loc[:,['Transition_S','Transition_L','Mutations_S','Mutations_L','Counts_S',
                                                 'Counts_L','Reference Neucleotide_S','Reference Neucleotide_L',
                                                 'Total Count of Ref Neucleotide_S',
                                                 'Total Count of Ref Neucleotide_L','Normalized Frequency_S','Normalized Frequency_L']]
    mut_analysis_sl_titv1 = mut_analysis_sl_titv1.drop(['Transition_L','Mutations_L','Reference Neucleotide_L'], axis =1)
    mut_analysis_sl_titv1.rename(columns = {'Transition_S':'ti','Mutations_S':'Mutations',
                                            'Reference Neucleotide_S':'Neucleotide',
                                            'Total Count of Ref Neucleotide_S':'Count in S',
                                            'Total Count of Ref Neucleotide_L':'Count in L',
                                            'Normalized Frequency_S':'NFrequency_S',
                                            'Normalized Frequency_L':'NFrequency_L'}, inplace = True)
    #print(mut_analysis_sl_titv1.head().to_string())
    df_result = mut_analysis_sl_titv1
    return df_result


def process(gene_names,path):
    parent_path = path
    #print("gui_stemLoop_mut",parent_path)
    os.chdir(parent_path)
    dir_suppl = 'supplimentary'
    #print(dir_suppl not in os.listdir())
    if dir_suppl not in os.listdir():
        os.mkdir(dir_suppl)
    path_suppl = os.path.join(parent_path, dir_suppl)  # joins two strings as a path
    os.chdir(path_suppl)  # move into another directory
    #print("gui_stemLoop_mut-- ", os.getcwd())
    if os.path.exists('Supplimentary_Files.csv'):
        df_supplimentaryFiles = pd.read_csv('Supplimentary_Files.csv')
        df_supplimentaryFiles_row = df_supplimentaryFiles.shape[0]

    else:
        df_supplimentaryFiles = pd.DataFrame(columns=['Gene_file', 'SL_file'])#,'consensus_file','mutation_file','titv_file'])
        df_supplimentaryFiles_row = df_supplimentaryFiles.shape[0]

    #    if extn == "fasta":
    #    os.rename(fil_, file + '.txt')

    #Create CSV from Fasta/Text gene file
    ln = 0
    CCount = 0
    nColumns = 0  # Counts the Number of Coulumns
    line_f = gene_names[0]
    line_f = line_f.strip()
    fil_ = os.path.basename(line_f)
    file = os.path.splitext(fil_)[0]
    extn = os.path.splitext(fil_)[1]
    sf = open(line_f, 'r')
    df = open('transit.txt', 'w')
    for i in sf:
        for li in i:
            if (li == '>'):
                ln += 1
                if (CCount > nColumns):
                    nColumns = CCount
                CCount = 0
                df.write("\n")
                df.write(str(ln) + ',')
                s = i.replace(',', '-')
                # t=s.replace(',','-')
                df.write(s[1:].rstrip('\n'))
                break
            elif (li == "\n"):
                df.write(li.rstrip('\n'))
            else:
                CCount += 1
                lee = li.upper()
                df.write(',' + lee.rstrip('\n'))

            # print("Number of columns",CCount)
        if (CCount > nColumns):
            nColumns = CCount
        # print("Col", nColumns)
        #print("     .")
    #print("Sequence alignment done  !!!.....")
    df.close()
    df = open('transit.txt', 'r')
    nf = open('transit1.txt', 'w')  # ####

    #print("Printing Column numbers ****")
    nf.write("sl,strain name")
    for j in range(1, nColumns + 1):
        nf.write(',' + str(j).rstrip('\n'))
        #print("     *")

    for line in df:
        nf.write(line)
    nf.close()
    df.close()
    sf.close()

    # To csv(using pandas module)
    gene_file = 'sequence_file'+ str(df_supplimentaryFiles_row+1) + '.csv'
    df_gene = pd.read_csv('transit1.txt')
    #print(f"df_gene \n{df_gene}")
    df_gene.to_csv(gene_file, index=False)
    #print(f"{gene_file} file created !")
    df_supplimentaryFiles.loc[df_supplimentaryFiles_row, 'Gene_file'] = gene_file
    os.remove('transit.txt')
    os.remove('transit1.txt')                                                          #----------------------gene_file


    # Create CSV file from stem-loop text file
    line_f_sl = gene_names[1]
    # line_f_sl = 'D:/self learning/programs/utr3_ncbi.txt'
    line_f_sl = line_f_sl.strip()
    fil_ = os.path.basename(line_f_sl)
    file = os.path.splitext(fil_)[0]
    extn = os.path.splitext(fil_)[1]

    # Stem-loop data frame
    df_sl = pd.DataFrame()
    df_sl_row = df_sl.shape[0]
    df_sl.loc[df_sl_row, 0] = "SL_Structure"

    with open(line_f_sl, 'r') as fp:
        N1 = len(fp.readlines())  # count number of strains *2
        # print('Total lines:', N1)

    sf = open(line_f_sl, 'r')
    lines = sf.readlines()
    for l in range(N1):
        if l % 2 != 0:
            df_sl_col = df_sl.shape[1]
            for char in lines[l]:
                df_sl.loc[df_sl_row, df_sl_col] = char
                df_sl_col += 1

    # print(f"df_sl\n {df_sl}")

    sl_file = 'stem_loop' + str(df_supplimentaryFiles_row + 1) + '.csv'
    df_sl.to_csv(sl_file, index=False )
    df_supplimentaryFiles.loc[df_supplimentaryFiles_row, 'SL_file'] = sl_file  #-----------------------stem-loop file

    #Creating inputfiles.csv
    df_supplimentaryFiles.to_csv('Supplimentary_Files.csv', index=False)   #----------------------- writting to Supplimentary_file


    #Find the Consensus Sequence
    df_consensus = consensus(df_gene,df_supplimentaryFiles_row)         #----------------------consensus function call

    #Calculating Separaed mutations in repeated Rows
    df_ref = df_consensus
    #print(df_ref)
    ref = df_ref.iloc[-1, 0:]  # extract the consensus sequence
    df_mutation = pd.DataFrame()
    df_mutation_row = 0
    for i in range(df_ref.shape[1]):
        # Mutation Calculation
        col = df_ref.loc['A':'C', str(i + 1)]
        muts = col[col != '0'].index
        if len(muts) != 0:
            for j in range(len(muts)):
                if (j != len(muts) and muts[j] != df_ref.loc['Consensus Sequence', str(i + 1)]):
                    df_mutation.loc[df_mutation_row, 'Position'] = i + 1
                    df_mutation.loc[df_mutation_row, 'Source'] = df_ref.loc['Consensus Sequence', str(i + 1)]
                    df_mutation.loc[df_mutation_row, 'Target'] = muts[j]
                    df_mutation_row += 1
        else:
            df_mutation.loc[df_mutation_row, 'Position'] = i + 1
            df_mutation.loc[df_mutation_row, 'Source'] = 0
            df_mutation.loc[df_mutation_row, 'Target'] = 0
            df_mutation_row += 1
    df_separatedMutation_duplicateRows = df_mutation  #---------------------- Mutation Separated by adding rows with same informations
    #print(df_mutation)

    #Unique Mutations with Stem_loop
    df_result_NF = mutations_stemLoop(df_separatedMutation_duplicateRows, df_sl, df_consensus,df_supplimentaryFiles_row)
    nFrequency_calc_slFile = 'normalisedFrequency_File' + str(df_supplimentaryFiles_row + 1) + '.csv'
    df_result_NF.to_csv(nFrequency_calc_slFile, index = False)
    df_supplimentaryFiles.loc[df_supplimentaryFiles_row, 'result_file'] = nFrequency_calc_slFile

    #titv_calc_filename = 'ti/tv_Calculation_SupplimentaryFile' + str(df_supplimentaryFiles_row + 1) + '.csv'
    #df_titv.to_csv(titv_calc_filename, index=False)
    
    #appending stem_loop file to consensus sequence
    df_consensus = df_consensus.reset_index()
    df_stemLoop = df_sl
    df_stemLoop.columns = df_consensus.columns
    df_consensus = df_consensus.append(df_stemLoop)
    df_consensus = df_consensus.reset_index(drop = True)
    consensus_file = 'Consensus' + str(df_supplimentaryFiles_row + 1) + '.csv'
    df_consensus.to_csv(consensus_file, index=False )


# Combining All Files For Every Data

    # For All Consensus File
    all_consensus = pd.DataFrame()
    if df_supplimentaryFiles_row > 0:
        for files_no in range(df_supplimentaryFiles_row+1):
            #print(f"{files_no}.....{df_supplimentaryFiles.loc[files_no, 'SL_file']}")
            df_con_name = 'Consensus' + str(files_no+1) +'.csv'
            temp_consensus = pd.read_csv(df_con_name)
            #print(f"temp_consensus {files_no} \n", temp_consensus)
            temp_consensus.loc[(temp_consensus.shape[0]), 'Total':'156'] = '---------------------- '
            all_consensus = all_consensus.append(temp_consensus)
            #print(f"all_consensus after APPEND {files_no} \n", all_consensus)
    else:
        all_consensus = df_consensus

    '''
    # For All Mutation File
    all_mutations = pd.DataFrame()
    if df_supplimentaryFiles_row > 0:
        for files_no in range(df_supplimentaryFiles_row+1):
            df_mut_name = 'nonZeroMutations' + str(files_no + 1) + '.csv'
            temp_mutation = pd.read_csv(df_mut_name)
            all_mutations = pd.concat([all_mutations, temp_mutation], axis =1 )
            all_mutations.insert(all_mutations.shape[1], " ", " ", allow_duplicates=True)
            #print(all_mutations)
    else:
        all_mutations = df_separatedMutation_duplicateRows
    '''

    #  For All Result File
    all_result_titv = pd.DataFrame(columns = df_result_NF.columns)
    if df_supplimentaryFiles_row > 0:
            for files_no in range(df_supplimentaryFiles_row + 1):
                df_result_name = 'normalisedFrequency_File' + str(df_supplimentaryFiles_row + 1) + '.csv'
                temp_result = pd.read_csv(df_result_name)
                if files_no == 0:
                    all_result_titv = temp_result
                else:
                    for i in range(all_result_titv.shape[0]):
                        all_result_titv.loc[i, 'ti'] = temp_result.loc[i, 'ti']
                        all_result_titv.loc[i, 'Mutations'] = temp_result.loc[i, 'Mutations']
                        all_result_titv.loc[i, 'Counts_S'] = all_result_titv.loc[i, 'Counts_S'] + temp_result.loc[i, 'Counts_S']
                        all_result_titv.loc[i, 'Counts_L'] = all_result_titv.loc[i, 'Counts_L'] + temp_result.loc[i, 'Counts_L']
                        all_result_titv.loc[i, 'Neucleotide'] = temp_result.loc[i, 'Neucleotide']
                        all_result_titv.loc[i, 'Count in S'] = all_result_titv.loc[i, 'Count in S'] + temp_result.loc[
                            i, 'Count in S']
                        all_result_titv.loc[i, 'Count in L'] = all_result_titv.loc[i, 'Count in L'] + temp_result.loc[
                            i, 'Count in L']
                        all_result_titv.loc[i, 'NFrequency_S'] = all_result_titv.loc[i, 'NFrequency_S'] + temp_result.loc[
                            i, 'NFrequency_S']
                        all_result_titv.loc[i, 'NFrequency_L'] = all_result_titv.loc[i, 'NFrequency_L'] + temp_result.loc[
                            i, 'NFrequency_L']
                    all_result_titv.to_csv('NFcombined.csv')

    else:
        all_result_titv = df_result_NF

    all_result  = all_result_titv.drop('ti', axis=1)

    # Mutations with transitions and Transversions Information
    #print(all_result)
    #print(all_result_titv)
    df_titv = pd.DataFrame(columns=['Stem_ti', 'Stem_tv', 'Stem_ti/tv', 'Loop_ti', 'Loop_tv', 'Loop_ti/tv'])
    # transitions
    mut_ti = all_result_titv.drop(all_result_titv[all_result_titv['ti'] == 0].index)
    ti_s = round(mut_ti['NFrequency_S'].sum(),3)
    ti_l = round(mut_ti['NFrequency_L'].sum(),3)
    # transversions
    mut_tv = all_result_titv.drop(all_result_titv[all_result_titv['ti'] == 1].index)
    tv_s = round(mut_tv['NFrequency_S'].sum(),3)
    tv_l = round(mut_tv['NFrequency_L'].sum(),)
    i = df_titv.shape[0]
    df_titv.loc[i, 'Stem_ti'] = ti_s
    df_titv.loc[i, 'Stem_tv'] = tv_s
    df_titv.loc[i, 'Stem_ti/tv'] = round(ti_s / tv_s,3)
    df_titv.loc[i, 'Loop_ti'] = ti_l
    df_titv.loc[i, 'Loop_tv'] = tv_l
    df_titv.loc[i, 'Loop_ti/tv'] = round(ti_l / tv_l,3)

    all_titv_result = df_titv

    # Returning Values to GUI
    return all_consensus, all_result, all_titv_result



#f = ["D:/PHD/research paper/stem-loop/SLanalysis_app/UTR3'.txt", 'D:/PHD/research paper/stem-loop/SLanalysis_app/utr3_NCBI.txt']
#df_consensus, df_mutations, df_nonZeroMutations_stemLoop = process(f)
#process(f)