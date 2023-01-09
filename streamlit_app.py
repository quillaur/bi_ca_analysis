import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Analyse du CA",
    page_icon="🧊",
    layout="wide"
)

st.title("Analyse du CA")

list_of_dataframes = []

uploaded_files = st.sidebar.file_uploader("Upload tes fichiers", accept_multiple_files=True, type="xlsx")
if uploaded_files is not None:
    for uploaded_file in uploaded_files: 
        list_of_dataframes.append(pd.read_excel(uploaded_file))
    
    if list_of_dataframes:
        df = pd.concat(list_of_dataframes, ignore_index=True)
        years_available = df["Annee"].unique().tolist()
        years_available.sort()

        with st.sidebar.form("Variables"):
            years = st.multiselect("Quelle(s) année(s) ?", years_available, default=years_available)
            option = st.radio("Visualiser par:", ('Mois', 'Semaine'))

            submit = st.form_submit_button("Valider")
        
        x_var = "Semaine"

        if option == "Mois":
            df["Mois"] = df.apply(lambda x: datetime.fromisocalendar(int(x.Annee), int(x.Semaine), 1).month, axis=1)
            df = df.groupby(by=["Annee", "Mois"], as_index=False).sum()
            x_var = "Mois"


        c1, c2 = st.columns(2, gap="large")
        if len(years) == len(years_available):
            with c1:        
                fig = px.line(df, x=x_var, y="Real_Fact", title=f'CA par {option}', color="Annee")
                st.plotly_chart(fig)
            
            with c2:
                df["RF_cumsum"] = df.groupby(by=["Annee"])['Real_Fact'].cumsum()
                fig = px.line(df, x=x_var, y="RF_cumsum", title=f'Somme cumulée du CA par {option}', color="Annee")
                st.plotly_chart(fig)

                # last_year_data = df[(df["Annee"] == years_available[0]) & (df["Real_Fact"] > 0)]["Real_Fact"]
                # ca_last = last_year_data.sum()
                # ca_prev = df[df["Annee"] == years_available[1]]["Real_Fact"][:last_year_data.shape[0]].sum()

                # diff = ca_last - ca_prev
                # delta = f"+{round(diff, 2)} k€" if diff > 0 else f"{round(diff, 2)} k€"

                # st.metric(label=f"Comparaison du CA à la même période de {years_available[0]} vs {years_available[1]}", 
                #     value=f"{round(ca_last, 2)} k€", 
                #     delta=delta)

            fig = px.bar(df, x=df["Annee"].astype("string"), y=["Obj_Fact", "Real_Fact"],
                        #  color="species", 
                        #  hover_data=['petal_width'],
                        title="Comparaison des objectifs et CA et réalisés par année",
                        labels={'x':'Années', "value": "Real_Fact"},
                        barmode = 'group')
            st.plotly_chart(fig, use_container_width=True)
            
        else:       
            with c1:  
                df = df[df["Annee"].isin(years)]
                # st.dataframe(df)
                fig = px.bar(df, x=x_var, y=["Obj_Fact", "Real_Fact"],
                        #  color="species", 
                        #  hover_data=['petal_width'],
                        barmode = 'group')
                st.plotly_chart(fig)
            
            with c2: 
                df["OF_cumsum"] = df.groupby(by=["Annee"])['Obj_Fact'].cumsum()
                df["RF_cumsum"] = df.groupby(by=["Annee"])['Real_Fact'].cumsum()
                fig = px.bar(df, x=x_var, y=["OF_cumsum", "RF_cumsum"],
                        #  color="species", 
                        #  hover_data=['petal_width'],
                        barmode = 'group')
                st.plotly_chart(fig)

        # st.dataframe(df)
        # st.write(df.dtypes)
        
        # gdf = df.groupby(by=["Annee"])["Obj_Fact", 'Real_Fact'].cumsum()
        # st.dataframe(gdf)
        # df = px.data.gapminder().query("continent=='Oceania'")
        # st.dataframe(df)

        
        
        
        # yearly_ca = pd.DataFrame()
        
        # for year in df.Annee.unique():
        #     yearly_ca[year] = df.loc[df['Annee'] == year, 'Real_Fact']

        # st.dataframe(yearly_ca)