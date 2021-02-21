import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



def col_stats(st,df):
    st.write(df.describe())




def dist_plot(st,df):

    names = list(df.columns)
    names.append("None")
    option = st.selectbox('Column',list(df.columns))
    groupby = st.selectbox('Group by',names,index=(len(names)-1))

    if groupby == "None":
        if option:
            st.write('Mean : '+str(df.mean()[option]))
            st.write('Standard Deviation : '+str(df.std()[option]))
            st.write('Median : '+str(df.median()[option]))
            st.write('Mode : '+str(df.mode()[option][0]))
            st.write('Skew : '+str(df.skew()[option]))
            st.write('Kurtosis : '+str(df.kurtosis()[option]))
            fig, ax = plt.subplots()
            sns.distplot(df[option])
            st.pyplot(fig)

    else:   
        if option:
            if groupby:
                values = df[groupby].unique()

                
                if len(values) < 20:
                    fig, ax = plt.subplots()

                    means = []
                    for val in values:
                        try:
                            sns.distplot(df[df[groupby] == val][option])
                        except RuntimeError as re:
                            if str(re).startswith("Selected KDE bandwidth is 0. Cannot estimate density."):
                                sns.distplot(df[df[groupby] == val][option], kde_kws={'bw': 0.1})
                            else:
                                raise re    

                        st.write('**'+groupby +' = '+str(val)+' :**')
                        st.write('Skew : '+str(df[df[groupby] == val].skew()[option]))
                        st.write('Mean : '+str(df[df[groupby] == val].mean()[option]))
                        means.append(df[df[groupby] == val].mean()[option])
                    st.pyplot(fig)        
                      
                else:
                    st.write('too many values for column')    



def bar_plot(st,df):
    X = st.selectbox('Category',list(df.columns))
    Y = st.selectbox('Variable average for category selected above',list(df.columns))

    if len(df[X].unique()) < 25:

        fig, ax = plt.subplots()
        sns.barplot(x = X, y = Y, data = df)
        st.pyplot(fig)

        
    else:
        st.write('too many values for categorical variable, choose another variable')

    






def corr_plot(st,df):
    fig, ax = plt.subplots()    
    sns.heatmap(df.corr(),annot=True)     
    st.pyplot(fig)        


def scat_plot(st,df):
    X = st.selectbox('X-column',list(df.columns))
    Y = st.selectbox('Y-column',list(df.columns))
    names = list(df.columns)
    names.append("None")
    groupby = st.selectbox('Group by',names,len(names)-1)
    

    fig, ax = plt.subplots()    
    if groupby == "None":
        sns.scatterplot(data=df, x = X, y = Y)
    else:
        sns.scatterplot(data=df, x = X, y = Y,hue = groupby)

    st.pyplot(fig)    
                     
