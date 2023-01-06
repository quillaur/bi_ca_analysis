import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    fig, ax = plt.subplots()
    ax = df["amount"].plot()
    st.pyplot(fig)