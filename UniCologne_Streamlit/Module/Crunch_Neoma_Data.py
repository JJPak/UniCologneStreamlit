import pandas as pd

def crunch_neoma_data(df, isotope_system ):


    # define all the elements that can be processed

    Element = ['Hf']

    Measured = [['173Yb Static 1', '174Hf Static 1', '175Lu Static 1', '176Hf Static 1', '177Hf Static 1', '178Hf Static 1', '179Hf Static 1', '180Hf Static 1', '181Ta Static 1', '183W Static 1', '177Hf.O Static 1',
                '178Hf/177Hf', '179Hf/177Hf', '173Yb/177Hf', '175Lu/177Hf', '181Ta/177Hf', '183W/177Hf', '174Hf/177Hf + I', '176Hf/177Hf + I', '180Hf/177Hf + I', '173Yb/176Hf monitor', '175Lu/176Hf monitor',
                '174Hf/177Hf MB+I', '176Hf/177Hf MB+I', '180Hf/177Hf MB+I', '177Hf.O/177Hf']]


    if isotope_system not in Element:
        print('Error: Element not found in the list')
        return None

    # find index of the chosen element
    index = Element.index(isotope_system)

    # choose the measured elements for the chosen element
    list_measured = Measured[index]


    # prepare the dataframe for easier manipulation

    df.iloc[0,2] = 'Elements'
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    df = df.iloc[0:,2:].reset_index(drop=True)


    # make a list with the rows that are needed

    order_list = [] # list for average values and se values
    for i in list_measured:
        average_val_string = i+' Mean'
        order_list.append(average_val_string)

    for i in list_measured:
        average_val_string = i+' SE'
        order_list.append(average_val_string)

    # only take out the rows that are needed which are the averages and the 1se row

        # Create a dummy df with the required list and the col name to sort on
    dummy = pd.Series(order_list, name = 'Elements').to_frame()
        # Use left merge on the dummy to return a sorted df
    sorted_df = pd.merge(dummy, df, on = 'Elements', how = 'left')
    df = sorted_df


    # transpose dataframe and make new header

    df = df.transpose()
    new_header = df.iloc[0] #grab the first row for the header
    df = df[2:] #take the data less the header row
    df.columns = new_header #set the header row as the df header

    # Calculate the 1se % for each element

    for i in list_measured:
        
        df[i+' 1SE %'] = (df[i+' SE'] / df[i+' Mean']) * 100
        
    # drop all columns except Mean and 1SE %

    for i in list_measured:
        df = df.drop(columns=[i+' SE'])

    df = df.transpose()

    return df
