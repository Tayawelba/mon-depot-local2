import streamlit as st
import numpy as np
import pandas as pd

class DataEvaluator:
    def __init__(self, df):
        self.df = df

    def show_head(self):
        # Affichage de l’en-tête et des premières lignes du dataframe
        st.write('L’en-tête et les premières lignes du DataFrame sont: ')
        st.dataframe(self.df.head(10))

    def show_dimensions(self):
        # Affichage des dimensions du dataframe
        dimensions = 'Les dimensions du DataFrame sont les suivantes : ' + str(self.df.shape[0]) + ' lignes et ' + str(
            self.df.shape[1]) + ' colonnes.'
        st.write(dimensions)

    def show_columns(self):
        # Affichage des noms de colonnes
        columns_names = ', '.join(list(self.df.columns))
        st.write('Les colonnes du DataFrame : ' + columns_names + '.')
