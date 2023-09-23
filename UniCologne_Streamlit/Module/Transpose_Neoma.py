import pandas as pd
import numpy as np


def append_empty_row(df): # a function that appends an empty row at the end of a dataframe
    empty_list = []
    column_names = []
    for i in df:
        empty_list.append(np.nan)
        column_names.append(i)
        
    empty_row = pd.Series(empty_list, index=column_names)
    df = pd.concat([df,empty_row.to_frame().T]).reset_index(drop=True)
    return df


def data_crunch_neoma (df, element_choose):
    
    df_list = []
    sample_list = []
    sample_list2 = []
    sample_list3 = []
    
    if element_choose == 'W':
        element_list_orig = ['Static 1:177Hf', 'Static 1:178Hf', 'Static 1:180W', 'Static 1:181Ta', 'Static 1:182W', 'Static 1:183W',
                         'Static 1:184W','Static 1:186W', 'Static 1:188Os', '180W/184W', '182W/184W', '183W/184W', '186W/184W',
                         '177Hf/184W', '181Ta/184W' '188Os/184W']

        element_list_rename = ['177Hf', '178Hf', '180W', '181Ta', '182W', '183W', '184W', '186W', '188Os',
                            '180W/184W', '182W/184W', '183W/184W', '186W/184W',  '177Hf/184W', '181Ta/184W', '188Os/184W', ]


        missing_ratios_list      = ['180W/183W', '182W/183W', '184W/183W', '186W/183W', '177Hf/183W','181Ta/183W', '188Os/183W'  ]
        numerator_list           = ['180W',      '182W',      '184W',      '186W',      '177Hf',     '181Ta',      '188Os'       ]
        denominator_list         = [     '183W',      '183W',      '183W',      '183W',       '183W',      '183W',       '183W'  ]

        final_order_list = ['177Hf', '178Hf', '180W', '181Ta', '182W', '183W', '184W', '186W', '188Os',
                            '180W/184W', '182W/184W', '183W/184W', '186W/184W', '180W/183W', '182W/183W',
                            '184W/183W', '186W/183W', '177Hf/184W', '181Ta/184W', '188Os/184W', '177Hf/183W',
                            '181Ta/183W', '188Os/183W']

    
    
    
    
    
    
    
    
    df = df.rename(columns = {'Unnamed: 0':'Measurement order', 'Unnamed: 1':'Sample'})
    
    check_elements = df.iloc[[1]].values.tolist()

    # check if element_list_orig in df
    for i in range(len(element_list_orig[0])):
        if element_list_orig[i] not in check_elements[0]:
            return print('ERROR: the CSV FILE does not contain '+ element_list_orig[i])
    
    # change order of columns
    df.insert(0, 'Sample', df.pop('Sample'))
    
    # rename cell in column 'Sample'
    df.loc[0, 'Sample'] = 'Cycle'
    df.loc[1, 'Sample'] = 'Isotope'
    df.loc[2, 'Sample'] = 'Unit'
    
    #  replace old names with new names
    for i in range(len(element_list_orig)):
        df.replace(element_list_orig[i], element_list_rename[i], inplace = True)
    
    # # Transpose data frame
    df = df.T.reset_index(drop=True)
    
    #  New header
    new_header = df.iloc[0] #grab the first row for the header
    df.columns = new_header #set the header row as the df header
    
    # Drop first row using drop()
    df.drop(index=df.index[0], axis=0, inplace=True)
    df = df.reset_index(drop=True)
    
    # replace and add to cycle
    for i in range(0,60):
        for j in range(len(df['Unit'])):
            if df['Unit'][j] == f'Y[{i}] (Ratio)':
                df.loc[j, 'Cycle'] = i

    # drop Unit
    df.drop('Unit', axis=1, inplace=True)
    
    
    for i in element_list_rename:
        df_append = df[df['Isotope']== i ].reset_index(drop=True)
        df_list.append(df_append)
    
    for frames in df_list:
        name = frames.loc[0,'Isotope']
        row = [name]*len(frames.columns)
        frames.loc[60] = row
    
    lister = []
    for columns in range(len(df_list[0].columns)):
        for frames in df_list:
            lister.append(frames.iloc[:,columns:columns+1])
        df_new = pd.concat(lister, axis=1)
        sample_list.append(df_new)
        lister.clear()
        
    del sample_list[0]
    del sample_list[0]
    
    
    for frames in sample_list:
        column_name = frames.columns[0]
        column_name = [column_name]*len(frames)
        del column_name[-1]
        column_name.append('Sample')
        frames['Sample'] = column_name
    
    #  New header
    for frames in sample_list:
        new_header = frames.iloc[60] #grab the first row for the header
        frames.columns = new_header #set the header row as the df header

    for frames in sample_list:
        frame_2 = frames.drop([60])
        for i in element_list_rename:
            frame_2[i] = frame_2[i].astype(float)
        
        sample_list2.append(frame_2)
        
          
    #add other ratios
    for i in range(len(missing_ratios_list)):
        for frames in sample_list2:
            frames[missing_ratios_list[i]] = frames[numerator_list[i]] / frames[denominator_list[i]]
            frames['Cycle'] = range(1,61)
            
    final_order_list.insert(0, 'Sample')
    final_order_list.insert(1, 'Cycle')
    
    for frames in sample_list2:
        frames_new = frames[final_order_list]
        frames_new = append_empty_row(frames_new)
        sample_list3.append(frames_new)
    
    df_new = pd.concat(sample_list3)
    final_df = df_new.T


    return final_df
