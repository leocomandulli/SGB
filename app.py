import sqlite3
import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

# ----- Importação das páginas ------
import Biblioteca
import Home
import Search
import ultimos_registros
import Dashboard

# ------ Configuração da página ------

st.set_page_config(page_title="Painel TCP")

# ----- Imagem de cabeçalho -----
st.sidebar.image("Images/logo.png", use_column_width=True)

# ------ Classe MultiApp ------
class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='Painel SGB',
                options=['Home', 'Biblioteca', 'Busca família', 'Ultimos Registros', 'Dashboard' ],
                icons=['house-fill', 'book', 'search', 'clock', 'graph-up'],
                menu_icon='list',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'white'},
                    "icon": {"color": "black", "font-size": "20px"},
                    "nav-link": {"color": "black", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#A9A9A9"},
                    "nav-link-selected": {"background-color": "#696969"},
                }
            )

        if app == "Home":
            Home.app()
        elif app == "Biblioteca":
            Biblioteca.app()
        elif app == "Busca família":
            Search.app()
        elif app == "Ultimos Registros":
            ultimos_registros.app()
        elif app == "Dashboard":
            Dashboard.app()


# ------ Execução da aplicação ------

if __name__ == "__main__":
    multi_app = MultiApp()
    multi_app.run()

# ------ Conexão ao banco de dados ------

def load_data():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('TCP.db')
    cursor = conn.cursor()

    # Carregar dados da tabela 'Base_de_Familias'
    query = "SELECT * FROM Base_de_Familias"
    df = pd.read_sql_query(query, conn)

    # Fechar a conexão após carregar os dados
    conn.close()
    return df

# Adiciona a leitura do banco ao session_state
extrato_biblioteca = load_data()
st.session_state["extrato_biblioteca"] = extrato_biblioteca

