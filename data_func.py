import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import binom
import math



def get_outlier_impact_dataframe(data_clean,col,impact):

    iqr = data_clean[col].quantile(0.75) - data_clean[col].quantile(0.25) 
    upper_cutoff = data_clean[col].quantile(0.75) + iqr*1.5
    lower_cutoff = data_clean[col].quantile(0.25) - iqr*1.5

    n_up = data_clean[data_clean[col] > upper_cutoff]
    n_low = data_clean[data_clean[col] < lower_cutoff]

    values = data_clean[impact].unique()

    rows = ['All Data','Below IQR range','Above IQR range']

    iqr_data = pd.DataFrame(rows)

    new_col = []
    new_col.append(len(data_clean))
    new_col.append(len(n_low))
    new_col.append(len(n_up))

    iqr_data['total'] = new_col

    for val in values:
        new_col = []
        new_col.append(len(data_clean[data_clean[impact] == val]))
        new_col.append(len(n_low[n_low[impact] == val]))
        new_col.append(len(n_up[n_up[impact] == val]))

        iqr_data[impact+' = '+str(val)] = new_col
        
    return iqr_data


def probs(df):
    row = list(df.iloc[0])
    
    prob = []   
    for i in range(2,len(row)):
        prob.append(row[i]/row[1])
    return prob


def check_row(row,prob):#row is df row as list
    n = row[1]
    
    mean = []
    sdev = []   
    for p in prob:
        mean.append(int(n*p))
        sdev.append(int(binom.std(n,p)))
        
    return mean,sdev    



def outlier_analysis(st,data_clean,col,impact):
    
    out_frame = get_outlier_impact_dataframe(data_clean,col,impact)
        
    st.write(out_frame)
    

