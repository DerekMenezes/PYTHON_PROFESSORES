# app.py
import streamlit as st

st.set_page_config(
    page_title="Projetos",
    page_icon="⚛️",
    layout="wide"
)

st.title("📊 Projetos Python")

st.sidebar.success("Selecione uma página acima 👆")

st.markdown("""
### Sobre os projetos
Contém i) dashboard explora dados globais de **consumo de energia elétrica**,
comparando fontes **renováveis** e **não renováveis** ao longo do tempo.
ii) Modelo de resfriamento em superfícies.

📊 **Dataset:** World Energy Consumption (Kaggle)

👈 Use o menu lateral para navegar entre as análises.
""")
