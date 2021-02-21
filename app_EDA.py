import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import graph_func as fun
import data_func as dfun

from sklearn.preprocessing import LabelEncoder


st.title("APP")


path = st.text_input('file name')



pages = ['Home','Graphs','Outliers']

loaded = False

if path:
    try:
        df = pd.read_csv(path) 

        le = LabelEncoder()

        cols = df.columns

        for col in cols:
            if df[col].dtypes == object:

                c = df[col]

                df[col] = c


        loaded = True
        st.write("File has been loaded")

        v = st.checkbox('View data')
        if v:
            st.write(df)
    except:
        st.write("No such file found") 
        


reps = ['Column Statistics','Distribution Plot','Bar Plot','Correlation Heatmap','Scatter Plot']



rad =st.sidebar.selectbox("Navigation",pages)


if rad == "Home":
    st.write('')
elif rad == "Graphs":    

    if loaded:

        representation = st.selectbox('Representation',reps)

        if representation == 'Column Statistics':
            fun.col_stats(st,df)

        elif representation == 'Distribution Plot':
            fun.dist_plot(st,df) 

        elif representation == 'Bar Plot':
            fun.bar_plot(st,df)


        elif representation == 'Correlation Heatmap':
            fun.corr_plot(st,df)

        elif representation == 'Scatter Plot':
            fun.scat_plot(st,df)

elif rad == "Outliers":
    
    col = st.selectbox('Column',list(df.columns))
    impact = st.selectbox('Impact',list(df.columns))

    if df[impact].nunique() < 20:
        dfun.outlier_analysis(st,df,col,impact)

    else:
        st.write('Choose a Categorical variable for testing impact over')    




    
